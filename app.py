import json
import random
import datetime

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

# Links
# https://www.geeksforgeeks.org/flask-rendering-templates <- FLask tutorial
# https://pythonbasics.org/flask-sqlalchemy/#CRUD <- Flask SQLAlchemy tutorial


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# Company name
company='Joes Garage'

# Database setup
db = SQLAlchemy(app)

# Database models
class route(db.Model): 
    id = db.Column('route_id',db.Integer, primary_key = True, autoincrement=True)
    origin= db.Column(db.String(3))
    destination= db.Column(db.String(3))
    radius_o= db.Column(db.Integer)
    radius_d= db.Column(db.Integer) 
    startdate= db.Column(db.String(10))
    enddate= db.Column(db.String(10))
    maxweight= db.Column(db.Integer)
    trailertype= db.Column(db.String(25))
    trailerlength= db.Column(db.Integer)

# Routes
@app.route('/')
def home():
    return render_template('base.html', company_name=company)

@app.route('/dashboard')
def dashboard():
    list=getHistory('')
    return render_template('Dashboard.html', company_name=company, history=list)
    
@app.route('/account')
def account():
    return render_template('Account.html', company_name=company)
    
@app.route('/contact')
def contact():
    return render_template('ContactUs.html', company_name=company)
    
@app.route('/profile')
def profile():
    return render_template('Profile.html', company_name=company)

@app.route('/AddRoute', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['origin'] or not request.form['destination'] :
         flash('Please enter all the fields', 'error')
      else:
         newRoute = route(
            origin = request.form['origin'], 
            destination = request.form['destination'],
            radius_o = request.form['radius_o'],
            radius_d = request.form['radius_d'],
            startdate = request.form['startdate'],
            enddate = request.form['enddate'],
            maxweight= request.form['maxweight'],
            trailertype = request.form['ttype'],
            trailerlength = request.form['tlength']
            )
         
         db.session.add(newRoute)
         db.session.commit()
         flash('Record was successfully added')
   return redirect(url_for('dashboard'))

# internal functions
def getHistory(username):
    list = route.query.all()
    return list

# Start the App
if __name__ == "__main__":
    app.run()

with app.app_context():
    db.create_all()
