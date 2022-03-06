from tracemalloc import start
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)




app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")

    return (
            f"Welcome to the API<br/>"
            f"Here are the possible routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f'/api/v1.0/tobs<br/>'
            f'/api/v1.0/start_date<br/>'
            f'/api/v1.0/start_date/end_date<br/>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    dict = []
    prcp = session.query(Measurement.date, Measurement.prcp).all()
    for row in prcp:
        dict.append(row._asdict())
    return jsonify(dict)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    dict = []
    stations = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    for row in stations:
        dict.append(row._asdict())
    return jsonify(dict)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Tobs' page...")
    recent_date = session.query(Measurement.date)\
                            .order_by(Measurement.date.desc()).limit(1).all()[0][0]

    most_recent = dt.datetime.strptime(recent_date, "%Y-%m-%d")
    one_year = str((most_recent-dt.timedelta(days=365)).date())

    dict = []
    tobs = session.query(Measurement.date, Measurement.tobs)\
                    .filter(Measurement.date >= one_year)\
                    .filter(Measurement.date <= recent_date)\
                    .filter_by(station = 'USC00519281').all()
    for row in tobs:
        dict.append(row._asdict())
    return jsonify(dict)

@app.route("/api/v1.0/<start>")
def starts(start):
    print("Server received request for 'Start' page...")
    dict = []

    min = session.query(func.min(Measurement.tobs))\
                    .filter(Measurement.date >= start).first()   

    for row in min:
        dict.append({"min":row})

    max = session.query(func.max(Measurement.tobs))\
                    .filter(Measurement.date >= start).first()   

    for row in max:
        dict.append({"max":row})

    avg = session.query(func.avg(Measurement.tobs))\
                    .filter(Measurement.date >= start).first()   

    for row in avg:
        dict.append({"avg":row})

    return jsonify(dict)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    print("Server received request for 'Start/End' page...")
    dict = []

    min = session.query(func.min(Measurement.tobs))\
                    .filter(Measurement.date >= start)\
                    .filter(Measurement.date <= end).first()   

    for row in min:
        dict.append({"min":row})

    max = session.query(func.max(Measurement.tobs))\
                    .filter(Measurement.date >= start)\
                    .filter(Measurement.date <= end).first()    

    for row in max:
        dict.append({"max":row})

    avg = session.query(func.avg(Measurement.tobs))\
                    .filter(Measurement.date >= start)\
                    .filter(Measurement.date <= end).first()     

    for row in avg:
        dict.append({"avg":row})
        
    return jsonify(dict)

session.close()

if __name__ == "__main__":
    app.run(debug=True)