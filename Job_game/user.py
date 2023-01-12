import datetime
from itertools import count
from select import select
from unittest import result
import random
import string
from flask import Flask, redirect, render_template, request, session, url_for
from requests import delete
from db import db_manager
from flask_mail import Mail, Message
import smtplib
from db.db_manager import db_manager
import random, string,requests


app = Flask(__name__)

app.secret_key = "".join(random.choices(string.ascii_letters, k=256))
mail = Mail(app)


# ------------------------------------------------
# スタート画面 あとで編集してください。/user/start.html
@app.route("/")
def start():
    return render_template("/user/start.html")

# ------------------------------------------------
# ユーザーログイン画面 u_log
@app.route("/u_log_page")
def u_log_page():
    return render_template("/user/u_login.html")

@app.route('/u_log',methods=["POST"])
def u_log():
    dbmg = db_manager()
    id = request.form.get("id")
    pw = request.form.get("pw")
    sql = "select * from user where id  = %s"
    result = dbmg.exec_query(sql,id)
    try:
        hash_pw , _ = dbmg.calc_pw_hash(pw,result[0]["salt"])
    except IndexError: # idpwともに一致していなかった時
        return render_template("/user/u_login.html",error="アカウントが見つかりませんでした。もう一度お試しください") 
    if hash_pw == result[0]["pw"]:   
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=60)
        # sessionの登録
        session['user_id'] = result[0]['id']
        return redirect("/tutorial_story")
    else:
        return render_template("/user/u_login.html",error2="パスワードまたは名前が違います。もう一度ログインし直してください")

# ---------------------------------------------------​
# ユーザー新規登録トップ画面 u_register
@app.route("/u_register_page")
def u_register_page():
    return render_template("/user/u_register.html")

@app.route("/u_register", methods=["POST"])
def u_register():
    id    = request.form.get("id")
    pw = request.form.get("pw")
    try:
        dbmg = db_manager()
        hash_pw, salt = dbmg.calc_pw_hash(pw)
        A = dbmg.exec_query("insert into user value(%s,%s,0,0,0,0,0,%s)",(id,hash_pw,salt))
        return redirect("/u_log_page")
    except:
        return render_template("/user/u_register.html",error="同じIDが登録されています。別の名前でお試しください")


# ユーザー新規登録確認画面 u_register_con
@app.route("/u_register_con", methods=["POST"])
def u_register_con():
    id    = request.form.get("id")
    pw = request.form.get("pw")
    return render_template("/user/u_register_con.html",id=id,pw=pw)

# -------------------------------------------------
# 就職活動案内画面　job_guidance
@app.route("/job_guidance")
def job_guidance():
    return render_template("/user/job_guidance.html")

# 就職活動案内画面　job_guidance
@app.route("/job_guidance_s_1")
def job_guidance_s_1():
    return render_template("/user/job_guidance_s_1.html")

# 就職活動案内画面　job_guidance
@app.route("/job_guidance_s_2")
def job_guidance_s_2():
    return render_template("/user/job_guidance_s_2.html")

# 就職活動案内画面　job_guidance
@app.route("/job_guidance_s_3")
def job_guidance_s_3():
    return render_template("/user/job_guidance_s_3.html")

@app.route("/job_guidance_s_4")
def job_guidance_s_4():
    return render_template("/user/job_guidance_s_4.html")

@app.route("/job_guidance_s_5")
def job_guidance_s_5():
    return render_template("/user/job_guidance_s_5.html")
    
# -------------------------------------------------
# ブラウザゲームトップ画面 gametop
@app.route("/gametop")
def gametop():
    return render_template("/user/gametop.html")

# -------------------------------------------------
# プロフィール画面　myprofile
@app.route("/myprofile")
def myprofile():

    id=session["user_id"]

    dbmg = db_manager()
    result =dbmg.exec_query("SELECT * FROM user where id = %s",id)

    return render_template("/user/myprofile.html",result=result)

# -------------a------------------------------------
# 個人情報編集画面　profile_edit
@app.route("/profile_edit_page")
def profile_edit_page():

    id=session["user_id"]

    dbmg = db_manager()
    result =dbmg.exec_query("SELECT * FROM user where id = %s",id)

    return render_template("/user/profile_edit.html",result=result,id=id)

# -------------------------------------------------
# 個人情報編集画面 処理　profile_edit処理
@app.route("/profile_edit", methods=["POST"])
def profile_edit():
    id=session["user_id"]
    pw=request.form.get("pw")

    dbmg = db_manager()
    hash_pw, salt = dbmg.calc_pw_hash(pw)
    sql = "UPDATE user SET pw=%s,salt=%s WHERE id = %s"
    dbmg.exec_query(sql,(hash_pw,salt,id))
    
    return redirect("/myprofile")


