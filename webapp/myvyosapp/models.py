from flask_login import UserMixin

from myvyosapp import login,db
import uuid

import datetime
import bcrypt

from myvyosapp import app


class User(UserMixin,db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), index=True, unique=True)
    signup_date = db.Column(db.DateTime)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def setPassword(self, login_passwd):
        pw_hash = bcrypt.hashpw(login_passwd.encode('utf-8'),bcrypt.gensalt())
        passwd = Password(password=pw_hash,user_id=self.id,last_update=datetime.datetime.now())
        db.session.add(passwd);
        db.session.commit()

    def checkPassword(self, login_passwd):
        passwd = Password.query.filter_by(user_id=self.id).first()
        return  bcrypt.checkpw(login_passwd.encode('utf-8'),passwd.password.encode('utf-8'))

    def generateAPIKey(self):
        apikey = uuid.uuid4()
        apikeyobj = ApiKey(user_id=self.id,apikey=apikey)
        db.session.add(apikeyobj)
        db.session.commit()
        return apikeyobj

    def deleteAPIKey(self):
        ApiKey.query.filter_by(user_id=self.id).delete()
        db.session.commit()


    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'signup_date': self.signup_date,
        }

class ApiKey(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    apikey = db.Column(db.String(48), index=True, unique=True)

    def __repr__(self):
        return '<ApiKey {0}>'.format(self.user_id)

class Password(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128))
    last_update = db.Column(db.DateTime)

    def __repr__(self):
        return '<Password {0}>'.format(self.user_id)

class Track(db.Model):

    track = db.Column(db.String(24), primary_key=True)
    current_version = db.Column(db.String(12))
    version_url = db.Column(db.String(128))

    def __repr__(self):
        return '<Track {0}>'.format(self.track)

class Stat(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.String(48), index=True, primary_key=True)
    cpu = db.Column(db.String(8))
    mem = db.Column(db.String(8))
    uptime = db.Column(db.Float)
    root_usage = db.Column(db.String(8))
    version = db.Column(db.String(12))
    last_update = db.Column(db.DateTime)
    hostname = db.Column(db.String(64))
    remote_addr = db.Column(db.String(45))
    track = db.Column(db.String(24))

    def __repr__(self):
        return '<Stat {0}>'.format(self.system_id)
