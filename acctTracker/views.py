from accountTracker import app

@app.route('/')
@app.route('/catalog/')
def showCatalog():
	return "This page will show the main page with each account"