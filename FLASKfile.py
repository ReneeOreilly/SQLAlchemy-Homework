import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite",  connect_args={'check_same_thread':False})


Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/")
def home():
    print("Server recieved request for 'Home' page")
    return(
        f"Routes available:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipjson():
    print("Server recieved request for 'Precip' page")
    precips = session.query(Measurement.date, Measurement.prcp).\
    order_by(Measurement.date.desc()).\
    filter(Measurement.date > '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').all()
    return jsonify(precips)

@app.route("/api/v1.0/stations")
def stationsjson():
    print("Server recieved requet for 'Stations' page")
    count = func.count(Measurement.station).label('count')
    stations = session.query(count, Measurement.station).\
    group_by(Measurement.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobsjson():
    print("Server recieved request for 'tobs' page")
    temps = session.query(Measurement.date, Measurement.tobs).\
    order_by(Measurement.date.desc()).\
    filter(Measurement.date > '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').all()
    return jsonify(temps)


@app.route("/api/v1.0/<start>")
def start(start):
    start = dt.datetime.strptime(start,"%Y-%m-%d")
    startresults = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    return jsonify(startresults)   

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    start = dt.datetime.strptime(start,"%Y-%m-%d")
    end = dt.datetime.strptime(end,"%Y-%m-%d")
    seresults = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    return jsonify(seresults)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

