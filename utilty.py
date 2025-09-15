ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# 拡張子を判定
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# テキスト読み込み関数
def read_conf(file_path):
    f = open(file_path, 'r', encoding='UTF-8')

    data = f.read()
    contents_list = data.split("\n")

    contents_dict = [
        {"value": en, "label": jp}
        for item in contents_list
        for jp,en in [item.split(",", 1)]
]
    f.close()

    return contents_dict