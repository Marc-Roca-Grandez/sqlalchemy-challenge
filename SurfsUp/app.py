import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
#Base.metadata.tables
Base.classes.keys()
# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def home():
    #"""List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return the list of the past 12 months of precipitation"""
    #last 12 months
    #date_search = "2016-08-23"
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").all()
    session.close()
    #dictionary
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station, station.name, station.longitude, station.id, station.latitude, station.elevation).all()
    session.close()
    all_stations = []
    for station,name,longitude,id,latitude,elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["longitude"] = longitude
        station_dict["id"] = id
        station_dict["latitude"] = latitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    ##Still need to fix date search
    session = Session(engine)
    dates = session.query(measurement.date).order_by(measurement.date.desc()).first()
    date_search = dates[0]
    results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= date_search).all()
    session.close()
    all_tobs = []
    for date,tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
    filter(measurement.date >= start).all()
    session.close()
    all_start = []
    for tmin,tavg,tmax in results:
        start_dict = {}
        start_dict["tmin"] = tmin
        start_dict["tavg"] = tavg
        start_dict["tmax"] = tmax
        all_start.append(start_dict)
    return jsonify(all_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
    filter(measurement.date >= start and measurement.date <= end ).all()
    session.close()
    all_range = []
    for tmin,tavg,tmax in results:
        range_dict = {}
        range_dict["tmin"] = tmin
        range_dict["tavg"] = tavg
        range_dict["tmax"] = tmax
        all_range.append(range_dict)
    return jsonify(all_range)

if __name__ == '__main__':
    app.run(debug=True)