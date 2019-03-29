import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


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
        f"/api.v1.0/precipitation<br/>"
        f"/api.v1.0/stations<br/>"
        f"/api.v1.0/tobs<br/>"
        f"/api.v1.0/start<br/>"
        f"/api.v1.0/start/end<br/>"
    )

@app.route("/api.v1.0/precipitation")
def precipjson():
    print("Server recieved request for 'Precip' page")
    return jsonify(precips)

@app.route("/api.v1.0/stations")
def stationsjson():
    print("Server recieved requet for 'Stations' page")
    return jsonify(stationcount)

@app.route("/api.v1.0/tobs")
def tobsjson():
    print("Server recieved request for 'tobs' page")
    return jsonify(temps)


@app.route("/api/v1.0/<start>")
def start(start):
    start = dt.datetime.strptime(start, "%y-%m-%d")
    startresults = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    return jsonify(startresults)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    start = dt.datetime.strptime(start,"%y-%m-%d")
    end = dt.datetime.strptime(end,"%y-%m-%d")
    #end_date = dt.date(start) - dt.timedelta(days=365)
    seresults = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end_date).group_by(Measurement.date).all()
    return jsonify(seresults)

if __name__ == "__main__":
    app.run(port=5000, debug=False)