# -------------------------------------------------
# 個人情報編集確認画面  profile_edit_con
@app.route("/profile_edit_con", methods=["POST"])
def profile_edit_con():
    id=session["user_id"]
    pw=request.form.get("pw")

    return render_template("/user/profile_edit_con.html",id=id,pw=pw)

# -------------------------------------------------
# 就職対策トップ画面 findworktop
@app.route("/findworktop")
def findworktop():
    return render_template("/user/findworktop.html")

# -------------------------------------------------
# 筆記試験対策ステージ選択画面 fin_written
@app.route("/fin_written")
def fin_written():
    return render_template("/user/fin_written.html")

# -------------------------------------------------
# マップ一覧画面 map
@app.route("/main_map")
def main_map():
    session['quiz_count'] = 0
    return render_template("/user/main_map.html")

@app.route("/main_map_2")
def main_map_2():
    return render_template("/user/main_map_2.html")
# -----------------------------------------------


# -------------------------------------------------
# メインクイズ問題画面 表示 
@app.route("/main_quiz")
def main_quiz():
    dbmg = db_manager()
    user_id = session["user_id"]

    # session から 何問目かを取得
    count = int(session['quiz_count'])
    if count is None:
        count = 1
    else :
        count += 1
    
    # 3問目だったら終了
    if count > 3:
        return render_template("/user/main_map.html")    
    else:
        session['quiz_count'] = count

    # id ランダム
    c = dbmg.exec_query("select count(id) as id_count from quiz")
    id = int(c[0]["id_count"])
    
    ram = random.randint(2,id)
    result = dbmg.exec_query("select * from quiz where id=%s",ram)

    # 文字置き換え
    str = result[0]["quiz_image_id"]
    new_str = str.replace("¥","/")
    # print(new_str)

    quiz_id = result[0]["id"]

    # 文字付けたし
    new_str = "../static/images/quiz" + new_str
 
    return render_template("/user/main_quiz.html",
    result=result,quiz_id=quiz_id,new_str=new_str)

# main問題画面 処理 (回答)
@app.route("/kaitou_quiz_main")
def kaitou_quiz_main():
        quiz_id = request.args.get("quiz_id")
        user_id = session["user_id"]
        user_answer = request.args.get("q1")
        
        dbmg = db_manager()
        quiz = dbmg.exec_query("select * from quiz where id = %s",quiz_id)
        
        answer = quiz[0]["answer"]
        # print(user_answer)
        # print(answer)
        # print(type(user_answer))
        # print(type(answer))

        if int(user_answer) == answer:
            ox = "正解!!"
        else:
            ox = "不正解"
            # dbmg.exec_query("insert into review value(%s,%s)",(user_id,quiz_id))
        return render_template("/user/main_right.html",ox=ox,user_id=user_id,quiz=quiz)
# -------------------------------------------------
# 解説画面 画像表示
@app.route("/main_quiz_right", methods=["POST"])
def main_quiz_right():
    dbmg = db_manager()

    quiz_id = request.form.get("quiz_id")
    user_id = session["user_id"]
    
    # 解説表示の処理
    quiz = dbmg.exec_query("select * from quiz where id=%s",quiz_id)

    # 文字置き換え
        
    if quiz_id == quiz[0]["comment"]:
        str = quiz[0]["comment"]
        new_str = str.replace("¥","/")
        # print(new_str)
        # 文字付けたし
        new_str = "../static/images/Answer" + new_str
        return render_template("/user/main_right.html",new_str=new_str,user_id=user_id,quiz_id=quiz_id,quiz=quiz)
    else:
        return render_template("test.html")


# -------------------------------------------------
@app.route("/ministart")
def ministart():
    id=session["user_id"]
    session['now_s'] = 0

    dbmg = db_manager()
    result =dbmg.exec_query("SELECT * FROM user where id = %s",id)

    return render_template("/user/ministart.html",result=result)

