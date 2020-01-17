#엔트리 포인트 : 진입로, 시작점, 모든 경로법은 엔트로부터 따진다
#1. 모듈 가져오기 start---------------------------------------------------
#플라스크 관련 모듈 가져오기
from flask import Flask, render_template, request, jsonify, redirect
#2. 테스트 모듈 가져오기
from ml.mod import *
#언어 감지 및 번역 모듈 가져오기
from ml import detect_lang as dl, transfer_lang
from ml import PI2
from db import logBackup
#1. 모듈 가져오기 end-------------------------------------------------------


#2. Flask 객체 생성

app=Flask(__name__)
#3. 라우팅
@app.route('/')
def home():
    text_str='''
    Bong Joon-ho (Korean: 봉준호, Korean pronunciation: [poːŋ tɕuːnho → poːŋdʑunɦo]; born September 14, 1969) is a South Korean film director and screenwriter. He garnered international acclaim for his second feature film Memories of Murder (2003), before achieving commercial success with his subsequent films The Host (2006) and Snowpiercer (2013), both of which are among the highest-grossing films of all time in South Korea.
    '''
    print(dl(text_str))

    return render_template('index.html')

#restful
@app.route('/bsgo',methods=['GET','POST'])
def bsgo():
    if request.method=='GET':
        return render_template('bsgo.html')
    else:
        #전달된 데이터 획득
        # print(request.form.get('o1'))
        oriTxt=request.form.get('o') #내용이 들어있고, 100글자 이상
        # print(request.form['o1']) #만약 키가 틀리면 오류를 발생한다
        #언어감지
        na_code, na_str = dl(oriTxt)
        if na_code: #예측 되었다
            res={
                'code':na_code,
                'code_str':na_str
            }
        else:
            res={
                'code':'0',
                'code_str':'언어 감지 실패'
            }
        #결과응답
        return jsonify(res)


#번역처리
@app.route('/transfer',methods=['POST'])
def transfer():
    #데이터 획득
    oriTxt=request.form.get('o')
    na=request.form.get('na')
    #번역
    res = transfer_lang(oriTxt, na)
    #로그처리
    tarlang=res['message']['result']['tarLangType']
    trans=res['message']['result']['translatedText']
    logBackup(na,tarlang,oriTxt,trans)
    #응답
    return jsonify(res)

#4. 서버 가동
if __name__=='__main__':
    app.run(debug=True)
else:
    print('작동 안됨')