import json
from data_process import one_car_re
from flask import Flask, render_template, request, flash, jsonify
from werkzeug.utils import redirect
from datetime import timedelta

app = Flask(__name__, template_folder='templates')

app.secret_key = 'itheima'


# 车款评论信息总页面 2.0
@app.route("/last")
def last():
    return render_template('last.html')


# 车款评论信息总页面1.0
@app.route("/car_command_list")
def car_command_list():
    return render_template('car_command_list.html')


# 根据用户选择更新图表
@app.route("/car_command", methods=['GET', 'POST'])
def car_command():
    data = json.loads(request.form.get('data'))
    one_car_re(data['car_name'])  # 根据车名生成图表所需的数据
    name = data['car_name']
    f = open("static/command_data/" + name + ".json", 'r', encoding='utf-8')
    json_data = json.load(f)
    f.close()

    return json_data


# 默认路由
@app.route("/")
def index():
    return redirect('/login')


# 初始页面
@app.route("/index")
def first_page():
    return render_template('index.html')


@app.route("/gra_one")
def gra_one_show():
    return render_template("gra_one.html")


@app.route("/car_price")
def car_price_show():
    return render_template("car_price.html")


@app.route("/power_type")
def power_type_show():
    return render_template("power_type.html")


@app.route("/score_line")
def score_line_show():
    return render_template("score_line.html")


@app.route("/command")
def command_show():
    return render_template("command.html")


# 登录页面
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        return render_template("index.html")
    else:
        return "没有做呢"


if __name__ == '__main__':

    # 设置静态文件缓存过期时间
    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
    app.send_file_max_age_default = timedelta(seconds=1)
    app.run(debug=True)


@app.route("/login_", methods=["GET", "POST"])
def index_():
    if request.method == "GET":
        return "success"
        return render_template("login_self.html")
        # username = request.form.get("username")
        # password = request.form.get("password")
        # password2 = request.form.get("password2")

        # if not all([username, password, password2]):
        #     print("参数不完整")
            # flash(u"参数不完整")
        # elif password != password2:
        #     print("密码不一致")
        #     flash(u"密码不一致")
        # else:
        #     return 'success'


# @app.route("/register")
# def register():
#     return render_template("register.html")


# @app.route("/result", methods=['POST', "GET"])
# def result():
#     if request.method == "POST":
#         result = request.form
#     return render_template("result.html", result=result)