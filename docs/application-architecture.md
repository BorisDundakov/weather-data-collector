# APPLICATION / CONTAINER FLOW

Local source code / repository

```
┌───────────────────────────────────────────────────────────────────────────┐
│ main.py                                                                   │
│ Kind: Python / Flask application                                          │
│                                                                           │
│ • Creates the Flask application                                           │
│ • Reads configuration from environment variables:                         │
│     os.getenv("XWEATHER_BASE_URL")                                        │
│     os.getenv("XWEATHER_CLIENT_ID")                                       │
│     os.getenv("XWEATHER_CLIENT_SECRET")                                   │
│     os.getenv("MONGO_HOST")                                               │
│     os.getenv("MONGO_PORT")                                               │
│     os.getenv("MONGO_DB")                                                 │
│     os.getenv("MONGO_USERNAME")                                           │
│     os.getenv("MONGO_PASSWORD")                                           │
│                                                                           │
│ • Calls XWeather API and receives weather data                            │
│ • Connects to MongoDB and stores/retrieves weather data                   │
│ • Passes data to index.html using render_template()                       │
└───────────────────────┬───────────────────────────────┬───────────────────┘
                        │                               │
                        │ render_template()             │ os.getenv()
                        ▼                               ▼
┌───────────────────────────────────┐     ┌──────────────────────────────────────┐
│ templates/index.html              │     │ Process Environment                  │
│ Kind: HTML / Jinja2 template      │     │                                      │
│                                   │     │ XWEATHER_BASE_URL                    │
│ • Receives data from main.py      │     │ XWEATHER_CLIENT_ID                   │
│ • Renders the weather webpage     │     │ XWEATHER_CLIENT_SECRET               │
│ • Served to the user's browser    │     │ MONGO_HOST                           │
│                                   │     │ MONGO_PORT                           │
│                                   │     │ MONGO_DB                             │
│                                   │     │ MONGO_USERNAME                       │
│                                   │     │ MONGO_PASSWORD                       │
└───────────────────────────────────┘     └──────────────────┬───────────────────┘
                                                            ▲
                                       ┌────────────────────┴────────────────────┐
                                       │                                         │
                                       │                                         │
                            LOCAL DEVELOPMENT                           KUBERNETES
                                       │                                         │
                     ┌─────────────────┴──────────────┐       ┌──────────────────┴──────────────────┐
                     │ .env                           │       │ Kubernetes resources                │
                     │ Kind: Local configuration      │       │                                     │
                     │                                │       │ weather-secrets (Secret)            │
                     │ XWEATHER_BASE_URL=...          │       │   ├─ XWEATHER_BASE_URL              │
                     │ XWEATHER_CLIENT_ID=...         │       │   ├─ XWEATHER_CLIENT_ID             │
                     │ XWEATHER_CLIENT_SECRET=...     │       │   └─ XWEATHER_CLIENT_SECRET         │
                     │                                │       │                                     │
                     │ MONGO_HOST=...                 │       │ mongo-config (ConfigMap)            │
                     │ MONGO_PORT=...                 │       │   ├─ MONGO_HOST                     │
                     │ MONGO_DB=...                   │       │   ├─ MONGO_PORT                     │
                     │ MONGO_USERNAME=...             │       │   └─ MONGO_DB                       │
                     │ MONGO_PASSWORD=...             │       │                                     │
                     │                                │       │ mongo-secret (Secret)               │
                     │ load_dotenv() loads these      │       │   ├─ MONGO_USERNAME                 │
                     │ into the process environment   │       │   └─ MONGO_PASSWORD                 │
                     │                                │       │                                     │
                     │ NOTE: Use .env.example as      │       │ Deployment uses envFrom to inject   │
                     │ reference when creating .env   │       │ them into container environment.    │
                     └────────────────────────────────┘       └─────────────────────────────────────┘
```

# CONTAINER IMAGE BUILD

> **Note:** The entire Kubernetes environment can be brought up from scratch using the `solution.sh` script.

```
┌──────────────────────────────────────┐
│ Application source                   │
│                                      │
│ main.py + templates + requirements   │
│ + Dockerfile                         │
│                                      │
│ .env is NOT included in the image    │
└───────────────────┬──────────────────┘
                    │
                    │ docker build
                    ▼
┌──────────────────────────────────────┐
│ weather-app Docker image             │
│                                      │
│ • Contains application + dependencies│
│ • Used by weather-app-deployment     │
│ • Secrets/ConfigMaps are injected    │
│   by Kubernetes at runtime           │
└──────────────────────────────────────┘
```