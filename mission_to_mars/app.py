from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# PyMongo to  Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
#home route
@app.route("/")
def home():
    # find one of the data in mongo
    mars_data = mongo.db.collection.find_one()
    #render with the html template and have the data returned
    return render_template("index.html", mars=mars_data)
# scrape function route
@app.route("/scrape")
def scrape():
    mars_dict = scrape_mars.scrape_info()
#  Update database with upsert=True
    mongo.db.collection.update({}, mars_dict, upsert=True)
#back to home page
    return redirect("/")

#most important 
if __name__ == "__main__":
    app.run(debug=True)