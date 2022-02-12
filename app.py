# MongoDB and Flask app

# Dependencies

from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# MongoDB setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)


# Flask route
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_facts = scrape_mars.scrape_all()
    mars.update({}, mars_facts, upsert=True)
    return "Scrape Successful"

if __name__ == "__main__":
    app.run(debug=True)



