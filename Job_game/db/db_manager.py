import pymysql.cursors
import hashlib
import random
import string


class db_manager:
    def connect(self):
        return pymysql.connect(
            host="localhost",
            user="root",
            passwd="nakura8810",
            db="job_game",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
            )
    def exec_query(self, sql, params=()):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql,params)
                results = cursor.fetchall()
            conn.commit()
        return results

    def calc_pw_hash(self,pw,salt="".join(random.choices(string.ascii_letters, k=5))):
        pw_salt = (pw + salt).encode("UTF-8")
        hash_pw = hashlib.sha512(pw_salt).hexdigest()
        return hash_pw, salt