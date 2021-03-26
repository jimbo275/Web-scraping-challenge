from flask import Flask, render_template, redirect
# import Flask, pymongo, and scrape_mars (your python file)
from flask_pymongo import PyMongo
import scrape_mars

# Instantiate a Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars = mongo.db.mars  
# Create a base '/' route that will query your mongodb database and render the `index.html` template
@app.route('/')
def index():
  
    scrape_dict = mongo.db.mars.find_one()
     
    # print(mars)
    # Return the template with the data passed in
    return render_template('index.html', mars=scrape_dict)

# Create a '/scrape' route that will create the mars collection, run your scrape() function from scrape_mars, and update the mars collection in the database
# The route should redirect back to the base route '/' with a code 302.
@app.route("/scrape")
def scraper():
    # insert the scraped image into the MongoDB
    scrape_dict = scrape_mars.scrape()
    mars.update({}, scrape_dict, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
# Run your app