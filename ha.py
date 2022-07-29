from config import *  # noqa: F401, F403
import pymysql


def DeleteUserInfo(conn, uid):
    with conn.cursor() as cursor:
        sql = f"DELETE FROM userinfo WHERE lineid='{uid}'"
        cursor.execute(sql)
    conn.commit()


connection = pymysql.connect(
    host="us-cdbr-east-05.cleardb.net",
    user="b5f2e205874506",
    password="3291697e",
    db="heroku_b2cccf87a825db4",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
user_id = 'Uc10a26bd60f68b67b4db78d4ee14b8d2'
DeleteUserInfo(connection, user_id)
