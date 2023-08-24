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





#################################################
# Flask Routes
#################################################
# New flask route
@app.route('/', methods = ['GET'])
def welcome():
    return 'hello'

#---------------------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------
@app.route('/dates', methods=['GET'])
def dates():
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = str(int(most_recent_date.split("-")[0]) - 1) + most_recent_date[4:]

    return jsonify({
        'Most_Recent_Date': most_recent_date,
        'One_Year_Ago': one_year_ago
    })
#----------------------------------------------------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------------------
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

#--------------------------------------------------------------------------------------------
#-- Precipitation routes
@app.route('/precipitation', methods=['GET'])
def precipitation():
    # Query to retrieve the date and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    # Create a dictionary from the row data and append to a list
    precip_data = {}
    for date, prcp in results:
        precip_data[date] = prcp
    
    return jsonify(precip_data)

@app.route('/precipitation_last_year', methods=['GET'])
def precipitation_last_year():
    # Query to find the most recent date in the dataset
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = (datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Query to retrieve the date and precipitation values for the last year
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    
    # Create a dictionary from the row data
    precip_data = {}
    for date, prcp in results:
        precip_data[date] = prcp
    
    return jsonify(precip_data)

#------------------------------------------------------------------------------------------------------------------
#-- Stations Route
@app.route('/stations', methods=['GET'])
def stations():
    # Query all stations from the Station table
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    # Create a list of dictionaries to hold station information
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        all_stations.append(station_dict)
    
    return jsonify(all_stations)

#---------------------------------------------------------------------------------------------------------
# tobs route most active station
@app.route('/tobs', methods=['GET'])
def tobs():
    # Most active station ID
    most_active_station = 'USC00519281'

    # Query to get the most recent date for the most active station
    most_recent_date = session.query(Measurement.date).filter(Measurement.station == most_active_station).order_by(Measurement.date.desc()).first()[0]

    # Calculate the date one year from the last date in data set
    one_year_ago = str(int(most_recent_date.split("-")[0]) - 1) + most_recent_date[4:]

    # Query to get temperature observations for the most active station for the last year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date >= one_year_ago).all()

    # Create a list of dictionaries to hold TOBS information
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route('/tobs_last_year', methods=['GET'])
def tobs_last_year():
    # Most active station ID
    most_active_station = 'USC00519281'

    # Query to get the most recent date for the most active station
    most_recent_date = session.query(Measurement.date).filter(Measurement.station == most_active_station).order_by(Measurement.date.desc()).first()[0]

    # Calculate the date one year from the last date in data set
    one_year_ago = str(int(most_recent_date.split("-")[0]) - 1) + most_recent_date[4:]

    # Query to get temperature observations for the most active station for the last year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date >= one_year_ago).all()

    # Create a list of dictionaries to hold TOBS information
    last_year_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        last_year_tobs.append(tobs_dict)

    return jsonify(last_year_tobs)

#---------------------------------------------------------------------------------------------------------------------------
#-- Start route
@app.route('/start/<start_date>', methods=['GET'])
def start_route(start_date):
    # Query to get the min, max, and avg temperature from the start_date to the end of the dataset
    stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    # Create a dictionary to hold the statistics
    temp_stats = {}
    temp_stats['Start Date'] = start_date
    temp_stats['TMIN'] = stats[0][0]
    temp_stats['TMAX'] = stats[0][1]
    temp_stats['TAVG'] = stats[0][2]
    
    return jsonify(temp_stats)

@app.route('/start/<start_date>', methods=['GET'])
def temperature_stats_from_start(start_date):
    # Query to get the min, max, and average temperatures from the given start date to the end of the dataset
    temp_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # Create a dictionary to hold the temperature stats and return it as JSON
    temp_dict = {
        'Start Date': start_date,
        'Min Temperature': temp_stats[0][0],
        'Max Temperature': temp_stats[0][1],
        'Avg Temperature': temp_stats[0][2]
    }
    
    return jsonify(temp_dict)
   






if __name__ == '__main__':
    app.run(debug=True)