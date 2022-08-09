#Dependencies 
import datetime as dt
import numpy as np
import pandas as pd

#Dependencies for SQAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Dependencies for Flask
from flask import Flask, jsonify

#Access the SQLite Database
engine = create_engine("sqlite:///hawaii.sqlite")

#Function to access and query SQLite database
Base = automap_base()

#Reflect Database
Base.prepare(engine, reflect=True)

#Save Refrencest to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create Session Link
session = Session(engine)

#Set Up Flask
app = Flask(__name__)

#Define Welcome Route 
@app.route('/')

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#Define Precipitation Route
@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Defube Statuins Route
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
