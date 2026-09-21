# Weather Data Collector

**Version 2.0.0**

Weather Data Collector is a Kubernetes-based project consisting of a Python/Flask web application and a MongoDB database.

The application retrieves weather data for New York City from the XWeather API, displays the current data on a simple web page, and stores the retrieved data in MongoDB.

The primary focus of this project is the **containerized and Kubernetes infrastructure** rather than the visual presentation of the weather data.

**Docker image:** `borisdundakov/weather-data-collector:2.0.0`

## What the application does

- Retrieves NYC weather data from the XWeather API.
- Extracts location, temperature, wind speed, humidity, and timestamp.
- Displays the retrieved data using a simple Flask HTML template.
- Stores every retrieved weather record in MongoDB.
- Uses Kubernetes Secrets for sensitive configuration such as API and database credentials.

## MongoDB

MongoDB provides persistent storage for the weather data retrieved by the application.

- A new API request is currently triggered whenever the application page is refreshed.
- Each API response is stored as a MongoDB document.
- Stored data includes:
  - Location
  - Temperature
  - Wind speed
  - Humidity
  - Timestamp
- MongoDB runs as a Kubernetes StatefulSet with persistent storage.
- The application connects to MongoDB using a dedicated application user rather than the MongoDB root user.
- Database credentials are provided to the application through a Kubernetes Secret.

## Architecture

More detailed explanations of the application and Kubernetes infrastructure are available here:

- [Application Architecture](docs/application-architecture.md)
- [Kubernetes Architecture](docs/kubernetes-architecture.md)

## How to run the solution

### Prerequisites

Make sure the following are installed and configured:

- Docker
- `kubectl`
- Minikube

Start Minikube if it is not already running:

```bash
minikube start
```

### Configure secrets

Create the following files:

```text
weather-secret.yaml
mongo-secret.yaml
```

Use their corresponding `.example.yaml` files as templates and provide the required credentials.

Do not commit the actual Secret files containing credentials to the repository.

### Bring up the environment

The entire Kubernetes environment can be brought up from scratch using the `solution.sh` script.

Make the script executable:

```bash
chmod +x solution.sh
```

Then run:

```bash
./solution.sh
```

The script deploys the resources required by the application and MongoDB environment.

## Preview

![Application preview](images/python-web-app.png)
