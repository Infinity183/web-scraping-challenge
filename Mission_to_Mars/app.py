from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scraper

app = Flask(__name__)

# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# db = client.mars_scraper_db
# mars_stuff = db.mars_stuff

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scraper_app")

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scraper")
def scraper():
    mars = mongo.db.mars
    mars_data = mars_scraper.scraper()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)