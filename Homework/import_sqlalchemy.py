import sqlalchemy
import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
import numpy as np
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

#Measurement class
measurement = Base.classes.measurement
#station class
station = Base.classes.station

session = Session(engine)

#Beginning Flask
app = Flask(__name__)

#Beginning Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/id<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/date<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs</br>"  
        f"/api/v1.0/start</br>"  
        f"/api/v1.0/end"  
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(measurement.date, measurement.prcp).limit(20).all()

    session.close()
    returned = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        returned.append(prcp_dict)

    return jsonify(returned)

@app.route("/api/v1.0/stations")
def stations():

    results2 = session.query(measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results2))

    return jsonify(all_stations)
    session.close()
@app.route("/api/v1.0/tobs")
def tobs():
    days = datetime.timedelta(365)
    var = datetime.date(2017, 8 , 23) - days

# Perform a query to retrieve the data and precipitation scores
    results3 = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= var).all()
    return jsonify(results3)
    session.close()

@app.route("/api/v1.0/temps/<start_date>")
def start(start_date):
    results4= session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs).filter(measurement.date >= start_date)).all()

    session.close()
    return jsonify(results4)
    

@app.route("/api/v1.0/etemps/<starts_date>/<end_date>")
def end(starts_date, end_date):
    results5= session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs).filter(measurement.date >= starts_date).filter(measurement.date <= end_date)).all()


    return jsonify(results5)
    session.close()

if __name__ == '__main__':
    app.run(debug=True)