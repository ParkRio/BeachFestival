import math

import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

from pymongo import MongoClient

import certifi
ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.3cgedw6.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'


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
    board = db.beach
    # 페이지값 (디폴트 = 1)
    page = request.args.get("page", 1, type=int)
    # 한 페이지 당 몇 개의 게시물을 출력할 것인가
    limit = 15

    datas = list(board.find({}).sort("_id", -1).skip((page - 1) * limit).limit(limit))

    # 게시글의 총 개수 세기 / 현재 51개 나옴 OK
    tot_count = board.count_documents({})
    # 마지막 페이지의 수 구하기 / 지금은 마지막 페이지 4임
    last_page_num = math.ceil(tot_count / limit)

    # 페이지 블럭을 4개 표기
    block_size = 3
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    print(block_num)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start=6 )
    block_start = (block_size * block_num) + 1
    print(block_start)
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)
    print(block_end)

    #########
    beach_list = list(db.beach.find({}, {'_id': False}))
    print(beach_list)
    rows = beach_list

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user=user_info, rows=rows, datas=datas, limit=limit, page=page, block_start=block_start, block_end=block_end, last_page_num=last_page_num)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("home", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("home", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/home')
def home():
    board = db.beach
    # 페이지값 (디폴트 = 1)
    page = request.args.get("page", 1, type=int)
    # 한 페이지 당 몇 개의 게시물을 출력할 것인가
    limit = 15

    datas = list(board.find({}).sort("_id", -1).skip((page - 1) * limit).limit(limit))

    # 게시글의 총 개수 세기 / 현재 51개 나옴 OK
    tot_count = board.count_documents({})
    # 마지막 페이지의 수 구하기 / 지금은 마지막 페이지 4임
    last_page_num = math.ceil(tot_count / limit)

    # 페이지 블럭을 4개 표기
    block_size = 3
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    print(block_num)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start=6 )
    block_start = (block_size * block_num) + 1
    print(block_start)
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)
    print(block_end)

    ######

    beach_list = list(db.beach.find({}, {'_id': False}))
    print(beach_list)
    rows = beach_list
    msg = request.args.get("msg")
    return render_template('index.html', rows=rows, datas=datas, limit=limit, page=page, block_start=block_start, block_end=block_end, last_page_num=last_page_num)

@app.route('/detail/posting')
def detail_posting():
    beach_list = list(db.beach.find({}, {'_id': False}))
    print(beach_list)
    rows = beach_list
    msg = request.args.get("msg")
    return render_template('detail.html', rows=rows, msg=msg)

@app.route('/login')
def login():
    board = db.beach
    # 페이지값 (디폴트 = 1)
    page = request.args.get("page", 1, type=int)
    # 한 페이지 당 몇 개의 게시물을 출력할 것인가
    limit = 15

    datas = list(board.find({}).sort("_id", -1).skip((page - 1) * limit).limit(limit))

    # 게시글의 총 개수 세기 / 현재 51개 나옴 OK
    tot_count = board.count_documents({})
    # 마지막 페이지의 수 구하기 / 지금은 마지막 페이지 4임
    last_page_num = math.ceil(tot_count / limit)

    # 페이지 블럭을 4개 표기
    block_size = 3
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    print(block_num)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start=6 )
    block_start = (block_size * block_num) + 1
    print(block_start)
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)
    print(block_end)

    ######

    beach_list = list(db.beach.find({}, {'_id': False}))
    print(beach_list)
    rows = beach_list
    msg = request.args.get("msg")
    return render_template('index.html', rows=rows, msg=msg, datas=datas, limit=limit, page=page, block_start=block_start, block_end=block_end, last_page_num=last_page_num)

@app.route('/api/search', methods=['GET'])
def search():
    beach_list = list(db.beach.find({}, {'_id': False}))
    print(beach_list)
    return jsonify({'result': 'success'}, {'msg': 'DB 조회 완료'}, {'beach_list': beach_list})


# @app.route('/detail/')
# def detail():
#     return render_template("detail.html")

@app.route('/detail/<keyword>')
def detail(keyword):
    beach_one = db.beach.find_one({'정점명': keyword})

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template("detail.html", word=keyword, beach_one=beach_one, user_info=user_info)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="해변 상세정보를 보기 위해선 로그인 해주시기 바랍니다."))


@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        comment_receive = request.form["comment_give"]
        date_receive = request.form["date_give"]
        url_receive = request.form["url_give"]
        doc = {
            "username": user_info["username"],
            "profile_name": user_info["profile_name"],
            "profile_pic_real": user_info["profile_pic_real"],
            "comment": comment_receive,
            "date": date_receive,
            "url": url_receive
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("detail_posting"))


@app.route("/get_posts", methods=['POST'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    url_receive = request.form["url_give"]
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        posts = list(db.posts.find({"url":url_receive}).sort("date", -1).limit(20))
        for post in posts:
            post["_id"] = str(post["_id"])
            post["count_heart"] = db.likes.count_documents({"post_id": post["_id"], "type": "heart"})
            post["heart_by_me"] = bool(db.likes.find_one({"post_id": post["_id"], "type": "heart", "username": payload['id']}))
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "posts": posts})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("detail_posting"))


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 좋아요 수 변경
        user_info = db.users.find_one({"username": payload["id"]})
        post_id_receive = request.form["post_id_give"]
        type_receive = request.form["type_give"]
        action_receive = request.form["action_give"]
        doc = {
            "post_id": post_id_receive,
            "username": user_info["username"],
            "type": type_receive
        }
        if action_receive == "like":
            db.likes.insert_one(doc)
        else:
            db.likes.delete_one(doc)
        count = db.likes.count_documents({"post_id": post_id_receive, "type": type_receive})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        name_receive = request.form["name_give"]
        about_receive = request.form["about_give"]
        new_doc = {
            "profile_name": name_receive,
            "profile_info": about_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{username}.{extension}"
            file.save("./static/"+file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.users.update_one({'username': payload['id']}, {'$set':new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)