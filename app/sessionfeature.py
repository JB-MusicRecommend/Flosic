from flask import session
import time
import os, shutil

def create_session():
    timestamp = time.time()
    session['id'] = str(timestamp)
    session['auth'] = 'none'
    session['imgup'] = 'no'
    session['dir'] = 'none'
    session['preimg'] = 'none'

def delete_session():
    delete_files_dir()
    session.pop('id', None)
    session.pop('auth', None)
    session.pop('imgup', None)
    session.pop('dir', None)
    session.pop('preimg', None)

def delete_files_dir():
    path = './static/uploaded/'+session['id']
    if os.path.exists(path):
        shutil.rmtree(path)

    