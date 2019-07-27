import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine,reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Precipitation Data"""
    percp_data = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>'2016-08-23').all()

    percp_list = list(np.ravel(percp_data))

    return jsonify(percp_list)

@app.route("/api/v1.0/stations")
def stations():
    """Station Names"""
    stations = session.query(Station.station).all()
    station_list = list(np.ravel(stations))

    print(len(station_list))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Temperature Data"""
    tobs_data = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > '2016-08-23').all()
    tobs_list = list(np.ravel(tobs_data))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    start_data = session.query(Measurement.tobs).filter(Measurement.date > start).all()
    start_list = list(np.ravel(start_data))
    start_max = max(start_list)
    start_min = min(start_list)
    start_avg = sum(start_list)/len(start_list)
    return jsonify([start_max,start_min,start_avg])
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    start_data = session.query(Measurement.tobs).filter(Measurement.date > start).filter(Measurement.date < end).all()
    start_list = list(np.ravel(start_data))
    start_max = max(start_list)
    start_min = min(start_list)
    start_avg = sum(start_list)/len(start_list)
    return jsonify([start_max,start_min,start_avg])

if __name__ == '__main__':
    app.run(debug=True)

