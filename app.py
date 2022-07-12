from flask import Flask, render_template,json,request,jsonify
import requests

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.3cgedw6.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


app = Flask(__name__)


# @app.route('/', methods=["GET"])
# def main():
#
#     #openApi 에서 해수욕장 값 받기
#     citys = ["인천", "강원", "제주"];
#     for city in citys :
#         url = 'http://apis.data.go.kr/1192000/service/OceansBeachInfoService1/getOceansBeachInfo1'
#         params = {'serviceKey': 'pC6KGxF2CQUBDiyG6fTy7G0w+Ajs0JVe9jj48Wgnbwu6leKdptIuf031/zh7sLvlgkVFFV7aDZbM5be150larA==', 'pageNo': '1', 'numOfRows': '20', 'SIDO_NM': city, 'resultType': 'JSON'}
#         response = requests.get(url, params=params)
#
#         result = json.loads(response.content.decode())['getOceansBeachInfo']['item']
#
#         for value in enumerate(result):
#             insert_DB = {
#                 "시도명" : value[1]['sido_nm'],
#                 "구군명" : value[1]['gugun_nm'],
#                 "정점명" : value[1]['sta_nm'],
#                 "모래" : value[1]['beach_knd'],
#                 "관련사이트" : value[1]['link_nm'],
#                 "해수욕장 비상연락처" : value[1]['link_tel'],
#                 "위도" : value[1]['lat'],
#                 "경도" : value[1]['lon']
#             }
#             check_sta_nm = db.beach.find_one({'정점명': value[1]['sta_nm']},{'_id':False})
#
#             if (check_sta_nm) :
#                 if (value[1]['sta_nm'] == check_sta_nm['정점명']) :
#                     break;
#             else :
#                 db.beach.insert_one(insert_DB)
#
#     return render_template("index.html")


@app.route('/', methods=["GET"])
def main():

    beach_list = list(db.beach.find({}, {'_id': False}))
    print(beach_list)
    rows = beach_list

    return render_template("index.html", rows=rows)

@app.route('/api/search', methods=['GET'])
def search():
    beach_list = list(db.beach.find({}, {'_id': False}))
    print(beach_list)
    return jsonify({'result' : 'success'}, {'msg' : 'DB 조회 완료'}, {'beach_list' : beach_list})

# @app.route('/detail/')
# def detail():
#     return render_template("detail.html")

@app.route('/detail/<keyword>')
def detail(keyword):
    beach_one = db.beach.find_one({'정점명': keyword})
    print(beach_one)
    return render_template("detail.html", word = keyword, beach_one = beach_one)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)