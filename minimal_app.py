from flask import Flask
from flask_sqlalchemy import SQLAlchemy

'''
/home/nist778/nist778/songs/env/lib/python3.7/site-packages/flask_sqlalchemy/__init_
_.py:835: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS
adds significant overhead and will be disabled by 
default in the future.  Set it to True or False to sup
press this warning. 'SQLALCHEMY_TRACK_MODIFICATIONS 
adds significant overhead and '
'''


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/nist778/nist778/songs/adsf.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '%s' % (self.username,self.email)

