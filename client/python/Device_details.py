import threading
import time
from database import db, SystemMetrics  # Import the db instance and SystemMetrics model
import psutil
from flask import Flask  # Import Flask if needed
import api_keys
import datetime

def record_metrics(user):
    app = Flask(__name__)  # Create a Flask app instance within the thread
    app.config['SQLALCHEMY_DATABASE_URI'] = api_keys.db_key
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():  # Use the app context from the Flask app within the thread
        while True:
            cpu_utilization = psutil.cpu_percent()
            ram_utilization = psutil.virtual_memory().percent
            disk_utilization = psutil.disk_usage('/').percent

            # Create a new SystemMetrics instance and save it to the database
            print('before db')
            new_metrics = SystemMetrics(user = user, cpu=cpu_utilization, ram=ram_utilization, disk=disk_utilization,tstamp=datetime.datetime.now())
            print('after new_metrics')
            db.session.add(new_metrics)
            db.session.commit()

            # Wait for 10 seconds before collecting metrics again
            time.sleep(10)


def utility(user):
    # Create a thread to run the record_metrics function
    thread = threading.Thread(target=record_metrics, args=(user,))
    thread.start()

    # Do other stuff while the background task is running

# Call utility to start the background thread