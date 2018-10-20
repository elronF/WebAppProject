from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Owner, Account, Stock, Base

engine = create_engine('sqlite:///tracker.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Data first owner

owner1 = Owner(name="Logan")

session.add(owner1)
session.commit()

account1 = Account(accountType="RRSP", institution="RBC", owner_name=owner1.name)
account2 = Account(accountType="TFSA", institution="Questrade", owner_name=owner1.name)
account3 = Account(accountType="NonReg", institution="TD", owner_name=owner1.name)
account4 = Account(accountType="Trust", institution="Questrade", owner_name=owner1.name)
account5 = Account(accountType="RESP", institution="RBC", owner_name=owner1.name)

session.add(account1)
session.add(account2)
session.add(account3)
session.add(account4)
session.add(account5)
session.commit()

stock1 = Stock(ticker="CJ", exchange="TSX", companyName="Cardinal Energy", industry="Energy", description="Medium sized oil and gas company with assets in Canada", account=account1)
stock2 = Stock(ticker="GOOG", exchange="NYSE", companyName="Alphabet Inc.", industry="Technology", description="An American multinational conglomerate headquartered in Mountain View, California.", account=account1)
stock3 = Stock(ticker="ACB", exchange="TSX", companyName="Aurora Cannabis", industry="Cannabis", description="Major Canadian cannabis producer with operations focused in Alberta", account=account2)
stock4 = Stock(ticker="TOU", exchange="TSX", companyName="Tourmaline Oil and Gas", industry="Energy", description="Large cap natural gas producer with assets in Alberta and BC", account=account2)
stock5 = Stock(ticker="WEED", exchange="TSX", companyName="Canopy Growth.", industry="Cannabis", description="Major Canadian cannabis producer with operations focused in Ontario", account=account3)
stock6 = Stock(ticker="FAKE", exchange="TSX", companyName="Fake Corp.", industry="Stuff", description="A real company doing real things", account=account3)
stock7 = Stock(ticker="ATVI", exchange="NYSE", companyName="Activision Blizzard Inc.", industry="Entertainment", description="An American video game holding company based in Santa Monica, California", account=account4)
stock8 = Stock(ticker="FB", exchange="NYSE", companyName="Facebook Inc.", industry="Technology", description="An American online social media and social networking service company based in Menlo Park, California", account=account4)
stock9 = Stock(ticker="AAPL", exchange="NYSE", companyName="Apple Inc.", industry="Technology", description="An American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services.", account=account5)

session.add(stock1)
session.add(stock2)
session.add(stock3)
session.add(stock4)
session.add(stock5)
session.add(stock6)
session.add(stock7)
session.add(stock8)
session.add(stock9)
session.commit()

print("Added owner, accounts and stocks!")