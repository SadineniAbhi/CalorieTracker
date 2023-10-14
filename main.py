import os
from flask import Flask, render_template, session, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,FloatField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
from wtforms_alchemy import QuerySelectField
import logging

######################################
#### SET UP OUR SQLite DATABASE #####
####################################

app = Flask(__name__)

# This grabs our directory
basedir = os.path.abspath(os.path.dirname(__file__))


# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "KEY"
db = SQLAlchemy(app)

#reads and updates the changes in the database design
Migrate(app,db)


class FoodItems(db.Model):
    item = db.Column(db.Text, primary_key=True)
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)

    def __init__(self, item, calories, protein):
        self.item = item
        self.calories = calories
        self.protein = protein

    def __repr__(self):
        return "item {} has {} calories and has {} protien".format(self.item, self.calories, self.protein)


class EatenItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Text)
    weight = db.Column(db.Integer)

    def __init__(self, item, weight):
        self.item = item
        self.weight = weight

    def __repr__(self):
        return "you ate {} grams of {}".format(self.weight, self.item)


class AddToTodayTable(FlaskForm):
    item = QuerySelectField('Select an item', query_factory=lambda: FoodItems.query, get_label='item')
    weight = FloatField("enter the weight of food")
    submit = SubmitField("Submit")


class AddToItemsTable(FlaskForm):
    item = StringField("Enter the name of the item")
    calories = FloatField("Enter the calories of item")
    protein =  FloatField("Enter the amount of protein in the item")
    submit = SubmitField("Submit")


@app.route("/",methods=['GET','POST'])
def home():
    form = AddToTodayTable()
    data = EatenItems.query.all()
    if form.validate_on_submit():
        app.logger.critical("This is a critical message")
        itemname = form.item.data
        itemweight = form.weight.data
        ate = EatenItems(itemname,itemweight)
        data = EatenItems.query.all()
        db.session.add(ate)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("home.html",form = form,data = data)

if __name__ == "__main__":
    app.run(debug= True)