import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
##########################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurements
Station = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
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

	results_date_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-01', Measurement.date < '2017-08-23').order_by(Measurement.date).group_by(Measurement.date).all()

    precipitation_data = []

    for precipitation in results_date_prcp:
    	precipitation_dict = {}
    	precipitation_dict["date"] = Measurement.date
    	precipitation_dict["prcp"] = Measurement.prcp
    	precipitation_data.append(precipitation_dict)
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():

    results_stations = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results_stations))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    results_high_tobs_year = session.query(Measurement.tobs).\
    filter(Measurement.date >= '2016-08-01', Measurement.date <= '2017-08-23').all()
    
    all_tobs = list(np.ravel(results_high_tobs))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start_only(start):

    results_calc = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    start_only_calc = list(np.ravel(results_calc))

    return jsonify(start_only_calc)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):

    results_calc = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start, Measurement.date <= end).all()

    start_and_end_calc = list(np.ravel(results_calc))

    return jsonify(start_and_end_calc)

if __name__ == '__main__':
    app.run(debug=True)
