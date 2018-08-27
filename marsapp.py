# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    fullmarsdata = db.collection.find_one()

    # return template and data
    return render_template("index.html", fullmarsdata=fullmarsdata)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    fullmarsdata= scrape_mars.scrape()

    # Insert forecast into database
    db.collection.drop()
    db.collection.insert_one(fullmarsdata)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