# ミニゲーム クイズ画像表示画面 minigame_quiz
@app.route("/minigame_quiz_page")
def minigame_quiz_page():
    now_s = request.args.get("now_s")
    dbmg = db_manager()
    
    acount = int(session['now_s'])
    if acount is None:
        acount = 1
    else :
        acount += 1
    print(acount)

    # id ランダム
    c = dbmg.exec_query("select count(id) as id_count from quiz")
    id = int(c[0]["id_count"])

    ram = random.randint(2,id)
    results = dbmg.exec_query("select * from quiz where id=%s",ram)

    # 文字置き換え
    str = results[0]["quiz_image_id"]
    new_str = str.replace("¥","/")
    print(new_str)

    quiz_id = results[0]["id"]

    # 文字付けたし
    new_str = "static/images/quiz" + new_str
 
    return render_template("/user/minigame_quiz.html",results=results,new_str=new_str,now_s=now_s,quiz_id=quiz_id)

# -------------------------------------------------
# ミニゲーム 問題処理 画面 minigame_quiz
@app.route("/minigame_quiz")
def minigame():
    # now_s = 0
    now_s = session["now_s"]
    quiz_id = request.args.get("quiz_id")
    user_id = session["user_id"]
    user_answer = request.args.get("q1")

    dbmg = db_manager()
    quiz = dbmg.exec_query("select * from quiz where id=%s",quiz_id)
    
    answer=quiz[0]["answer"]

    # print(type(user_answer))
    # print(type(answer))

    if int(user_answer) == answer:
        ox = "正解!!"
        now_s = now_s + 10
        session["now_s"]=now_s
    else:
        ox = "不正解"
        print(now_s)

    
    return render_template("/user/minigame_right.html",ox=ox,user_id=user_id,quiz=quiz,now_s=now_s)

# -------------------------------------------------
# ミニゲーム 解説画像表示 画面 minigame_right_page
@app.route("/minigame_right_page",methods=["POST"])
def minigame_right_page():
    # now_s = request.form.get("now_s")
    user_id = session["user_id"]
    quiz_id = request.form.get("quiz_id")
    
    # 解説表示の処理
    dbmg = db_manager()
    quiz = dbmg.exec_query("select * from quiz where id=%s",quiz_id)
    # str = quiz[0]["answer"]

    # 文字置き換え
    if quiz_id == quiz[0]["comment"]:
        str = quiz[0]["comment"]
        new_str = str.replace("¥","/")
        # print(new_str)
        # 文字付けたし
        new_str = "../static/images/Answer" + new_str
        return render_template("/user/mimigame_right.html",new_str=new_str,user_id=user_id,quiz_id=quiz_id,quiz=quiz)
    else:
        return render_template("test.html")
    # new_str = str.replace("¥","/")
    # print(new_str)

    # 文字付けたし
    # new_str = "static/images/Answer" + new_str
 
    # return render_template("/user/minigame_right.html",new_str=new_str,user_id=user_id,now_s=now_s)

# -------------------------------------------------
# ミニゲーム 完了 画面 minigame_ok
@app.route("/minigame_ok",methods=["post"])
def minigame_ok():
    user_id=session["user_id"]
    now_s = session["now_s"]
    dbmg = db_manager()
    my_date = dbmg.exec_query("select * from user where id=%s",user_id)
    my_score = my_date[0]["score"]
    print(my_score)
    print(my_date)
    if my_score < now_s :
        sql = "update user set score = %s where id = %s"
        dbmg.exec_query(sql,(now_s,user_id))

    return render_template("/user/minigame_ok.html",now_s=now_s,my_score=my_score)
# -------------------------------------------------
#ランキング
@app.route("/ranking",methods=["POST"])
def ranking():
    dbmg = db_manager()
    score = dbmg.exec_query("SELECT * FROM user ORDER BY score DESC")

    return render_template("/user/ranking.html",score=score)

 


# ユーザーログアウト
@app.route("/u_logout")
def u_logout():
    if "user_id" in session:
        session.pop('user_id',None)
    session.clear()
    return redirect("/")


# JavaScript(チュートリアル)
@app.route("/tutorial_story")
def story():
    return render_template("/user/tutorial_story.html")


# お問い合わせ機能
# -------------------------------------------------
#お問い合わせ画面
@app.route("/u_inquiry")
def u_inquiry():
    return render_template("/user/u_inquiry.html")

# 掲示板機能
# -------------------------------------------------
# ここから掲示板～スレッドを表示する～
@app.route("/thread_page")
def thread_page():
    dbmg = db_manager()
    thread = dbmg.exec_query("select * from thread")
    return render_template("/user/thread.html", thread=thread)
# スレッドを立てる
@app.route("/thread")
def thread():
    user_id = session["user_id"]
    thread_name = request.args.get("thread_name")
    dbmg = db_manager()
    dbmg.exec_query("insert into thread (thread_name,user_id) value (%s,%s)", (thread_name,user_id))
    thread = dbmg.exec_query("select * from thread")
    ok="スレッドを作成しました。会話をお楽しみください！"
    return render_template("/user/thread.html", thread=thread,ok=ok)
