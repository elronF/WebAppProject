from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Owner, Account, Stock
import json

app = Flask(__name__)

engine = create_engine('sqlite:///tracker.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Routes that do not require login
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


# Routes that require login
# Create item
@app.route('/accounts/<int:account_id>/stock/create/', methods=['GET', 'POST'])
def newStock(account_id):
    accounts = session.query(Account).order_by(asc(Account.accountType))
    account = session.query(Account).filter_by(id=account_id).one()
    if request.method == 'POST':
        newStock = Stock(companyName=request.form['companyName'], ticker=request.form['ticker'], exchange=request.form['exchange'], industry=request.form['industry'], description=request.form['description'], account_id=account_id)
        session.add(newStock)
        flash('{} has been added to your {} account'.format(newStock.companyName, account.accountType))
        session.commit()
        return redirect(url_for('showOneAccount', account_id=account_id))
    else:
        return render_template('createstock.html', accounts=accounts, account_id=account_id)


# Edit stock
@app.route('/accounts/<int:account_id>/<string:stock_ticker>/update/', methods=['GET', 'POST'])
def editStock(account_id, stock_ticker):
    accounts = session.query(Account).order_by(asc(Account.accountType))
    account = session.query(Account).filter_by(id=account_id).one()
    updatedStock = session.query(Stock).filter_by(ticker=stock_ticker).one()
    if request.method == 'POST':
        if request.form['companyName']:
            updatedStock.companyName = request.form['companyName']
        if request.form['ticker']:
            updatedStock.ticker = request.form['ticker']
        if request.form['exchange']:
            updatedStock.exchange = request.form['exchange']
        if request.form['industry']:
            updatedStock.industry = request.form['industry']
        if request.form['description']:
            updatedStock.description = request.form['description']
        session.add(updatedStock)
        flash('{} has been updated'.format(updatedStock.companyName))
        session.commit()
        # add flashing here
        return redirect(url_for('showOneAccount', account_id=account_id))
    else:
        return render_template('editstock.html', accounts=accounts, account=account, stock=updatedStock)


# Delete stock
@app.route('/accounts/<int:account_id>/<string:stock_ticker>/delete/', methods=['GET', 'POST'])
def deleteStock(account_id, stock_ticker):
    account = session.query(Account).filter_by(id=account_id).one()
    deleteStock = session.query(Stock).filter_by(ticker=stock_ticker).one()
    session.delete(deleteStock)
    flash('{} has been deleted'.format(deleteStock.companyName))
    session.commit()
    # add flashing here
    return redirect(url_for('showOneAccount', account_id=account_id))
    

# JSON endpoints 
# Show all accounts (JSON)
@app.route('/accounts/JSON/')
def accountsJSON():
    accounts = session.query(Account).all()
    return jsonify(accounts=[a.serialize for a in accounts])


# Show stock information (JSON)
@app.route('/accounts/<int:account_id>/<string:stock_ticker>/JSON/')
def stockJSON(account_id, stock_ticker):
    stock = session.query(Stock).filter_by(ticker=stock_ticker).one()
    return jsonify(stock=stock.serialize)


if __name__ == '__main__':
    app.secret_key = 'b_5#y2L"F4Q8z\n\xec]/'
    app.debug = True # server reloads each time there's a code change
    app.run(host = '0.0.0.0', port = 5000)