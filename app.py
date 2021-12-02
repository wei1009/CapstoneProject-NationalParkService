from flask import Flask, render_template, redirect, session, g, flash, request, url_for
from forms import UserForm, UserLoginForm
from models import db, connect_db, User, Favorites
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from api import *
import os
import re

CURR_USER_KEY = "curr_user"
app = Flask(__name__)
uri = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI','postgresql:///park_info')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY","secret")

connect_db(app)

debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return render_template("homepage.html")

##############################################################################
# User signup/login/logout
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    """User register"""
    form = UserForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username = form.username.data,
                email = form.email.data,
                password = form.password.data)
            db.session.commit()
        except IntegrityError:
            return render_template("user/register.html", form=form)
        do_login(user)

        return redirect("/")
    else:
        return render_template("user/register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_user():
    """User login"""
    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.email.data,form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        else:
            form.email.errors = ['Invalid username/password.']

    return render_template("user/login.html", form=form)

@app.route("/logout")
def logout():
    """Logout route."""

    do_logout()
    return redirect("/login")

##############################################################################
# park info
@app.route('/getparks', methods=['GET'])
def getParks():
    """Call National parks API"""
    parkCode = request.args.get('parkcode')
    stateCode = request.args.get('state')
    limit = request.args.get('limit')

    parks = get_parks(stateCode, parkCode, limit)
    return parks

@app.route("/parkinfo/<parkcode>")
def show_park(parkcode):
    """Call single park API and get lat and lng data for Google Map API"""
    apiParkData =  get_parks(None, parkcode, None)
    park = get_park_info(apiParkData)

    coords = {'lat': park["lat"], 'lng': park["lng"]}
    mapinfo = get_map(coords)

    likes_park_codes = []

    if g.user:
        likes_park_codes = [park.parkcode for park in g.user.favorites]

    return render_template("park/parkinfo.html",park=park, mapinfo=mapinfo,parkcode=parkcode, likes=likes_park_codes, images=park["images"])

#########################################################################

@app.route("/park/<parkcode>/addfavoritepark", methods=["POST"])
def add_favorite_park(parkcode):
    """Toggle a liked park for the currently-logged-in user."""
    if not g.user:
        return redirect("/login")

    like_park = Favorites(
                            user_id = g.user.id,
                            parkcode=parkcode)
    liked_park = Favorites.query.filter_by(user_id = g.user.id, parkcode=parkcode).first()

    if not liked_park:
        g.user.favorites.append(like_park)
    else:
        db.session.delete(liked_park)

    db.session.commit()
    return redirect(f"/parkinfo/{parkcode}")

@app.route("/parks/state/<state>")
def get_park_by_state(state):
    """Call National park API by state and show state parks infomation"""
    apiParkData = get_parks(state, None, None)
    stateData = apiParkData["data"]
    return render_template("park/stateparksinfo.html",state=stateData,statename=state)

########################################################################
@app.route('/user/<int:user_id>/favorites', methods=["GET"])
def show_favorites(user_id):
    """Show user favorite parks"""
    user = User.query.get_or_404(user_id)

    favoriteParks = Favorites.query.filter(Favorites.user_id == g.user.id).all()

    parkCodeStr=""

    for park in favoriteParks:
        parkCodeStr += park.parkcode + ","

    if parkCodeStr != "":
        parkCodeStr=parkCodeStr[0:len(parkCodeStr)-1]
        apiParkData = get_parks(None, parkCodeStr, None)
        favoriteParksData = apiParkData["data"]

        return render_template("user/favorites.html", user=user,parks=favoriteParksData)

    return render_template("user/favorites.html")

@app.route('/user/<parkcode>/deletefavoritepark',  methods=["GET", "POST"])
def delete_favorite_park(parkcode):
    """Delete favorite park in favorite lists"""
    liked_park = Favorites.query.filter_by(user_id = g.user.id, parkcode=parkcode).first()
    db.session.delete(liked_park)
    db.session.commit()
    return redirect(f"/user/{g.user.id}/favorites")
