from flask import current_app, request, url_for

from . import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    
    # one_to_many relationship
    # backref - Add a back reference in the other model in the relationship
    users = db.relationship('User', backref='role',lazy='dynamic')

    #for debugging and testing purposes
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    
    # one_to_many relationship
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    #for debugging and testing purposes
    def __repr__(self):
        return '<User %r>' % self.username