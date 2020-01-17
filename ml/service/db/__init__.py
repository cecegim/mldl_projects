import pymysql

def logBackup(oCode, tCode, oStr, tStc):
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
        print('잘들어갔다')
    except Exception as e:
        print(e)
    finally:
        if connection:
            connection.close()