# スレッドの中身に投稿する
@app.route("/board")
def board():
    name =session["user_id"]
    comment = request.args.get("comment")
    thread_id = request.args.get("thread_id")
    t_date=datetime.datetime.now()
    date =t_date.strftime("%Y/%m/%d %H:%M:%S")
    dbmg = db_manager()
    sql = "insert into board (thread_id,user_id,comment,date) value (%s,%s,%s,%s)"
    dbmg.exec_query(sql, (thread_id,name,comment,date))
    sql2 = "select * from board where thread_id=%s"
    comments = dbmg.exec_query(sql2, (thread_id))
    thread = dbmg.exec_query("select * from thread where thread_id=%s",thread_id)
    thread_name = thread[0]["thread_name"]
    user_id = thread[0]["user_id"]
    return render_template("/user/board.html", comments=comments,thread_id=thread_id)
# スレッドの中身を表示する
@app.route("/board_page",methods=["POST"])
def board_page():
    thread_id = request.form.get("thread_id")
    dbmg = db_manager()
    sql = "select * from board where thread_id=%s"
    comments = dbmg.exec_query(sql, (thread_id))
    thread = dbmg.exec_query("select * from thread where thread_id=%s",thread_id)
    thread_name = thread[0]["thread_name"]
    user_id = thread[0]["user_id"]
    return render_template("/user/board.html", comments=comments,thread_id=thread_id)
# 削除依頼<コメント>
@app.route("/u_board_comdelete_page",methods=["POST"])
def u_board_comdelete_page():
    comment_id = request.form.get("comment_id")
    dbmg = db_manager()
    comments = dbmg.exec_query("select * from board where comment_id=%s",comment_id)
    return render_template("/user/u_board_comdelete.html",comments=comments,comment_id=comment_id)
# 削除依頼<スレッド>
@app.route("/u_board_thrdelete_page",methods=["POST"])
def u_board_thrdelete_page():
    thread_id = request.form.get("thread_id")
    dbmg = db_manager()
    threads = dbmg.exec_query("select * from thread where thread_id=%s",thread_id)
    return render_template("/user/u_board_thrdelete.html",threads=threads,thread_id=thread_id)
#掲示板削除依頼画面<コメント>
@app.route("/u_board_comdelete", methods=["POST"])
def u_board_comdelete_b():
    comment_id = request.form.get("comment_id")
    reason = request.form.get("reason")
    dbmg = db_manager()
    com = dbmg.exec_query("select * from board where comment_id=%s",comment_id)
    date = com[0]["date"]
    user_id = com[0]["user_id"]
    comment = com[0]["comment"]
    thread_name = com[0]["thread_name"]
    sql = "insert into delete_board (date,user_id,comment,thread_name,reason) value (%s,%s,%s,%s,%s)"
    dbmg.exec_query(sql, (date,user_id,comment,thread_name,reason))
    return redirect("/thread_page")
#掲示板削除依頼画面<スレッド>
@app.route("/u_board_thrdelete", methods=["POST"])
def u_board_thrdelete_b():
    thread_id = request.form.get("thread_id")
    reason_2 = request.form.get("reason_2")
    dbmg = db_manager()
    com = dbmg.exec_query("select * from thread where thread_id=%s",thread_id)
    thread_name = com[0]["thread_name"]
    user_id = com[0]["user_id"]
    sql = "insert into delete_thread (thread_name,user_id,reason_2) value (%s,%s,%s)"
    dbmg.exec_query(sql, (thread_name,user_id,reason_2))
    return redirect("/thread_page")


# ↓↓ここから管理者機能↓↓




# 管理者ログイン機能機能
# -------------------------------------------------
# 管理者ログイン画面（TOP画面）
@app.route("/ad_log_page")
def ad_log_page():
    return render_template("/ad/ad_login.html")

@app.route('/ad_log',methods=["POST"])
def ad_log():
    dbmg = db_manager()
    id = request.form.get("id")
    pw = request.form.get("pw")
    sql = "select * from admin where id=%s and pw=%s"
    result = dbmg.exec_query(sql,(id,pw))
    if result != ():  
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=60)
        # sessionの登録
        session['admin_id'] = result[0]['id']
        return redirect("/adtop")
    else:
        return render_template("/ad/ad_login.html",error="パスワードまたは名前が違います。もう一度ログインし直してください")

