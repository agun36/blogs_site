from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)
# connecting to database
# old sqlite db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
# my new mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/our_users'
app.config['SECRET_KEY'] = 'mykey' 
# initializing database
db = SQLAlchemy(app)


# create a model
class Users (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # create a string
    def __repr__(self):
         return  '<Name %r>' % self.name

# create a form class
class UserForm(FlaskForm): 
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
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
                               name_to_update = name_to_update)
    
        


# create a route decorator
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None 
    form = UserForm()
    if form.validate_on_submit():
        existing_user = Users.query.filter_by(name=form.name.data).first()
        if existing_user:
            flash("Username already exists")
        else:
            user = Users.query.filter_by(email=form.email.data).first()
            if user is None:
                user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
                db.session.add(user)
                db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        flash("Form Submitted Successfully!")
        return redirect(url_for('add_user'))
    our_users = Users.query.order_by(Users.date_created).all()
    return render_template('add_user.html', form=form, name=name, our_users=our_users) 

@app.route('/')
def index():
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
    app.run(debug=True, host='0.0.0.0', port=5001)