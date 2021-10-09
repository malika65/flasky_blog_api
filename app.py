import os
from flask import Flask, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))

# app instance  
app = Flask(__name__)

#configuration of db
app.config['SQLALCHEMY_DATABASE_URI'] =\
 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

#to use less memory unless signals for object changes are needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

#Flask-Mail is initialized
mail = Mail(app)

#configure the application to send email through a Google Gmail account
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')


class NameForm(FlaskForm):
    #The DataRequired() validator ensures that the field is not submitted empty
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


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


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))   
    return render_template('index.html',
    form = form,
    name = session.get('name'), 
    known = session.get('known', False))

#The flask shell command will import these items automatically into the shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# if __name__ == '__main__':
#     app.run(debug=True)