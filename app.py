from flask import Flask, request
from config import *
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/login", methods=["POST"])
def check():  # 默认返回内容

    return_dict = {'return_code': 200, 'return_info': '处理成功', 'result': False}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

    # 获取传入的参数
    get_Data = request.get_data()
    get_Data = json.loads(get_Data)

    if get_Data.get('username') == 'admin' and get_Data.get('password') == '123456':
        return_dict = {'return_code': 1, 'return_info': '登陆成功', 'result': 0, 'token': '0'}

    return json.dumps(return_dict, ensure_ascii=False)


@app.route('/check_db', methods=['GET', 'POST'])
def check_db():
    db = SQLManager()
    temp = db.get_list('select * from temp')
    print(temp)
    db.close()
    return_dict = {'return_code': 200, 'return_info': '处理成功', 'result': False}
    return json.dumps(return_dict, ensure_ascii=False)


@app.route("/population", methods=["POST", "GET"])
def city_info():  # 默认返回内容
    return_dict = {'return_code': 200, 'return_info': '处理成功', 'result': False}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

    # 获取传入的参数
    get_Data = request.get_data()
    get_Data = json.loads(get_Data)
    prem = get_Data.get('key')
    # prem = "'上海'"
    str1 = 'select * from summer.population where province_name=' + ('\'') + prem + ('\';')
    print(str1)
    db = SQLManager()
    temp = db.get_list(str1)
    print(temp)
    db.close()
    return json.dumps(temp, ensure_ascii=False)


@app.route("/infection", methods=["POST", "GET"])
def china_provincedata():  # 默认返回内容
    return_dict = {'return_code': 200, 'return_info': '处理成功', 'result': False}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

    # 获取传入的参数
    get_Data = request.get_data()
    get_Data = json.loads(get_Data)
    prem = get_Data.get('key')

    str1 = 'SELECT confirmedCount, confirmedIncr, dateId FROM summer.china_provincedata where provinceShortName=' + (
        '\'') + prem + ('\';')
    db = SQLManager()
    re = db.get_list(str1)
    temp = {'confirmeCount': [i['confirmedCount'] for i in re], 'confirmedIncr': [i['confirmedIncr'] for i in re],
            'dateId': [str(i['dateId'])[4:] for i in re]}
    print(temp)
    db.close()
    result = json.dumps(temp, ensure_ascii=False)
    return result


if __name__ == '__main__':
    app.run(host='192.168.31.124', port=5000, debug=False)
    # app.run(host='0.0.0.0', port=5000, debug=False)
