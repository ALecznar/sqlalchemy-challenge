
from flask import Flask, jsonify
import datetime as dt
import pandas as pd
from sqlalchemy import create_engine

# Create a Flask app
app = Flask(__name__)


#sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Define the homepage route
@app.route('/')
def homepage():
    return "Welcome to My Climate App!"

# Define a route 
@app.route('/api/routes')
def list_routes():
    routes = [
        {"url": "/", "description": "Homepage (Welcome message)"}  
    ]
    
    return jsonify(routes)

#rout to 12 month precipitation rout 1
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Calculate the date 
    most_recent_date = engine.execute("SELECT MAX(date) FROM measurement").scalar()
    one_year_ago = pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)
    
    # Convert date formatting
    one_year_ago_str = one_year_ago.strftime('%Y-%m-%d')
    
    # precipitation data for the last 12 months
    query = f"SELECT date, prcp FROM measurement WHERE date >= '{one_year_ago_str}'"
    results = engine.execute(query).fetchall()
    
    # Convert to a dictionary
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp
    
    return jsonify(precipitation_data)

#rout 2
@app.route('/api/v1.0/stations')
def stations():
    # list of stations
    query = "SELECT station, name FROM station"
    results = engine.execute(query).fetchall()
    
    # Convert results to a list of dictionaries
    station_list = []
    for station, name in results:
        station_list.append({"station": station, "name": name})
    
    return jsonify(station_list)


#rout 3
@app.route('/api/v1.0/tobs')
def tobs():
    most_recent_date = engine.execute("SELECT MAX(date) FROM measurement").scalar()
    one_year_ago = pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)
    
    # Convert date format
    one_year_ago_str = one_year_ago.strftime('%Y-%m-%d')
    
    # most-active station in the last 12 months
    query = f"SELECT date, tobs FROM measurement WHERE date >= '{one_year_ago_str}' AND station = 'USC00519281'"
    results = engine.execute(query).fetchall()
    
    # Convert to a list of dictionaries
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in results]
    
    return jsonify(tobs_list)


# rout 4  not sure if this is what is being asked...... getting null for some reason

@app.route('/api/v1.0/<start>')
def temperature_range_start(start):
    query = f"SELECT MIN(tobs) AS TMIN, AVG(tobs) AS TAVG, MAX(tobs) AS TMAX FROM measurement WHERE date >= '{start}'"
    results = engine.execute(query).fetchall()
    
    # Convert to a list of dictionaries
    temperature_data = [{"TMIN": result.TMIN, "TAVG": result.TAVG, "TMAX": result.TMAX} for result in results]
    
    return jsonify(temperature_data)

#rout 5   not sure if this is what is being asked......getting null again...ahhhhhhh
@app.route('/api/v1.0/<start>/<end>')
def temperature_range_start_end(start, end):
    query = f"SELECT MIN(tobs) AS TMIN, AVG(tobs) AS TAVG, MAX(tobs) AS TMAX FROM measurement WHERE date BETWEEN '{start}' AND '{end}'"
    results = engine.execute(query).fetchall()
    
    # Convert to a list of dictionaries
    temperature_data = [{"TMIN": result.TMIN, "TAVG": result.TAVG, "TMAX": result.TMAX} for result in results]
    
    return jsonify(temperature_data)


if __name__ == '__main__':
    app.run(debug=True)