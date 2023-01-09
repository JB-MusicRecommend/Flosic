import threading
import time
import numpy as np
import cv2
import os
import tensorflow as tf
from flask import session
temp_dir_lock = threading.Lock()

flower_list = {'calla': 0,'camellia': 1,'canna': 2,'carnation': 3,'cosmos': 4,'cyclamen': 5,'daffodil': 6,'dandelion': 7,'dialia': 8,'erica': 9,'forget': 10,'forsythia': 11,'freesia': 12,'gerbera': 13,'gladiolus': 14,'hydrangea': 15,'lavender': 16,'lily': 17,'marigold': 18,'mum': 19,'pasque': 20,'phlox': 21,'poinsettia': 22,'poppy': 23,'ranunculus': 24,'rose': 25,'snapdragon': 26,'sunflower': 27,'tulip': 28}

def image_transfer(uploaded_file, session):
    session_id = session['id']
    temp_dir_lock.acquire()
    modified_dir_path = f'./static/uploaded/{session_id}/preimg'


    size=(256,256)
    base_pic=np.zeros((size[1],size[0],3),np.uint8)
    pic1 = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

    if pic1 is None:
        print('Image load failed')
    else:
        h,w=pic1.shape[:2]
        ash=size[1]/h
        asw=size[0]/w
    
        if asw<ash:
            sizeas=(int(w*asw),int(h*asw))
        else:
            sizeas=(int(w*ash),int(h*ash))
        
        pic1 = cv2.resize(pic1,dsize=sizeas)
        con = 0
    
        try: 
            base_pic[int(size[1]/2-sizeas[1]/2):int(size[1]/2+sizeas[1]/2),
            int(size[0]/2-sizeas[0]/2):int(size[0]/2+sizeas[0]/2),:]=pic1
            con = 0

        except:
            con = 1

        if(con == 0):
            timestamp = time.time()
            resize_img = os.path.join(modified_dir_path,f'{timestamp}.jpg')
            try:
                cv2.imwrite(resize_img, base_pic) 
                print("이미지 저장 성공")
            except Exception as e:
                print(f"이미지 저장 실패 : {e}")
            session['imgup'] = 'yes'
    temp_dir_lock.release()
    return resize_img


def upload_image(uploaded_file,session):
    
    if session['imgup'] == 'no':
        createdir(f'./static/uploaded/{session["id"]}/preimg')
        modified_img_path = image_transfer(uploaded_file, session)
    
    elif session['imgup'] == 'yes': 
        os.remove(session['dir'])
        modified_img_path = image_transfer(uploaded_file, session)

    
    if modified_img_path is not None:
        return modified_img_path
    else:
        return None

def createdir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as e:
        print(f"디렉토리 생성 실패 : {e}")

def predict_image(directory):
    dir = directory
    print(dir)
    model = tf.keras.models.load_model('./imagemodel_v1.h5')
    img_height, img_width, batch_size = 150, 150, 16
    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    
    test_ds = test_datagen.flow_from_directory\
    (
        dir,
        class_mode='categorical',
        target_size=(img_height, img_width),
        batch_size=batch_size
    )
    
    model.evaluate(test_ds)
    classes = model.predict(test_ds, batch_size=10)
    return np.argmax(classes)
    
    
