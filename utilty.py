import os
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# 拡張子を判定
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# テキスト読み込み関数
def read_conf(file_path, detail=False):
    f = open(file_path, 'r', encoding='UTF-8')

    data = f.read()
    contents_list = data.split("\n")

    contents_dict = [
        {
            "value": en,
            "label": jp,
            "image_path": os.path.join("static", "icon", f"{en}.png"),
            **(
                {"detail_path": os.path.join("static", "maps", f"{en}.png")}
                if detail else {}
            )
        }
        for item in contents_list
        for jp, en in [item.split(",", 1)]
    ]
    f.close()

    return contents_dict