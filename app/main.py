from flask import Flask, render_template, request, redirect, session
import db_controller as db

app = Flask(__name__)
app.secret_key = 'sk'

 
@app.route("/")
@app.route("/home")
def home():
    if 'id' not in session:
        session['id'] = None
    return render_template('main/index.html')

@app.route("/adminlogin", methods=['GET', 'POST'])
def admlogin():
    if 'id' not in session:
        session['id'] = None
    if request.method == 'POST':
            session['id'] = request.form['id']
    if session['id'] == 'admin1234':
        return redirect('/songindex/')
    else:
        return render_template('main/adminlogin.html')


@app.route('/adminlogout')
def logout():
    session.pop('id', None)
    return redirect('/adminlogin')


@app.route("/songindex/")
def songindex():   
    if session['id'] == 'admin1234':
        return render_template('main/songindex.html', song_list = db.read_song_tolist())
    else:
        return redirect('/adminlogin')  

@app.route("/addsong", methods=['GET', 'POST'])
def addsong():   
    if request.method == 'POST':
        song_list = db.recieve_csv_tolist()
    if song_list is not None:
        db.add_songlist(song_list)
    else :
        print("song_list is None")
        
    return redirect('/songindex/')

@app.route("/deletesong/<int:id>", methods=['GET', 'POST'])
def deletesong(id):
    if request.method == 'POST':
        db.delete_song(id) 
    
    return redirect('/songindex/')

@app.route("/flowerindex/")
def flowerindex():
    if session['id'] == 'admin1234':
        return render_template('main/flowerindex.html',flower_list = db.read_flower_tolist())
    else:
        return redirect('/adminlogin') 
    

@app.route("/addflower/", methods=['GET', 'POST'])
def addflower():   
    if request.method == 'POST':
        db.add_flower(request.form['name'], request.form['word'] , request.form['etc'])
    return redirect('/flowerindex/')

@app.route("/deleteflower/<int:id>", methods=['GET', 'POST'])
def deleteflower(id):
    if request.method == 'POST':
        db.delete_flower(id)     
    return redirect('/flowerindex/')

@app.route("/resetaisong")
def resetaisong():
    db.reset_ai("song")
    return redirect('/songindex/')

@app.route("/resetaiflower")
def resetaiflower():
    db.reset_ai("flower")
    return redirect('/flowerindex/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    



# 추가할 모듈이 있다면 추가
# config 파일이 있다면 추가
 
# 앞으로 새로운 폴더를 만들어서 파일을 추가할 예정임
# from app.main.[파일 이름] --> app 폴더 아래에 main 폴더 아래에 [파일 이름].py 를 import 한 것임
 
# 위에서 추가한 파일을 연동해주는 역할
# app.register_blueprint(추가한 파일)
