from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Flower(Base):
    __tablename__ = 'flower'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    word = Column(String)
    etc = Column(String)
    modelnum = Column(Integer)
    
class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    genre = Column(String)
    rdate = Column(String)
    lyrics = Column(String)
    enlyr = Column(String)
    preproc = Column(String)
    postproc = Column(String)
       
    