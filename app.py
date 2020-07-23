from flask import Flask, request
from config import *
from flask_cors import CORS
import json
import pandas
from SERI import draw_little_elephant, draw_elephant, dict2list

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
    # print(temp)
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
    # print(str1)
    db = SQLManager()
    temp = db.get_list(str1)
    # print(temp)
    db.close()
    return json.dumps(temp, ensure_ascii=False)


@app.route("/elephant", methods=["POST", "GET"])
def great_elephant():  # 默认返回内容
    return_dict = {'return_code': 200, 'return_info': '处理成功', 'result': False}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

    # 获取传入的参数
    get_Data = request.get_data()
    get_Data = json.loads(get_Data)
    area = get_Data.get('area')
    r1 = float(get_Data.get('r1'))
    r2 = float(get_Data.get('r2'))
    # prem = "'上海'"
    population = 'select province_population from summer.population where province_name=' + ('\'') + area + ('\';')
    count = 'SELECT confirmedCount FROM summer.china_provincedata where dateId=20200124 and provinceShortName=' + (
        '\'') + area + '\';'
    db = SQLManager()
    population = int((db.get_list(population))[0]['province_population'])
    count = int(db.get_list(count)[0]['confirmedCount'])
    # print(population)
    # print(count)
    db.close()
    data = draw_little_elephant(r1, r2, int(population))
    date_data = [d.strftime('%Y%m%d') for d in pandas.date_range('20200105', '20200711')]

    return json.dumps({'small_elephant': data[16:], 'big_elephant': date_data[16:]}, ensure_ascii=False)


@app.route("/predict_2", methods=["POST", "GET"])
def giant_elephant():  # 默认返回内容
    return_dict = {'return_code': 200, 'return_info': '处理成功', 'result': False}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

    # 获取传入的参数
    get_Data = request.get_data()
    get_Data = json.loads(get_Data)
    area = get_Data.get('area')
    # prem = "'上海'"
    population = 'select province_population from summer.population where province_name=' + ('\'') + area + ('\';')
    # count = 'SELECT confirmedCount FROM summer.china_provincedata where dateId=20200124 and provinceShortName=' + (
    #     '\'') + area + ('\';')
    db = SQLManager()
    population = int((db.get_list(population))[0]['province_population'])
    # count = int(db.get_list(count)[0]['confirmedCount'])
    r1 = 'SELECT r1 FROM summer.rate where province_name=' + '\'' + area + '\';'
    r2 = 'SELECT r2 FROM summer.rate where province_name=' + '\'' + area + '\';'
    r1 = float(db.get_list(r1)[0]['r1'])
    r2 = float(db.get_list(r2)[0]['r2'])
    # print(r1, r2)
    # print(population)
    # print(count)
    db.close()
    data = draw_little_elephant(r1, r2, int(population))
    increase_data = [0]
    for i in range(1, len(data)):
        increase_data.append(data[i] - data[i - 1])
    # print(len(increase_data))

    date_data = [d.strftime('%Y%m%d') for d in pandas.date_range('20200105', '20200711')]

    return json.dumps(
        {'small_elephant': data[16:], 'big_elephant': date_data[16:], 'increase_elephant': increase_data[16:]},
        ensure_ascii=False)


@app.route("/predict", methods=["POST", "GET"])
def elephant_king():  # 默认返回内容
    return_dict = {'return_code': 200, 'return_info': '处理成功', 'result': False}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

    # 获取传入的参数
    get_Data = request.get_data()
    get_Data = json.loads(get_Data)
    area = get_Data.get('area')
    regulation_vaccine = get_Data.get('data')
    regulation_vaccine = dict2list(regulation_vaccine)
    population = 'select province_population from summer.population where province_name=' + '\'' + area + '\';'
    r0 = 'SELECT r1 FROM summer.rate where province_name=' + '\'' + area + '\';'
    db = SQLManager()
    population = float((db.get_list(population))[0]['province_population'])
    r0 = float(db.get_list(r0)[0]['r1'])
    # print(r0)
    db.close()
    data = draw_elephant(regulation_vaccine=regulation_vaccine, population=population, r0=r0)
    increase_data = [0]
    for i in range(1, len(data)):
        increase_data.append(data[i] - data[i - 1])
    # print(len(data))
    date_data = [d.strftime('%Y%m%d') for d in pandas.date_range('20200105', '20200711')]
    # print(len(date_data))
    return json.dumps({'predict_data': data[16:], 'time': date_data[16:], 'increase_data': increase_data[16:]},
                      ensure_ascii=False)
    # return json.dumps(return_dict, ensure_ascii=False)


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
        '\'') + prem + '\' order by dateId;'
    db = SQLManager()
    re = db.get_list(str1)
    temp = {'confirmeCount': [i['confirmedCount'] for i in re], 'confirmedIncr': [i['confirmedIncr'] for i in re],
            'dateId': [str(i['dateId'])[4:] for i in re]}
    db.close()
    result = json.dumps(temp, ensure_ascii=False)
    return result


if __name__ == '__main__':
    app.run(host='192.168.31.124', port=5000, debug=False)
    # app.run(host='192.168.31.245', port=8000, debug=False)
