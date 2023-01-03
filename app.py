from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

#-----------------
# Database Setup |
#-----------------
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

Measurements = Base.classes.measurement
Stations = Base.classes.station


#--------------
#  Home Page  |
# #------------
@app.route("/")
def index():
    return(
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/prcp<br/>"
        f"/api/stations<br/>"
        f"/api/tobs<br/>"
        f"<br/>Entering in a date will return the highest, lowest, and average temperatures between the interval of the specified start date and the most recent date.<br/>"
        f"ex:<br/>"
        f"/api/2017-08-13<br/>"
        f"<br/>Returns:<br/>"
        f"Lowest Temperature: 70.0<br/>"
        f"Highest Temperature: 85.0<br/>" 
        f"Average Temperature: 78.475<br/>"
        f"<br/>Entering in a set of dates separated by '/' will return the highest, lowest, and average temperature in the date ranges provided."
        f"<br/>ex:"
        f"/api/2017-08-03/2017-08-10<br/>"
        f"<br/>Returns:<br/>"
        f"Lowest Temperature: 71.0<br/>"
        f"Highest Temperature: 83.0<br/>" 
        f"Average Temperature: 79.61<br/>"
    )
    
#--------------------
# Precipation route |
#--------------------
@app.route("/api/prcp")
def prcp():
    session = Session(engine)

#filtering for most recent year of prcp data, excluding nulls
    prcp_data = session.query(Measurements.date,Measurements.prcp).\
    filter(Measurements.date >= "2016-08-23").\
        filter(Measurements.prcp != None).\
        order_by(Measurements.date).all()
    
    session.close()

#creating dictionaries using the prcp_data query results and adding to a list
    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

#----------------
# Station route |
#----------------
@app.route("/api/stations")
def stations():
    session = Session(engine)

    station_data = session.query(Stations.station,Stations.name,Stations.latitude,Stations.longitude,Stations.elevation)

    session.close()

#creating dictionaries with results from station_data query results and appending them to a list
    station_list = []
    for station, name, lat, lng, elv8 in station_data:
        station_dict = {}
        station_dict['ID'] = station
        station_dict['Name'] = name
        station_dict['Lat'] = lat
        station_dict['Lng'] = lng
        station_dict['Elevation'] = elv8
        station_list.append(station_dict)
    
    return jsonify(station_list)

#--------------------
# Temperature route |
#--------------------
@app.route("/api/tobs")
def tobs():
    session = Session(engine)

    tobs_data = session.query(Measurements.date,Measurements.tobs).\
        filter(Measurements.station == 'USC00519281').\
            filter(Measurements.date >= "2016-08-18").\
            order_by(Measurements.date).all()

    session.close()

    tobs_list = []
    for date, temp in tobs_data:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Temperature'] = temp
        tobs_list.append(tobs_dict)
    
    return jsonify(tobs_list)

#---------------------------
# Dynamic, Start Date Only |
#---------------------------
@app.route("/api/<start_date>")
def temp_stats_1(start_date):

    session = Session(engine)

    temp_stats = session.query(func.min(Measurements.tobs),func.max(Measurements.tobs),func.avg(Measurements.tobs)).\
        filter(Measurements.date > start_date).all()

    session.close()
    
    try: 
        return (
        f"Lowest Temperature: {temp_stats[0][0]}<br/>"
        f"Highest Temperature: {temp_stats[0][1]}<br/>"
        f"Average Temperature: {round(temp_stats[0][2],2)}"
    )
    except TypeError:
        return (
            f"Oop, that date is outside the data.<br/>"
            f"The most recent data point was recorded on 2017-08-23, try a date before that!"
        )


    

#-------------------------------
# Dynamic, Start Date/End Date |
#-------------------------------

@app.route("/api/<start_date>/<end_date>")
def temp_stats_2(start_date, end_date):
    session = Session(engine)

    temp_stats = session.query(func.min(Measurements.tobs),func.max(Measurements.tobs),func.avg(Measurements.tobs)).\
        filter(Measurements.date >= start_date).\
            filter(Measurements.date <= end_date).all()

    session.close()

    try: 
        return (
        f"Lowest Temperature: {temp_stats[0][0]}<br/>"
        f"Highest Temperature: {temp_stats[0][1]}<br/>"
        f"Average Temperature: {round(temp_stats[0][2],2)}"
    )
    except TypeError:
        return (
            f"Oop, that date is outside the data.<br/>"
            f"The most recent data point was recorded on 2017-08-23, try some dates before that!"
        )


if __name__ == "__main__":
    app.run(debug=True)