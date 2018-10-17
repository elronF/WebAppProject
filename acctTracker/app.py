from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Account, Stock

app = Flask(__name__)

engine = create_engine('sqlite:///tracker.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


account = {'id': '1', 'owner': 'Logan', 'accountType': 'RRSP', 'institution': 'RBC'}
accounts = [{'id': '1', 'owner': 'Logan', 'accountType': 'RRSP', 'institution': 'RBC'}, 
            {'id': '2', 'owner': 'Madeleine', 'accountType': 'RRSP', 'institution': 'RBC'}, 
            {'id': '3', 'owner': 'Logan', 'accountType': 'TFSA', 'institution': 'RBC'}, 
            {'id': '4', 'owner': 'Madeleine', 'accountType': 'TFSA', 'institution': 'RBC'}]

stock = {'id': '1', 'ticker': 'CJ', 'exchange': 'TSX', 'companyName': 'Cardinal Energy', 'industry': 'Energy'}
stocks = [{'id': '1', 'ticker': 'CJ', 'exchange': 'TSX', 'companyName': 'Cardinal Energy', 'industry': 'Energy'}, 
          {'id': '2', 'ticker': 'ACB', 'exchange': 'TSX', 'companyName': 'Aurora Cannabis', 'industry': 'Cannabis'},
          {'id': '3', 'ticker': 'GOOG', 'exchange': 'NASDAQ', 'companyName': 'Alphabet Inc', 'industry': 'Technology'}]


# Show all accounts
@app.route('/')
@app.route('/accounts')
def showAccounts():
    return render_template('accounts.html', accounts=accounts)

# Show all accounts of one owner
@app.route('/accounts/<string:owner>/')
def showOwnerAccounts(owner):




if __name__ == '__main__':
    app.debug = True # server reloads each time there's a code change
    app.run(host = '0.0.0.0', port = 5000)