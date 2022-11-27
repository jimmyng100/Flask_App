from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
# import psycopg2
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsaSecret'


POSTGRES = {
    'user':'postgres',
    'pw': 'password',
    'db': 'dvdrental',
    'host':'localhost',
    'port': '5432'
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES



db = SQLAlchemy(app)
# db.init_app(app)

#
#Create db model
class tbl_email(db.Model):
    email = db.Column(db.String(30), primary_key=True, nullable=False)

class reportForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message='Please enter this dumbo'), Length(min=5, max=10, message='Message be 5-10')])
    form_action = SelectField('Select Action', choices=[ ('add', 'Add'), ('delete', 'Delete'), ('update', 'Update') ])

@app.route("/")
@app.route("/form", methods=['POST','GET'])
def form():
    form = reportForm()

    email = form.email.data
    new_register = tbl_email(email=email)

    if form.validate_on_submit() == False:
        return render_template('form.html', title='My Form', form=form)

    if form.form_action.data == 'add' and bool(db.session.query(tbl_email).filter_by(email=email).first())==True:
        flash("Email already exist.")
        return render_template('form.html', title='My Form', form=form)

    if form.form_action.data == 'delete' and bool(db.session.query(tbl_email).filter_by(email=email).first())==False:
        flash("Email does not exist in record.")
        return render_template('form.html', title='My Form', form=form)

    if form.form_action.data == 'add':
        db.session.add(new_register)
        db.session.commit()
        flash("Data entered!")
        return render_template('form.html', title='My Form', form=form)
    elif form.form_action.data == 'delete':
        tbl_email.query.filter_by(email=email).delete()
        db.session.commit()
        flash("Data deleted!")
        return render_template('form.html', title='My Form', form=form)

    return render_template('form.html', title='My Form', form=form)

# http://127.0.0.1:5000/first_page
@app.route("/first_page", methods=['POST','GET'])
def first_page():
    return render_template('first_page.html')


if __name__ == '__main__':
    app.run(debug=True)
    #my PC ip address. Allows my PC to be the host and allow other PC within my network to access.
    # app.run(host='192.168.1.3')
