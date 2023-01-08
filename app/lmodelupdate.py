import pandas as pd
import numpy as np
from konlpy.tag import Komoran 
from db_controller import read_song_tolist
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

from gensim.models.word2vec import Word2Vec
from gensim.models import Word2Vec

import db_controller as db





def generate_and_update_model():

    music = pd.DataFrame(db.read_song_tolist())
    print("음악 불러옴")
    komoran = Komoran()
    pos = music['lyrics'].apply(lambda x : komoran.pos(x))

    stop = []
    stop2 = ['테', '좆', '병신', '시발', '떼', '다리', '랩', '그지', '틀', '폭력', '개소리', '까', '자식', '녀석','짓', '코', '주먹', '되', '창', '사',
                '악', '판', '칼', '병', '여러분', '마찬가지', '박', '여', '명', '여기저기', '악마', '따', '곳도', '베', '꼴', '패', '결', '땡', '하하하',
                '당장', '겨', '가나', '칠', '혀', '에선', '미', '이래', '이이', '소주', '니들', '보니', '김', '장', '목이', '인해', '하리', '여태', '인지',
                '으', '그때', '존', '래', '투', '인마', '깡패', '황지', '버', '깡', '값', '얼', '티', '식', '두지', '폰', '진', '앤', '인가', '들', '린지',
                '인', '태', '벤', '침', '주', '벌레', '하', '걸', '쪼', '주네', '메', '나서', '룩', '임', '트', '빌', '수연', '따지', '포', '텐', '잇', '쑤',
                '누가', '낫', '드', '누구', '토이', '아양', '겨레', '칸', '와도', '세노', '게로', '자르', '린', '이다', '대만', '작']
    

    for i in pos:
        for word, tag in i:
            if tag in 'NNG' or tag in 'NNP' or tag in 'VV' or tag in 'VA' or tag in 'XR' or tag in 'NP' or tag in 'VX' or tag in 'XSN' or tag in 'XSA':
                continue
                #stopwords.append(word)
            else:
                stop.append(word)
    a = set(stop)
    stopwords = list(a)
    stopwords = stopwords + stop2

    print("불필요한 단어 제거")
    lyriceToken = []
    for i in pos:
        clean_words = [] 
        for word, tag in i: 
            if word not in stopwords:
                clean_words.append(word)
        lyriceToken.append(clean_words)
        #nouns[i] = ' '.join(clean_words).split()


    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lyriceToken)
    print("토큰화 완료")

    threshold = 3
    total_cnt = len(tokenizer.word_index) # 단어의 수
    rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
    total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
    rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

    # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
    for key, value in tokenizer.word_counts.items():
        total_freq = total_freq + value

        # 단어의 등장 빈도수가 threshold보다 작으면
        if(value < threshold):
            rare_cnt = rare_cnt + 1
            rare_freq = rare_freq + value

    print('단어 집합(vocabulary)의 크기 :',total_cnt)
    print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
    print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
    print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)


    # 전체 단어 개수 중 빈도수 2이하인 단어는 제거.
    # 0번 패딩 토큰을 고려하여 + 1
    vocab_size = total_cnt - rare_cnt + 1
    print('단어 집합의 크기 :',vocab_size)

    model = Word2Vec(sentences = lyriceToken, vector_size = 100, window = 5, min_count = 5, workers = 4, sg = 0)
    print("모델생성 완료")
    flowerlist = db.read_flower_tolist()
    print(flowerlist)

    sim = []
    for i in range(len(flowerlist)):
        sim.append(model.wv.most_similar(flowerlist[i]['word'], topn=20))
            
    simLf = []
    for i in sim:
        new = []
        for j, k in i:
            new.append(j)
        simLf.append(new)
    
    score = []
    for i in lyriceToken:
        new = [0 for i in range(len(simLf))] 
        for a, j in enumerate(simLf): # simLf[0]
            for k in j: # simLf[0][0]
                if k in i: #꽃말과 유사단어가 lyriceToken안에 있으면
                    new[a] += 1
        score.append(new)

    flowerLanguage = []
    for i in score:
        max = 0
        index = 0
        for j, k in enumerate(i):
            if k > max:
                max = k
                index = j
        flowerLanguage.append(flowerlist[index]['word'])
    print("꽃말 추출 완료")        
        #print(str(i) + ': ' + str(index) +'번째 ' + str(max) + '가 젤 높음')
        #print(languageOfFlower)
    music = pd.DataFrame(read_song_tolist())
    music['postproc'] = flowerLanguage
    songlist = music.to_dict(orient='records')

    print("데이터베이스에 저장")
    db.update_song_list(songlist)




