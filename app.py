import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from peewee import *


app = Flask(__name__)

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
    user = ForeignKeyField(User, related_name='messages')
    content = TextField()
    creat_at = DateTimeField(default=datetime.datetime.now())
    
class Relationship(BaseModel):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')
    created_at = DateTimeField(default=datetime.datetime.now())
    
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
    
