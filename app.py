import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired , EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
# connecting to database
# old sqlite db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
# my new mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/our_users'
app.config['SECRET_KEY'] = 'mykey' 
# initializing database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# create a model
class Users (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #password creation
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # create a string
    def __repr__(self):
         return  '<Name %r>' % self.name

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")
        our_users = Users.query.order_by(Users.date_created).all()
        return render_template('add_user.html', form=form, name=name, our_users=our_users)
    except:
        flash("Error! Looks like there was a problem...try again!")
        return render_template('add_user.html', form=form, name=name, our_users=our_users)


# create a form class
class UserForm(FlaskForm): 
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit") 
 

# create a route for update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template('update.html', form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there was a problem...try again!")
            return render_template('update.html',
                                   form=form,
                                   name_to_update = name_to_update)
    else:
        return render_template('update.html',
                               form=form,
                               name_to_update = name_to_update, id=id)
    
        


# create a route decorator
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None 
    form = UserForm()
    if form.validate_on_submit():
        existing_user = Users.query.filter_by(name=form.name.data, email=form.email.data).first()
        if existing_user:
            flash("Username already exists")
        else:
            user = Users.query.filter_by(email=form.email.data).first()
            if user is None:
                # hash the password
                hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
                user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=form.password_hash.data)
                db.session.add(user)
                db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash("Form Submitted Successfully!")
        return redirect(url_for('add_user'))
    our_users = Users.query.order_by(Users.date_created).all()
    return render_template('add_user.html', form=form, name=name, our_users=our_users) 

@app.route('/')
def index():
    # first_name = "John"
	# stuff = "This is bold text"
	# favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template('index.html')

@app.route("/users/<name>")
def user(name):
    return render_template('user.html')



# create custom error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# create internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
    return render_template('name.html',
                            name = name, form = form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host="0.0.0.0",port=int(os.environ.get("PORT",8080)))