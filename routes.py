from app import app, database
from models import User, Relationship, Message
from functools import wraps
from hashlib import md5



from flask import Flask, render_template, request, redirect, url_for, flash, session
from peewee import *
from hashlib import md5


################
# Helper
################


@app.before_request
def before_request():
    database.connect()
    
    
@app.after_request
def after_request(response):
    database.close()
    return response


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


@app.context_processor
def _inject_user():
    return {'active_user': get_current_user()}


def getUserOrAbort(username):
    try:
        return User.get(User.username == username)
        
    except User.DoesNotExist:
        return render_template('404.html')
    
    
    
    
################
# Routing 
################


# index
@app.route('/')
@redirect_if_logged
def index():
    return render_template('index.html')


# main app
@app.route('/home')
@login_required
def home():
    
    user = get_current_user()
    messages = (Message.select()
                .where(Message.user)
                .order_by(
                    Message.published_at.desc()))
       
    return render_template('home.html', messages = messages, user=user)
 
  
# register
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


# login
@app.route('/login', methods=['GET', 'POST'])
@redirect_if_logged
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


# logout
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))



# create function
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



# edit function
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user = get_current_user()
    if request.method == 'POST' and request.form['content'] and request.form['id']:
        message = Message.update(content = request.form['content']).where(Message.id == request.form['id']).execute()
        flash('Message posted')
        return redirect(url_for('user_profile', username = user.username))
    message = Message.select().where(Message.id == request.args.get('id')).first()
    return render_template('edit.html', message = message)



# delete function
@app.route('/delete', methods=['GET'])
@login_required
def delete():
    message = Message.delete().where(Message.id == request.args.get('id')).execute()
    user = get_current_user()
    return redirect(url_for('user_profile', username = user.username))
    


# profile page
@app.route('/user/<username>')
@login_required
def user_profile(username):
    user = getUserOrAbort(username)
    if(username == get_current_user().username):
        myself = True 
    else:
        myself = False
    email = user.email
    messages = Message.select().where(Message.user == user).order_by(Message.published_at.desc())
    return render_template('user.html', messages=messages, user=user, email=email, myself=myself)
        


# not found page
@app.route('/404')
def not_found():
    return render_template('404.html')
    
    


# about page
@app.route('/about')
def about():
    return render_template('about.html')


# follow and unfollow
@app.route('/follow/<username>', methods=['POST'])
def follow_user(username):
    try:
        user = User.get(User.username == username)
        
    except User.DoesNotExist:
        return render_template('404.html')
    
    
    try:
        with database.atomic():
            Relationship.create(
                from_user=get_current_user(),
                to_user = user)
            
    except IntegrityError:
        pass
    
    flash('You are now following ' + username)
    return redirect(url_for('user_profile', username=username))


@app.route('/unfollow/<username>', methods=['POST'])
def unfollow_user(username):
    user = getUserOrAbort(username)
    

    (Relationship.delete().where(
        (Relationship.from_user == get_current_user()) &
        (Relationship.to_user == user)).execute())
            
        
    flash('You are no longer following ' + username)
    return redirect(url_for('user_profile', username=username))



# list of followers and following page
@app.route('/user/<username>/followers')
def show_followers(username):
    user = getUserOrAbort(username)
    
    followers = user.followers()
    return render_template('followers.html', users = followers, user = user)


@app.route('/user/<username>/following')
def show_following(username):
    user = getUserOrAbort(username)
    
    return render_template('following.html', users = user.following(), user = user)
