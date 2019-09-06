from flask import render_template, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import datetime

from . import site
from ..models import db, User, Password, ApiKey, Track, Stat
from ..forms import LoginForm, SignupForm, GenerateApiKeyForm, DeleteApiKeyForm, SetTrackForm

from flask import Flask

import sys

from myvyosapp import app


@site.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@site.route('/', methods=['GET','POST'])
def index():
    apikeyform = None
    deletekeyform = None
    apikey = None
    tracks = None
    stats = None

    if current_user.is_authenticated:
        apikey = ApiKey.query.filter_by(user_id=current_user.id).first()
        if (apikey is None):
            apikeyform = GenerateApiKeyForm()
            if apikeyform.generate and apikeyform.validate_on_submit():
                apikey = current_user.generateAPIKey()
                apikeyform = None
                deletekeyform = DeleteApiKeyForm()
        else:
            deletekeyform = DeleteApiKeyForm()
            if deletekeyform.delete and deletekeyform.validate_on_submit():
                current_user.deleteAPIKey()
                apikey = None
                deletekeyform = None
                apikeyform = GenerateApiKeyForm()

        tracks=Track.query.all()
        stats=Stat.query.filter_by(user_id=current_user.id).all()

        track_choice_list=[(i.track,i.track) for i in tracks]

        ## manipulate the stats for some display stuff
        for idx in range(len(stats)):
            days = divmod(stats[idx].uptime, 86400)
            hours = divmod(days[1], 3600)
            minutes = divmod(hours[1], 60)
            d = "s"
            if (days[0] == 1):
                d = ""
            stats[idx].formatted_uptime = "{:d} day{!s} {:02d}:{:02d}:{:02d}".format(int(days[0]), d, int(hours[0]), int(minutes[0]), int(minutes[1]))

            for track in tracks:
                if stats[idx].track == track.track:
                    stats[idx].trackObj = track

            trackForm = SetTrackForm(system_id = stats[idx].system_id,track_id=stats[idx].track)
            trackForm.track_id.choices = track_choice_list
            stats[idx].trackForm=trackForm;


    return render_template('index.html',apikey=apikey, apikeyform=apikeyform, deletekeyform=deletekeyform, tracks=tracks, stats=stats )


@site.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('site.index',_external=True))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.checkPassword(form.password.data):
            flash('Invalid username or password')
            return render_template('login.html',form=form,invalid_login=True)
        login_user(user)
        return redirect(url_for('site.index', _external=True))
    return render_template('login.html',form=form)

@site.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    Exists = False
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is not None:
            Exists = True
        else:
            signup_date = datetime.datetime.now()
            user = User(username=form.username.data, signup_date=signup_date)
            db.session.add(user)
            db.session.commit()
            user.setPassword(form.password.data)
            login_user(user)
            return redirect(url_for('site.index', _external=True))



    return render_template('signup.html',form=form, Exists=Exists)

@site.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.index', _external=True))

