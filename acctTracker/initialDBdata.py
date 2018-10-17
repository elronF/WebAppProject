from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///tracker.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Data first owner

owner1 = Owner(name="Gary")

session.add(owner1)
session.commit()

account1 = Account(accountType="RRSP", institution="RBC", owner_name=owner1.name)
account2 = Account(accountType="TFSA", institution="RBC", owner_name=owner1.name)
account3 = Account(accountType="NonReg", institution="RBC", owner_name=owner1.name)

session.add(account1, account2, account3)
session.commit()

stock1 = Stock(ticker="CJ", exchange="TSX", companyName="Cardinal Energy", industry="Energy", description="Medium sized oil and gas company with assets in Canada", account=account1)
stock2 = Stock(ticker="GOOG", exchange="NYSE", companyName="Alphabet Inc.", industry="Technology", description="An American multinational conglomerate headquartered in Mountain View, California.", account=account2)
stock3 = Stock(ticker="ACB", exchange="TSX", companyName="Aurora Cannabis", industry="Cannabis", description="Major Canadian cannabis producer with operations focused in Alberta", account=account3)

session.add(stock1, stock2, stock3)
session.commit()

# Data second owner
owner2 = Owner(name="Gerry")

session.add(owner2)
session.commit()

account1 = Account(accountType="RRSP", institution="TD", owner_name=owner2.name)
account2 = Account(accountType="TFSA", institution="BMO", owner_name=owner2.name)
account3 = Account(accountType="NonReg", institution="Questrade", owner_name=owner2.name)

session.add(account1, account2, account3)

stock1 = Stock(ticker="TOU", exchange="TSX", companyName="Tourmaline Oil and Gas", industry="Energy", description="Large cap natural gas producer with assets in Alberta and BC", account=account1)
stock2 = Stock(ticker="WEED", exchange="TSX", companyName="Canopy Growth.", industry="Cannabis", description="Major Canadian cannabis producer with operations focused in Ontario", account=account2)
stock3 = Stock(ticker="FAKE", exchange="TSX", companyName="Fake Corp.", industry="Stuff", description="A real company doing real things", account=account3)

session.add(stock1, stock2, stock3)
session.commit()

# Data third owner
owner3 = Owner(name="Larry")

session.add(owner3)
session.commit()

account1 = Account(accountType="RESP", institution="CIBC", owner_name=owner3.name)
account2 = Account(accountType="TFSA", institution="Questrade", owner_name=owner3.name)

session.add(account1, account2)
session.commit()

stock1 = Stock(ticker="ATVI", exchange="NYSE", companyName="Activision Blizzard Inc.", industry="Entertainment", description="An American video game holding company based in Santa Monica, California", account=account1)
stock2 = Stock(ticker="FB", exchange="NYSE", companyName="Facebook Inc.", industry="Technology", description="An American online social media and social networking service company based in Menlo Park, California", account=account2)
stock3 = Stock(ticker="AAPL", exchange="NYSE", companyName="Apple Inc.", industry="Technology", description="An American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services.", account=account2)

session.add(stock1, stock2, stock3)
session.commit()

print("Added owners, accounts and stocks!")