import datetime, sqlalchemy
from email import message
from functools import wraps


from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from peewee import *
from hashlib import md5


app = Flask(__name__)
app.secret_key = 'secretkeyuye'

DATABASE = 'curhatin.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database
        
        
class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)
    join_at = DateTimeField(default=datetime.datetime.now())
    
    
    def following(self):
        return User.select().join(
            Relationship, on=Relationship.to_user).where(
                Relationship.from_user == self).order_by(User.username)
            
    def followers(self):
        return User.select().join(
            Relationship, on=Relationship.from_user).where(
                Relationship.to_user == self).order_by(User.username)

class Message(BaseModel):
    user = ForeignKeyField(User, backref='messages')
    content = TextField()
    published_at = DateTimeField(default=datetime.datetime.now())
    
class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref='relationships')
    to_user = ForeignKeyField(User, backref='related_to')
    published_at = DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        indexes = (
            (('from_user', 'to_user'), True),
        )
        

@app.before_request
def before_request():
    database.connect()
    
    
@app.after_request
def after_request(response):
    database.close()
    return response

def create_tables():
    database.create_tables([User, Relationship, Message])
    


# =======================
#  Routing
# ======================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def redirect_if_logged(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in'):
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

    
def get_current_user():
    if session.get('logged_in'):
        return User.get(User.id == session['user_id'])
    
    
    
def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['username'] = user.username



@app.route('/')
@redirect_if_logged
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    if session.get('logged_in'):
        return render_template('home.html', user=get_current_user())
    else:
        return redirect(url_for('index'))
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and request.form['username'] and request.form['email'] and request.form['password']:
        try:
            with database.atomic():
                user = User.create(
                    username=request.form['username'],
                    password=md5(request.form['password'].encode('utf-8')).hexdigest(),
                    email=request.form['email'])

            
            return redirect(url_for('login'))
        
        except IntegrityError:
            flash('User already exists')
            return redirect(url_for('register'))
            
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['username'] and request.form['password']:
        try:
            hashed_pass = md5(request.form['password'].encode('utf-8')).hexdigest()
            user = User.get(
                (User.username == request.form['username']) & 
                (User.get(User.password == hashed_pass)))
            
            
            
        except User.DoesNotExist:
            flash('Wrong user or password')
        
        else:
            auth_user(user)
            return redirect(url_for('home'))

        
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ==============
# routing to post


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    user = get_current_user()
    if request.method == 'POST' and request.form['content']:
        message = Message.create(
            user = user,
            content = request.form['content']
            )
        
        flash('Message posted')
        return redirect(url_for('user_profile', username = user.username))
    
    return render_template('create.html')



@app.route('/user/<username>')
def user_profile(username):
    user = User.get(User.username == username)
    email = user.email
    messages = Message.select().where(Message.user == user).order_by(Message.published_at.desc())
    return render_template('user.html', messages=messages, username=username, email=email)


# def usredirect(username):
#     user = User.get(User.username == username)
#     return redirect(url_for('user_profile', username=user.username))

@app.route('/404')
def not_found():
    return render_template('404.html')
    