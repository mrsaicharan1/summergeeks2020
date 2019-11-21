#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
from config import account_sid, auth_token, from_phone, SENDGRID_API_KEY, address
from sqlalchemy import exc
import logging
import smtplib
from logging import Formatter, FileHandler
from forms import *
from models import *
import os
import datetime

from helpers import send_mail
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'TEST SECRET KEY'



@app.route('/')
def home():
    return redirect(url_for('checkin_visitor'))


@app.route('/checkin/visitor', methods=['POST','GET'])
def checkin_visitor():
    if request.method == 'POST':
        try:
            visitor = Visitor(name=request.form['name'], email=request.form['email'], phone=request.form['phone'],
                               check_in=datetime.datetime.now())
            host = db.session.query(Host).get(request.form['host_name'])
            visitor.host = host
            db.session.add(visitor)
            db.session.commit()
        except exc.IntegrityError as e:
            flash('An error has occurred. Please try again.')

        # send sms to host
        client = Client(os.getenv('account_sid'), os.getenv('auth_token'))
        message = client.messages \
                .create(
                     body='A new visitor has checked in. Details: {0}\n{1}\n{2}\n{3}'.format(
                         request.form['name'], request.form['email'], host.phone, 
                         visitor.check_in.strftime("%b %d %Y %H:%M:%S")
                     ),
                     from_=from_phone,
                     to=host.phone
                 )
        # send sms to client for checkout code(id)
        message = client.messages \
                .create(
                     body='Greetings Visitor. Here\'s your checkout code. Have a great day!: {0}'.format(visitor.id) ,from_=from_phone, to=request.form['phone'])
        # send email to host
        to_emails=request.form['email']
        subject='New Visitor Alert'
        html_content='A new visitor has checked in. Details: {0}\n{1}\n{2}\n{3}'.format(
                        request.form['name'], request.form['email'], request.form['phone'], 
                        visitor.check_in.strftime("%b %d %Y %H:%M:%S"))
        send_mail(to_emails, subject, html_content)

    hosts = db.session.query(Host).filter_by(check_out=None).all()
    return render_template('forms/visitor.html', hosts=hosts)


@app.route('/checkin/host', methods=['POST','GET'])
def checkin_host():
    if request.method == 'POST':
        host = Host(name=request.form['name'], phone=request.form['phone'], email=request.form['email'], check_in=datetime.datetime.now())
        db.session.add(host)
        db.session.commit()
    return render_template('forms/host.html')

@app.route('/checkout', methods=['POST','GET'])
def checkout():
    if request.method == 'POST':
        if request.form['type'] == 'visitor':
            visitor = db.session.query(Visitor).filter_by(uuid_code=request.form['uuid_code']).one()
            if visitor is None:
                flash('No such visitor with a uuid {}'.format(request.form['uuid_code']))
            elif visitor.check_out is None:
                visitor.check_out = datetime.datetime.now()
                db.session.commit()
                to_emails = visitor.email
                subject = 'Visit Details'
                content = "Name: {}\n".format(str(visitor.name)) +  "Phone: {}\n".format(str(visitor.phone)) + \
                        "Checkin Time: {}\n".format(str(visitor.check_in.strftime("%b %d %Y %H:%M:%S"))) + \
                        "Checkout Time: {}\n".format((visitor.check_out.strftime("%b %d %Y %H:%M:%S"))) + "Address: {}\n".format(address) + "Host Name: {}".format(visitor.host.name)
                send_mail(to_emails, subject, content)
                flash('Visitor ID {} has successfully checked out'.format(visitor.uuid_code))
            else:
                flash('The visitor/host has already checked out.')
        elif request.form['type'] == 'host':
            host = db.session.query(Host).filter_by(uuid_code=request.form['uuid_code']).one()
            host.check_out = datetime.datetime.now()
            db.session.commit()
            flash('Host ID {} has successfully checked out'.format(host.uuid_code))


    return render_template('forms/checkout.html')



#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

