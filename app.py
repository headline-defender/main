import os
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, g, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import secrets
import shutil
import operateDB as odb
import utilty as utl
import datetime

UPLOAD_FOLDER = "static/images"

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    base_dir, "DB", "app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # バイト単位
# セッション機能使用時のシークレットキー
app.secret_key = secrets.token_hex(16)

db = SQLAlchemy(app)

agent_dict = utl.read_conf("/working/static/conf/agent_list.txt")
map_dict = utl.read_conf("/working/static/conf/map_list.txt")



# データベース接続
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("/working/DB/app.db")
    return g.db


# データベース切断
@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db:
        db.close()

@app.route("/")
def condition_select():
    return render_template("index.html", maps=map_dict, agents=agent_dict)

@app.route('/view', methods=['GET'])
def view():
    map_name = request.args.get('map_name')
    agent_name = request.args.get('agent_name')
    agent_name_jp = next(
            (a["label"] for a in agent_dict if a["value"] == agent_name), None
        )
    map_img_path = os.path.join("static", "maps", map_name + ".png")

    # DBから定点情報読み込み
    conn = get_db()
    c = conn.cursor()
    is_read = odb.read_lineups(c, map_name, agent_name)
    if not is_read:
        return "情報を読み込めませんでした"
    lineups = c.fetchall()
    if len(lineups) == 0:
        flash('検索結果が0件でした')
        return render_template("index.html", maps=map_dict, agents=agent_dict)

    # 取得情報をdictに変換
    keys = [
        'lineup_id', 'map_name', 'agent_name', 'site',
        'marker_x', 'marker_y', 'created_at'
    ]
    lineup_dict = [dict(zip(keys, item)) for item in lineups]
    
    # 関連画像を取得
    lineup_ids = [d['lineup_id'] for d in lineup_dict]
    is_read = odb.read_lineup_image(c,lineup_ids)
    if not is_read:
        return "情報を読み込めませんでした"
    linieup_images = c.fetchall()
    conn.close()
    keys = [
        'lineup_id', 'image_path', 'description'
    ]
    image_dict = [dict(zip(keys, item)) for item in linieup_images]
    print(image_dict)

    return render_template('view.html',
                           lineups = lineup_dict,
                           lineup_images = image_dict,
                           map_img_path = map_img_path,
                           agent_name_jp = agent_name_jp)

# アップロード画面
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # 入力値の取得
        map_name = request.form["map_name"]
        agent_name = request.form["agent_name"]
        # 確認画面に渡す際にエラーにならないように事前に作成
        stand_filepath = None

        # 確認画面への変数格納
        session["form_data"] = request.form.to_dict()
        session["form_data"]["map_name_jp"] = next(
            (m["label"] for m in map_dict if m["value"] == map_name), None
        )
        session["form_data"]["agent_name_jp"] = next(
            (a["label"] for a in agent_dict if a["value"] == agent_name), None
        )

        if request.form.get("stand_check"):
            is_poition = True
        else:
            is_poition = False

        # ファイルの取得と保存
        if "file" not in request.files:
            return "ファイルがありません", 400
        file = request.files["file"]
        if file.filename == "":
            return "ファイルが選択されていません", 400
        if file and utl.allowed_file(file.filename):
            # ファイル保存
            ext = os.path.splitext(file.filename)[1].lower()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{map_name}_{agent_name}_{timestamp}{ext}"

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], "temp", filename)
            file.save(filepath)

            # 立ち位置画像を追加
            if is_poition:

                # 画像を保存
                stand_file = request.files["stand_file"]
                ext = os.path.splitext(stand_file.filename)[1].lower()
                stand_filename = f"stand_{map_name}_{agent_name}_{timestamp}{ext}"
                stand_filepath = os.path.join(
                    app.config["UPLOAD_FOLDER"], "temp", stand_filename
                )
                stand_file.save(stand_filepath)

            return render_template(
                "upload_confirm.html",
                form_data=session["form_data"],
                filepath=filepath,
                stand_filepath=stand_filepath,
                is_poition=is_poition,
            )

    # GETメソッド(ページ読み込み時)
    else:
        return render_template("upload.html", maps=map_dict, agents=agent_dict)


# アップロード確認画面
@app.route("/upload_confirm", methods=["GET", "POST"])
def upload_confirm():
    if request.method == "POST":
        # 入力値の取得
        map_name = request.form["map_name"]
        marker_x = request.form["marker_x"]
        marker_y = request.form["marker_y"]
        agent_name = request.form["agent_name"]
        site = request.form["site"]
        description = request.form["description"]
        image_src = request.form["image_src"]

        # ファイルの取得と保存
        if image_src != "":
            moved_path = shutil.move(image_src, app.config["UPLOAD_FOLDER"])

            # DBへ登録
            conn = sqlite3.connect("/working/DB/app.db")
            c = conn.cursor()

            is_created = odb.create_lineups(
                c, map_name, agent_name, site, marker_x, marker_y
            )

            # 作成操作が失敗した場合
            if not is_created:
                conn.rollback()

            # 新しく作られた定点IDを取得
            lineup_id = c.lastrowid

            # 定点画像を登録

            is_created = odb.create_lineup_images(c, lineup_id, moved_path, description)
            if not is_created:
                conn.rollback()

        # 立ち位置を追加している場合
        if request.form.get("stand_description"):
            stand_image_src = request.form["stand_image_src"]
            stand_description = request.form["stand_description"]
            # 画像を保存
            moved_path = shutil.move(stand_image_src, app.config["UPLOAD_FOLDER"])

            # DBへ登録

            is_created = odb.create_lineup_images(
                c, lineup_id, moved_path, stand_description, is_position=1
            )
            if not is_created:
                conn.rollback()

        conn.commit()
        conn.close()

        # 正常終了
        if is_created:
            return render_template("upload_result.html")
        else:
            return f"ID: {lineup_id}の登録に失敗"


# アップロード完了画面
@app.route("/upload_result", methods=["GET", "POST"])
def upload_result():
    if request.method == "GET":
        return render_template("upload_result.html")


if __name__ == "__main__":
    # 開発環境でのみ使用
    app.run(host="0.0.0.0", debug=True)
