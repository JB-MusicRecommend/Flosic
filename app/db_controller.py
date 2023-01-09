from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import load_only
from sqlalchemy.sql.expression import null
from db_config import db_url
from db_model import Flower, Song
from flask import request
import codecs,csv
import random

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


def reset_ai(table):
    conn = engine.connect()
    
    query = 'SET @count=0;'
    conn.execute(text(query))

    
    query = f'UPDATE {table} SET id=@count:=@count+1;'
    conn.execute(text(query))

    
    result = conn.execute(f"SELECT MAX(id) FROM {table}")
    max_id = result.fetchone()[0]


    query = f"ALTER TABLE {table} AUTO_INCREMENT = {max_id}"
    conn.execute(query)

    conn.close()

def update_song_list(song_list):
    
    db = Session()
    db.query(Song).delete()
    db.commit()

    for song in song_list:
        object = Song(title = song['title'], artist = song['artist'], genre = song['genre'], rdate = song['rdate'], lyrics = song['lyrics'], enlyr = song['enlyr'], preproc = song['preproc'], postproc = song['postproc'])
        db.add(object)
    db.commit()
    reset_ai('song')
    db.close()



def recieve_csv_tolist():
    song_list = []
    csv_file = request.files['csv'].stream
    try:
        stream = codecs.iterdecode(csv_file, 'utf-8')

        reader = csv.reader(stream, dialect=csv.excel)
        
        for row in reader:

            title = row[0]
            artist = row[1]
            genre = row[2]
            rdate = row[3]
            lyrics = row[4]
            enlyr = row[5]
            if enlyr == '':
                enlyr = None
            song = {
                    'title' : title,
                    'artist' : artist,
                    'genre' : genre,
                    'rdate' : rdate,
                    'lyrics' : lyrics,
                    'enlyr' : enlyr,
                    'preproc' : None,
                    'postproc' : None
                    } 
            song_list.append(song)
        del song_list[0]
    except Exception as e:
        print(e)
        return None
    return song_list

def read_flower_tolist():
    db = Session()
    flower_list = []
    for flower in db.query(Flower).all():
        id = flower.id-1
        name = flower.name
        word = flower.word
        etc = flower.etc
        modelnum = flower.modelnum
        flower_list.append({'id':id, 'name':name, 'word':word , 'etc':etc, 'modelnum':modelnum})
    db.close()
    return flower_list
def add_flower(name, word, etc, modelnum):
    db = Session()
    flower = Flower(name=name, word=word , etc=etc, modelnum=modelnum)
    db.add(flower)
    db.commit()
    db.close()
def update_flower(name, word):
    db = Session()
    flower = db.query(Flower).filter(Flower.name == name).first()
    flower.word = word
    db.commit()
    db.close()
def delete_flower(id):
    db = Session()
    flower = db.query(Flower).filter(Flower.id == id).first()
    db.delete(flower)
    db.commit()
    db.close()
    
def find_flower_as_modelnum(modelnum):
    db = Session()
    flower = db.query(Flower).filter(Flower.modelnum == modelnum).first()
    db.close()
    return flower

def read_matched_song_list(flower):
    db = Session()
    song_list = []

    query = (
        db.query(Song)
        .options(load_only("id", "title", "artist", "genre", "rdate", "lyrics", "enlyr", "preproc", "postproc"))
        .filter(Song.postproc.like(f"%{flower['word']}%"))
    )

    for song in query.all():
        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'rdate': song.rdate,
            'lyrics': song.lyrics,
            'enlyr': song.enlyr,
            'preproc': song.preproc,
            'postproc': song.postproc,
        }    
        song_list.append(song_dict)
    db.close()

    while len(song_list) > 5:
        a = random.randint(0, len(song_list)-1)
        song_list.pop(a)
    

    return song_list
    
def read_song_tolist():
    db = Session()
    song_list = []
    for song in db.query(Song).all():
        id = song.id
        title = song.title
        artist = song.artist
        genre = song.genre
        rdate = song.rdate
        lyrics = song.lyrics
        enlyr = song.enlyr
        preproc = song.preproc
        postproc = song.postproc
        song_list.append({'id':id, 'title':title, 'artist':artist, 'genre':genre, 'rdate':rdate, 'lyrics':lyrics, 'enlyr':enlyr, 'preproc':preproc, 'postproc':postproc})
        db.close()
    return song_list
def add_songlist(song_list):
    db = Session()
    for song in song_list:
        try:
            if db.query(Song).filter(Song.title == song['title']).filter(song.artist == song['artist']).first() is not None:
                continue
        except:
            pass
        
        title = song['title']
        artist = song['artist']
        genre = song['genre']
        rdate = song['rdate']
        lyrics = song['lyrics']
        enlyr = song['enlyr']
        if enlyr == '':
            enlyr = null()
        postproc = null()
        preproc = null()

        song = Song(title=title, artist=artist, genre=genre, rdate=rdate, lyrics=lyrics , enlyr=enlyr, preproc=preproc, postproc=postproc)
        db.add(song)
    db.commit()
    db.close()
def delete_song(id):
    db = Session()
    song = db.query(Song).filter(Song.id == id).first()
    db.delete(song)
    db.commit()
    db.close()
    






