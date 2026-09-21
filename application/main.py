from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

# Load environment variables from .env file
# In Kubernetes, environment variables are injected directly via Secret/ConfigMap, so the line below is not neccessary.
load_dotenv()

# Initialize Flask application
app = Flask(__name__, template_folder="templates")

# Initialize logger
logger = logging.getLogger(__name__)

# XWeather API configuration. Retrieve data from either .env file or Kubernetes Secret/ConfigMap.
BASE_URL = os.getenv("XWEATHER_BASE_URL")
CLIENT_ID = os.getenv("XWEATHER_CLIENT_ID")
CLIENT_SECRET = os.getenv("XWEATHER_CLIENT_SECRET")

# MongoDB configuration
# from kubernetes configmap mongo-configmap.yaml
MONGO_DB = os.getenv("MONGO_DB")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")

# from kubernetes secret mongo-secret.yaml
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

MONGO_URI= (
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
)

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["weather"]
weather_collection = db["weather_data"]


def get_nyc_weather():
    response = requests.get(
        f"{BASE_URL}client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    )

    return response.json()


def store_weather_data_to_mongo(weather_data):
    # upload retrieved weather data from get_nyc_weather() func to MongoDB database
    weather = weather_data["response"][0]
    period = weather["periods"][0]

    weather_data = {
        "location": weather["place"]["name"],
        "temperature": period["tempC"],
        "wind": period["windSpeedKPH"],
        "humidity": period["humidity"],
        "timestamp": period["timestamp"]
    }
 
    # Save a weather data to MongoDB collection
    try:
        result = weather_collection.insert_one(weather_data)   
        logger.info(f"Mongo insert successful: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Error occurred while inserting into MongoDB: {e}")


@app.route("/")
def index():
    weather_data = get_nyc_weather()

    # store the weather data to MongoDB
    store_weather_data_to_mongo(weather_data)

    # format data for index.html template
    location = weather_data["response"][0]["place"]["name"]
    temperature = weather_data["response"][0]["periods"][0]["tempC"]
    wind = weather_data["response"][0]["periods"][0]["windSpeedKPH"]
    humidity = weather_data["response"][0]["periods"][0]["humidity"]
    timestamp = weather_data["response"][0]["periods"][0]["timestamp"]

    display_data = {
        "location": location,
        "temperature": temperature,
        "wind": wind,
        "humidity": humidity,
        "timestamp": timestamp
    }

    return render_template("index.html", weather=display_data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)