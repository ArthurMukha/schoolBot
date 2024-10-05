from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.sqlite import JSON

class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    teamName = Column(String(50))
    # image = Column(String(int), nullable=True)

    def to_json(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id
        }

class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    teamName = mapped_column(ForeignKey("user.teamName"))
    score = Column(Integer)
    lastPointTime = Column(Integer)
    compound = Column(JSON)
    status = Column(String(50))
    ex_num = Column(Integer)
    ex_1 = Column(Boolean)
    ex_2 = Column(Boolean)
    ex_3 = Column(Boolean)
    ex_4 = Column(Boolean)
    ex_5 = Column(Boolean)
    ex_6 = Column(Boolean)


    def to_json(self):
        return {
            "id" : self.id,
            "teamName" : self.teamName,
            "score" : self.score,
            "lastPointTime" : self.lastPointTime,
            "compound" : self.compound,
            "status" : self.status,
            "ex_num" : self.ex_num,
            "ex_1" : self.ex_1,
            "ex_2": self.ex_2,
            "ex_3": self.ex_3,
            "ex_4": self.ex_4,
            "ex_5": self.ex_5,
            "ex_6": self.ex_6
        }

engine = create_engine('sqlite:///database.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, autoflush=True)
session = Session()

session.close()

def createFirstData():
    pass