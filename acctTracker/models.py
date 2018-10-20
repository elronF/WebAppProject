from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db_setup import Base

class Account(Base):
    __tablename__ = 'account'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    owner = Column(String(50), nullable = False)

class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key = True)
    ticker = Column(String(8), nullable = False)
    exchange = Column(String(8), nullable = False)
    companyName = Column(String(50))
    industry = Column(String(30))
    account_id = Column(Integer, ForeignKey('account.id'))
    account = relationship(account)