# -------------------------------------------------
# 管理者トップ画面
@app.route("/adtop")
def adtop():
    return render_template("/ad/adtop.html")

# ここから追加-------------------------------------------------

@app.route("/reg_quiz_page")
def reg_quiz_page():
    return render_template("/ad/ad_quiz_register.html")

@app.route("/quiz_reg",methods=["POST"])
def reg_quiz():
    genre=request.form.get("genre")
    quiz_image = request.files['quiz_image']
    kaisetu_image = request.files["quiz_image2"]    
    level=request.form.get("level")
    right=request.form.get("right")
    importance=request.form.get("importance")
    dbmg = db_manager()

    if(genre=="" or quiz_image == "" or level=="" or
        right=="" or kaisetu_image=="" or importance==""):
        error="未入力欄があるからエラーだよ！"
        return render_template("/ad/ad_quiz_register.html",error=error)
    
    else:
        id =dbmg.exec_query("SELECT * FROM quiz ORDER BY id DESC LIMIT 1")
        nunber=id[0]["id"]
        nunber=int(nunber)+1
        image_name="\quiz_" + str(nunber) + ".png"
        image_kaisetu = "\Answer_" + str(nunber) + ".png"
# ファイルを保存するディレクトリを指定
        filepath1 = "static\images\quiz" + image_name
        filepath2 = "static\images\Answer" + image_kaisetu
# ファイルを保存する
        quiz_image.save(filepath1)
        kaisetu_image.save(filepath2)
        sql = "insert into quiz (genre,quiz_image_id,degree_d,degree_i,answer,comment) value (%s,%s,%s,%s,%s,%s)"
        dbmg.exec_query(sql,(genre,image_name,level,right,importance,image_kaisetu))
        error="登録できたよ！やったね！"
        return redirect("/adtop")

# ユーザー管理
@app.route("/user_management_page")
def user_management_page():
    dbmg = db_manager()
    result =dbmg.exec_query("SELECT * FROM user")
    return render_template("/ad/account_management.html",result=result)

# 検索表示
@app.route("/user_management_kensaku_page",methods=["POST"])
def user_management_kensaku_page():
    id = request.form.get("id")
    dbmg = db_manager()
    if id=="":
        result =dbmg.exec_query("SELECT * FROM user")
        m="検索項目が未入力です"
        return render_template("/ad/account_management.html",result=result,m=m)
    else :
        result =dbmg.exec_query("SELECT * FROM user whrer id = %s",id)
        m="検索結果"
        return render_template("/ad/account_management.html",result=result,m=m)

# ユーザー削除処理
@app.route("/ad_user_del",methods=["POST"])
def ad_user_del():
    id = request.form.get("id")
    dbmg = db_manager()
    dbmg.exec_query("DELETE FROM user WHERE id = %s",id)
    return redirect("/user_management_page")

#----------編集系の処理------------------------

# ユーザー編集画面表示
@app.route("/ad_account_edit_page",methods=["POST"])
def ad_acc_edit_con_page():
    id = request.form.get("id")
    dbmg = db_manager()
    result =dbmg.exec_query("SELECT * FROM user where id = %s",id)
    return render_template("/ad/acc_edit_con.html",result=result)

# ユーザー編集処理
@app.route("/ad_account_edit",methods=["POST"])
def ad_acc_edit_con():
    # ユーザー側からの編集方法はidをid=session["なんちゃら"]にするといいよ
    id=request.form.get("id")
    pw=request.form.get("pw")
    dbmg = db_manager()
    result = dbmg.exec_query("SELECT * FROM user where id = %s",id)
    if result[0]["pw"] != pw :
            sql = ('''
            UPDATE  user
            SET     pw = %s
            WHERE   id = %s
            ''')
    
            dbmg.exec_query(sql,(pw,id))
    return redirect("/user_management_page")

# 問題管理画面一覧表示
@app.route("/quiz_list")
def quiz_list():
    dbmg = db_manager()
    result = dbmg.exec_query("SELECT * FROM quiz")
    return render_template("/ad/quiz_management.html",result=result)

# クイズ削除処理
@app.route("/ad_quiz_del",methods=["POST"])
def ad_quiz_del():
    id = request.form.get("id")
    dbmg = db_manager()
    dbmg.exec_query("DELETE FROM quiz WHERE id = %s",id)
    return redirect("/quiz_list")
# 管理者ログアウト
@app.route("/ad_logout")
def ad_logout():
    if "admin_id" in session:
        session.pop('admin_id',None)
    session.clear()
    return redirect("/")

    




if __name__=="__main__":
    app.run(debug=True)

