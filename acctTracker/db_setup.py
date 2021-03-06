import sys
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2


Base = declarative_base()


class Owner(Base):
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True, nullable=False)

    @property
    def serialize(self):
        return {
            'id':         self.id,
            'name':       self.name,
        }


class UserCred(Base):
    __tablename__ = 'usercred'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)

    @property
    def serialize(self):
        return {
            'id':          self.id,
            'email':       self.email,
        }


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    accountType = Column(String(10), nullable=False)
    institution = Column(String(25), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'accountType':    self.accountType,
            'institution':    self.institution,
        }


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    ticker = Column(String(8), nullable=False)
    exchange = Column(String(8), nullable=False)
    companyName = Column(String(50))
    industry = Column(String(30))
    description = Column(String(500))
    account_id = Column(Integer, ForeignKey('account.id'))
    account = relationship(Account)
    user_id = Column(Integer, ForeignKey('usercred.id'))
    usercred = relationship(UserCred)

    __table_args__ = (
        UniqueConstraint('ticker'),
    )

    @property
    def serialize(self):
        return {
            'id':            self.id,
            'ticker':        self.ticker,
            'exchange':      self.exchange,
            'companyName':   self.companyName,
            'industry':      self.industry,
            'description':   self.description,
        }


# For later functionality
# class Transaction(Base):
# 	id = Column(Integer, primary_key = True)
# 	costBasis = Column(Integer, nullable = False)
# 	shareCount = Column(Integer, nullable = False)
# 	account_id = Column(Integer, ForeignKey('acccount.id'))
# 	stock_id = Column(Integer, ForeignKey('stock.id'))
# 	account = relationship(Account) # the transaction occurs in one account
# 	stock = relationship(Stock) # the transaction occurs with one stock

#engine = create_engine('sqlite:///tracker_v2.db')
engine = create_engine('postgresql://catalog:catpass@localhost/catalog')

Base.metadata.create_all(engine)
