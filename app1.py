# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from datetime import datetime


#################################################
# Database Setup
#################################################
# Python SQL toolkit and Object Relational Mapper
app = Flask(__name__)

# Reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()


# Show the tables found in the database
print("Tables found in the database:", Base.classes.keys())

# Create a session to interact with the database
session = Session(engine)

# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)



#------------------------------------------------------------------------------------------------------------------
@app.route('/', methods = ['GET'])
def welcome():
    return 'hello'
#-----------------------------------------------------------------------------------------------------------------
@app.route('/dates', methods=['GET'])
def dates():
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = str(int(most_recent_date.split("-")[0]) - 1) + most_recent_date[4:]

    return jsonify({
        'Most_Recent_Date': most_recent_date,
        'One_Year_Ago': one_year_ago
    })

#------------------------------------------------------------------------------------------------------------
@app.route('/stations', methods=['GET'])
def stations():
    results = session.query(Station.name).all()
    station_names = list(np.ravel(results))
    return jsonify(station_names=station_names)

@app.route('/measurement_stations', methods=['GET'])
def measurement_stations():
    results = session.query(Measurement.station).distinct().all()
    measurement_stations = list(np.ravel(results))
    return jsonify(measurement_stations=measurement_stations)

#----------------------------------------------------------------------------------------------------------------
@app.route('/temperature_stats', methods=['GET'])
def temperature_stats():
    # Get list of unique stations
    stations = session.query(Measurement.station).distinct().all()
    stations = [station[0] for station in stations]

    # Initialize an empty list to store temperature statistics dictionaries
    all_stats = []

    # Loop through each station and calculate min, max, and average temperature
    for station in stations:
        stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.station == station).\
            all()[0]

        # Create a dictionary to store the statistics for the current station
        stats_dict = {
            "Station": station,
            "Min Temperature": stats[0],
            "Max Temperature": stats[1],
            "Average Temperature": stats[2]
        }

 # Append the dictionary to the list of all statistics
        all_stats.append(stats_dict)

    return jsonify(all_stats)

#------------------------------------------------------------
@app.route('/temperature_stats/<start_date>', methods=['GET'])
def temperature_stats_start(start_date):
    # Get list of unique stations
    stations = session.query(Measurement.station).distinct().all()
    stations = [station[0] for station in stations]

    # Initialize an empty list to store temperature statistics dictionaries
    all_stats = []

    # Loop through each station and calculate min, max, and average temperature since the start date
    for station in stations:
        stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.station == station).\
            filter(Measurement.date >= start_date).\
            all()[0]

        # Create a dictionary to store the statistics for the current station
        stats_dict = {
            "Station": station,
            "Min Temperature": stats[0],
            "Max Temperature": stats[1],
            "Average Temperature": stats[2]
        }

        # Append the dictionary to the list of all statistics
        all_stats.append(stats_dict)

    return jsonify(all_stats)


#------------------------------------------------------------------------------------------------------------------------------
@app.route('/all_temperature_stats', methods=['GET'])
def all_temperature_stats():
    # Assuming that Measurement is the table and tobs is the temperature column
    # and station is the station column

    # Query to get list of unique stations
    stations = session.query(Measurement.station).distinct().all()
    stations = [station[0] for station in stations]

    # Initialize an empty list to store temperature statistics dictionaries
    all_stats = []

    # Loop through each station and calculate min, max, and average temperature
    for station in stations:
        stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.station == station).\
            all()[0]

        # Create a dictionary to store the statistics for the current station
        stats_dict = {
            "Station": station,
            "Min Temperature": stats[0],
            "Max Temperature": stats[1],
            "Average Temperature": stats[2]
        }

        # Append the dictionary to the list of all statistics
        all_stats.append(stats_dict)

    return jsonify(all_stats)










   
if __name__ == '__main__':
    app.run(debug=True)