def CheckUserExistance(conn, uid):
    with conn.cursor() as cursor:
        sql = f"SELECT * FROM userinfo WHERE lineid='{uid}'"
        cursor.execute(sql)
    result_one = cursor.fetchone()
    if result_one is None:
        return False
    return True


def AddUserInfo(conn, uid):
    with conn.cursor() as cursor:
        sql = f'''INSERT INTO userinfo (lineid, latlong, service)
        VALUES('{uid}', 'None', 0)'''
        cursor.execute(sql)
    conn.commit()

def GetUserInfo(conn, uid, item):
    with conn.cursor() as cursor:
        sql = f"SELECT * FROM userinfo WHERE lineid='{uid}'"
        cursor.execute(sql)
    result = cursor.fetchone()
    result = result[item]
    return result

def UpdateUserInfo(conn, uid, item, change):
    with conn.cursor() as cursor:
        sql = f"UPDATE userinfo set {item} = '{change}' where lineid='{uid}'"
        cursor.execute(sql)
    conn.commit()


def DeleteUserInfo(conn, uid):
    with conn.cursor() as cursor:
        sql = f"DELETE FROM userinfo WHERE lineid='{uid}'"
        cursor.execute(sql)
    conn.commit()


def test_sql_health(conn):
    with conn.cursor() as cursor:
        sql = "select * from userinfo"
        cursor.execute(sql)
    return cursor.fetchone()
