
from flask import Flask
from peewee import *



app = Flask(__name__)
app.config.from_pyfile('config.py')


                     
# database = MySQLDatabase('curhatin', user='root', passwd='', host='localhost')
database = SqliteDatabase(app.config['DATABASE_URI'])


from routes import *

if __name__ == '__main__':
    app.run(debug=True)
