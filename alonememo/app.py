from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbtest

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/bi/mi/basic.naver?code=171539', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

global cnt
cnt = 0

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['GET'])
def listing():
    articles = list(db.test.find({},{'_id':False}))
    return jsonify({'all_articles': articles})



## API 역할을 하는 부분
@app.route('/memo/insert', methods=['POST'])
def saving():
    doc = {
        'comment': "  안녕하세요. 케이론입니다!오늘 리뷰할 영화는그린 북입니다.지극히 개인적인 몇 줄 평<그린 북>은 2018 토론토국제영화제 관객상 수상과다가오는 골든 글로브 시상식에서감독상, 남우주연상 등 5개 부문 노미네이트는 물론크리틱...",
        'image': "https://movie-phinf.pstatic.net/20190115_228/1547528180168jgEP7_JPEG/movie_image.jpg?type=m665_443_2",
        'desc': "1962년 미국, 입담과 주먹만 믿고 살아가던 토니 발레롱가(비고 모텐슨)는 교양과 우아함 그 자체인천재...",
        'url': "https://movie.naver.com/movie/bi/mi/basic.nhn?code=171539",
        'title': "그린 북"
    }
    db.test.insert_one(doc)

    return jsonify({'msg': '저장이 완료되었습니다.'})


@app.route('/memo/delete', methods=['POST'])
def deleting():
    db.test.delete_one({'title':'그린 북'})

    return jsonify({'msg': '삭제 완료되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
