import pymysql

def insert_trans_log(oCode, tCode, oStr, tStc):
    # 차후 디비쪽 연결은 pooling이나 ORM방식을 이용하여 최대 동접에 대한 인정적인 처리를 구현한다
    # 현재는 그냥 요청하면 접속, 쿼리, 접속해제순으로 처리
    #해당 접속법은 임시적이다
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='12341234',
                                 db='py_db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    #예외처리 -> s/w는 죽으면 안된다(->오류가 발생할만한 잠재적인 요인을 가진 부분에는 모두다 예외처리를 수행)

    try:
        with connection.cursor() as cursor:
            # 쿼리문
            sql = '''
            INSERT INTO `py_db`.`tbl_trans_lang_log` (`oCode`, `tCode`, `oStr`, `tStc`) VALUES (%s,%s,%s,%s);
            '''
            #쿼리수행
            cursor.execute(sql, (oCode, tCode, oStr, tStc))

        #커밋수행(디비에 실제 반영)
        connection.commit()

    except Exception as e:
        print(e)
    finally:
        if connection:
            connection.close()
