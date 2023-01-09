from flask import Flask, render_template, request, redirect, session
import db_controller as db
import sessionfeature as ssft
import img_controller as imgctr
import os
import lmodelupdate as lmdupdate
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'flosic'

@app.route("/")
@app.route("/home")
def home():
    if 'auth' not in session:
        ssft.create_session()
    else:
        ssft.delete_session()
        ssft.create_session()

    return render_template('main/index.html')

@app.route('/selectsong')
def selectsong():
    return render_template('main/selectsong.html')

@app.route('/recommended<int:id>')
def recommended(id):
    flowerlist = db.read_flower_tolist()

    flower = flowerlist[id]
    flower['id'] = flower['id'] - 1
    if flower['etc'] == None:
        flower['etc'] = '없음'
    song_list= db.read_matched_song_list(flower)

    return render_template('main/recommended.html', song_list = song_list, flower = flower)




@app.route("/adminlogin", methods=['GET', 'POST'])
def admlogin():       
    if request.method == 'POST':
        if request.form['auth'] == 'admin1234':
            session['auth'] = request.form['auth']
            return redirect('/songindex/')
    
    return render_template('main/adminlogin.html')


@app.route('/adminlogout')
def logout():
    ssft.delete_session()
    return redirect('/')


@app.route("/songindex/")
def songindex():   
    if session['auth'] == 'admin1234':
        return render_template('main/songindex.html', song_list = db.read_song_tolist(), session = session)
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
    if session['auth'] == 'admin1234':
        return render_template('main/flowerindex.html',flower_list = db.read_flower_tolist())
    else:
        return redirect('/adminlogin') 
    

@app.route("/addflower/", methods=['GET', 'POST'])
def addflower():   
    if request.method == 'POST':
        db.add_flower(request.form['name'], request.form['word'] , request.form['etc'], request.form['modelnum'])
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

@app.route("/uploadimage", methods=['GET', 'POST'])
def uploadimage():   
    if request.method == 'POST':
        image = request.files['image']
        modified_dir_path = imgctr.upload_image(image,session)
        session['dir'] = modified_dir_path

    return redirect('/predictimage')

@app.route("/predictimage")
def predictimage():
    if session['dir'] is not None:
        if os.path.exists(session['dir']):
            dir = os.path.dirname(os.path.dirname(session['dir']))    
            predicted_number = imgctr.predict_image(dir)
            flower = db.find_flower_as_modelnum(predicted_number)
            num = flower['id']     
            url = '/predicted' +  str(num)
            return redirect(url)
        
@app.route('/predicted<int:id>')
def predited(id):
    flowerlist = db.read_flower_tolist()
    flower = flowerlist[id]
    flower['id'] = flower['id'] - 1
    if flower['etc'] == None:
        flower['etc'] = '없음'
    song_list= db.read_matched_song_list(flower)

    return render_template('main/predicted.html', song_list = song_list, flower = flower)

@app.route("/gnumodel")
def gnsmodel():
    lmdupdate.generate_and_update_model()
    return redirect('/songindex/')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    

