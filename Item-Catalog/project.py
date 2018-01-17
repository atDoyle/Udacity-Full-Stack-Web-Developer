# Import packages
import os
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   jsonify,
                   flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Team, Player
from flask import session as login_session
from flask import make_response, send_from_directory
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from werkzeug.utils import secure_filename
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)

# Import client ID information for Gplus signin
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Baseball Card Catalog"

engine = create_engine('sqlite:///mlb_cards.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Allow for the user to upload images
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Connect to Facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/v2.11/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (  # noqa
           app_id, app_secret, access_token)
    print url
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    # Extract the access token from response
    token = 'access_token=' + data['access_token']

    # Use token to get user info from API.
    url = 'https://graph.facebook.com/v2.11/me?%s&fields=name,id,email,picture' % token  # noqa
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    login_session['picture'] = data["picture"]["data"]["url"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    print user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '" style = "width: 300px; ' \
              'height: 300px;' \
              'border-radius: 150px;' \
              '-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


# Disconnect from Facebook - Revoke a current user's token
# and reset their login_session
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)  # noqa
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "You have been logged out"


# Connect to Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    print login_session['gplus_id']

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; '\
              'height: 300px;' \
              'border-radius: 150px;' \
              '-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s." % login_session['username'])
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Disconnect from Google - Revoke a current user's token
# and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON Endpoints
@app.route('/teams/<int:team_id>/JSON')
def teamBaseballCardsJSON(team_id):
    players = session.query(Player).filter_by(team_id=team_id).all()
    return jsonify(BaseballCards=[i.serialize for i in players])


@app.route('/teams/<int:team_id>/<int:player_id>/JSON')
def playerBaseballCardJSON(team_id, player_id):
    player = session.query(Player).filter_by(id=player_id).all()
    return jsonify(CardInfo=[i.serialize for i in player])


# Determine if file uploaded by the user is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Initial routing function which queries the Team database
@app.route('/', methods=['GET', 'POST'])
def teams():
    teams = session.query(Team).all()
    return render_template('main.html', teams=teams)


# Routing function to add a new team to the Team database
@app.route('/teams/new', methods=['GET', 'POST'])
def newTeam():
    if 'username' not in login_session:
        flash('Please login to continue.')
        return redirect('/login')
    if request.method == 'POST':
        newItem = Team(name=request.form['name'],
                       user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New baseball team, the %s, successfully created.'
              '  You can now add baseball cards for this team.'
              % newItem.name)
        return redirect(url_for('teams'))
    else:
        return render_template('addTeam.html')


# Routing function to view existing baseball cards
# stored in the Players database for a specific team
@app.route('/teams/<int:team_id>')
def players(team_id):
    team = session.query(Team).filter_by(id=team_id).one()
    creator = getUserInfo(team.user_id)
    players = session.query(Player).filter_by(team_id=team_id).all()
    if ('username' not in login_session or
       creator.id != login_session['user_id']):
        return render_template('publicplayers.html',
                               team=team, players=players,
                               team_id=team_id,
                               creator=creator)
    else:
        return render_template('players.html',
                               team=team,
                               players=players,
                               team_id=team_id,
                               creator=creator)


# Routing function to add a new baseball card to the
# Players database
@app.route('/teams/<int:team_id>/new', methods=['GET', 'POST'])
def newBaseballCard(team_id):
    if 'username' not in login_session:
        flash('Please login to continue.')
        return redirect('/login')
    team = session.query(Team).filter_by(id=team_id).one()
    if login_session['user_id'] != team.user_id:
        flash('You are not authorized '
              'to add baseball cards for this team')
        return redirect(url_for('players', team_id=team_id))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        newItem = Player(name=request.form['name'],
                         price=request.form['price'],
                         image=filename,
                         team_id=team_id,
                         user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("New baseball card successfully created for %s." % newItem.name)
        return redirect(url_for('players', team_id=team_id))
    else:
        return render_template('create.html', team_id=team_id)


# Routing function to edit an existing baseball card
# in the Players database
@app.route('/teams/<int:team_id>/<int:player_id>/edit', methods=['GET', 'POST'])  # noqa
def editBaseballCard(team_id, player_id):
    if 'username' not in login_session:
        flash('Please login to continue.')
        return redirect('/login')
    editedItem = session.query(Player).filter_by(id=player_id).one()
    team = session.query(Team).filter_by(id=team_id).one()
    if login_session['user_id'] != team.user_id:
        flash('You are not authorized to edit this baseball card.')
        return redirect(url_for('players', team_id=team_id))
    if request.method == 'POST':
        if request.form['name'] and request.form['price']:
            editedItem.name = request.form['name']
            editedItem.price = request.form['price']
            session.add(editedItem)
            session.commit()
            flash('Baseball card successfully edited.')
        else:
            flash('No information entered. '
                  'Please enter both a new name and price.')
        return redirect(url_for('players', team_id=team_id))
    else:
        return render_template('edit.html',
                               team_id=team_id,
                               player_id=player_id,
                               item=editedItem)


# Routing function to delete a baseball card from the
# Players database
@app.route('/teams/<int:team_id>/<int:player_id>/delete', methods=['GET', 'POST'])  # noqa
def deleteBaseballCard(team_id, player_id):
    if 'username' not in login_session:
        flash('Please login to continue.')
        return redirect('/login')
    itemToDelete = session.query(Player).filter_by(id=player_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        flash('You are not authorized to delete this baseball card.')
        return redirect(url_for('players', team_id=team_id))
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.name)
        session.commit()
        return redirect(url_for('players', team_id=team_id))
    else:
        return render_template('delete.html',
                               team_id=team_id,
                               player_id=player_id,
                               item=itemToDelete)


# Routing function to upload an image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    print login_session
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('teams'))
    else:
        flash('You were not logged in')
        return redirect(url_for('teams'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
