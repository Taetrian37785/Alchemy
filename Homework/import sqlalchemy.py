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

#Beginning Flask
app = Flask(__name__)

#Beginning Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/id<br/>"
        f"/api/v1.0/station"
        f"/api/v1.0/date<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/tobs"
        
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()
        returned = []
        for date, prcp in results:
            prcp_dict = {}
            passenger_dict["date"] = prcp
            returned.append(prcp_dict)

    return jsonify(prcp_dict)


if __name__ == '__main__':
    app.run(debug=True)