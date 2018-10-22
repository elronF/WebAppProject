from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Owner, Account, Stock

app = Flask(__name__)

engine = create_engine('sqlite:///tracker.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show all accounts
@app.route('/')
@app.route('/accounts/')
def showAccounts():
    accounts = session.query(Account).order_by(asc(Account.accountType))
    stocks = session.query(Stock).order_by(asc(Stock.account_id))
    return render_template('stocks.html', accounts=accounts, stocks=stocks)


# Show the contents of one account
@app.route('/accounts/<int:account_id>/')
def showOneAccount(account_id):
    accounts = session.query(Account).order_by(asc(Account.accountType))
    account = session.query(Account).filter_by(id=account_id).one()
    stocks = session.query(Stock).filter_by(account_id=account_id).all()
    return render_template('account.html', accounts=accounts, account=account, stocks=stocks)


# Show the details of one stock
@app.route('/accounts/<int:account_id>/<string:stock_ticker>/')
def showStockDetails(account_id, stock_ticker):
    stock = session.query(Stock).filter_by(ticker=stock_ticker).one()
    account = session.query(Account).filter_by(id=account_id).one()
    return("Hey there fella, something worked!")


if __name__ == '__main__':
    app.debug = True # server reloads each time there's a code change
    app.run(host = '0.0.0.0', port = 5000)