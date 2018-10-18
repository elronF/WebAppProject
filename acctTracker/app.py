from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Account, Stock

app = Flask(__name__)

engine = create_engine('sqlite:///tracker.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show all accounts
@app.route('/')
@app.route('/accounts')
def showAccounts():
    accounts = session.query(Account).all()
    return render_template('accounts.html', accounts=accounts)


if __name__ == '__main__':
    app.debug = True # server reloads each time there's a code change
    app.run(host = '0.0.0.0', port = 5000)