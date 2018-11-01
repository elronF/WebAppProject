from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, flash

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Owner, Account, Stock, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import socks
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
                open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Account Tracker App"

app = Flask(__name__)

engine = create_engine('sqlite:///tracker_v2.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# OAUTH LOGIC
@app.route('/login/')
def showLogin():
    '''Create state token. Store in session.'''
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''Validate state token'''
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    '''Get auth code'''
    code = request.data
    try:
        '''upgrade auth code into credentials object'''
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Check validity of access token'''
    access_token = credentials.access_token
    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
    urlToken = (url).format(access_token)
    h = httplib2.Http()
    result = json.loads(h.request(urlToken, 'GET')[1].decode('utf-8'))
    print(result)

    '''Abort if access token is invalid'''
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    '''Verify access token is used for intended user'''
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    '''Verify that access token is valid for app'''
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            "Token's client ID doesn't match app's client ID"), 401)
        print("Token's client ID doesn't match app's")
        response.headers['Content-Type'] = 'application/json'
        return response

    '''Check to see if user already logged in'''
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user already logged-in.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    '''Store access token for later use'''
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    '''Get user info'''
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    print(data)

    login_session['email'] = data["email"]

    output = ''
    output += '<h1>Welcome, '
    output += login_session['email']
    output += '!</h1>'
    flash("You are now logged in as {}".format(login_session['email']))
    print("done!")
    return output

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


# DISCONNECT - Revoke a current user's token and reset their login_session
# To disconnect from google login
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Logged out successfully")
        return redirect(url_for('showAccounts'))
    else:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['email']
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        print(response)
        flash("Logout failed")
        return redirect(url_for('showAccounts'))


# USER FUNCTIONS
def getUserID(email):
    '''Returns a user ID if email matches'''
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


def getUserInfo(user_id):
    '''If userid passed in, returns user object associated with user number'''
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    '''Creates a new user in the DB based on name and email, returns an ID.'''
    newUser = User(email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# ROUTES-NO LOGIN
@app.route('/')
@app.route('/accounts/')
def showAccounts():
    '''Show all accounts'''
    accounts = session.query(Account).order_by(asc(Account.accountType))
    stocks = session.query(Stock).order_by(asc(Stock.account_id))
    return render_template('stocks.html', accounts=accounts, stocks=stocks)


# ROUTES-LOGIN
@app.route('/accounts/<int:account_id>/')
def showOneAccount(account_id):
    '''Show the contents of one account'''
    accountsOne = session.query(Account).order_by(asc(Account.accountType))
    accountOne = session.query(Account).filter_by(id=account_id).one()
    stocksOne = session.query(Stock).filter_by(account_id=account_id).all()
    if 'email' not in login_session:
        return render_template('publicaccount.html',
                               accounts=accountsOne,
                               account=accountOne,
                               stocks=stocksOne)
    else:
        return render_template('account.html',
                               accounts=accountsOne,
                               account=accountOne,
                               stocks=stocksOne)


@app.route('/accounts/<int:account_id>/<string:stock_ticker>/')
def showStockDetails(account_id, stock_ticker):
    '''Show the details of one stock'''
    stock = session.query(Stock).filter_by(ticker=stock_ticker).one()
    account = session.query(Account).filter_by(id=account_id).one()
    return("Hey there fella, something worked!")


@app.route('/accounts/<int:account_id>/stock/create/', methods=['GET', 'POST'])
def newStock(account_id):
    '''Create new stock'''
    accounts = session.query(Account).order_by(asc(Account.accountType))
    account = session.query(Account).filter_by(id=account_id).one()
    if 'email' not in login_session:
        return redirect('/login/')
    if request.method == 'POST':
        newStock = Stock(companyName=request.form['companyName'],
                         ticker=request.form['ticker'],
                         exchange=request.form['exchange'],
                         industry=request.form['industry'],
                         description=request.form['description'],
                         account_id=account_id,
                         user_id=login_session['user_id'])
        session.add(newStock)
        flash('{} has been added to your {} account'.format(
            newStock.companyName, account.accountType))
        session.commit()
        return redirect(url_for('showOneAccount', account_id=account_id))
    else:
        return render_template('createstock.html',
                               accounts=accounts,
                               account_id=account_id)


@app.route('/accounts/<int:account_id>/<string:stock_ticker>/update/',
           methods=['GET', 'POST'])
def editStock(account_id, stock_ticker):
    '''Edit stock details'''
    accounts = session.query(Account).order_by(asc(Account.accountType))
    account = session.query(Account).filter_by(id=account_id).one()
    updatedStock = session.query(Stock).filter_by(ticker=stock_ticker).one()
    if 'email' not in login_session:
        return redirect('/login/')
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
        return redirect(url_for('showOneAccount', account_id=account_id))
    else:
        return render_template('editstock.html',
                               accounts=accounts,
                               account=account,
                               stock=updatedStock)


@app.route('/accounts/<int:account_id>/<string:stock_ticker>/delete/',
           methods=['GET', 'POST'])
def deleteStock(account_id, stock_ticker):
    '''Delete a stock'''
    account = session.query(Account).filter_by(id=account_id).one()
    deleteStock = session.query(Stock).filter_by(ticker=stock_ticker).one()
    if 'email' not in login_session:
        return redirect('/login/')
    session.delete(deleteStock)
    flash('{} has been deleted'.format(deleteStock.companyName))
    session.commit()
    return redirect(url_for('showOneAccount', account_id=account_id))


# JSON ENDPOINTS
@app.route('/accounts/JSON/')
def accountsJSON():
    '''Show JSON for accounts'''
    accounts = session.query(Account).all()
    return jsonify(accounts=[a.serialize for a in accounts])


@app.route('/accounts/<int:account_id>/<string:stock_ticker>/JSON/')
def stockJSON(account_id, stock_ticker):
    '''Show JSON for stocks'''
    stock = session.query(Stock).filter_by(ticker=stock_ticker).one()
    return jsonify(stock=stock.serialize)


if __name__ == '__main__':
    app.secret_key = 'b_5#y2L"F4Q8z\n\xec]/'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
