```
namespace = weather-data-collector

┌──────────────────────────────┐     ┌──────────────────────────────────────────┐     ┌──────────────────────────────────────┐
│ mongo-storageclass           │     │ mongo-statefulset                        │     │ weather-secret                       │
│ Kind: StorageClass           │     │ Kind: StatefulSet                        │     │ Kind: Secret                         │
│                              │     │                                          │     │                                      │
│ • Type: Local Storage        │     │ • Claims mongo-pvc                       │     │ • Contains API_KEY, URL and          │
│ • Defines StorageClass used  │     │ • Attaches PVC to mongo-container        │     │   CLIENT_SECRET                      │
│   for MongoDB storage        │     │ • PVC mounted at /data/db                │     │ • Required for weather API call      │
└──────────────┬───────────────┘     │ • MongoDB listens on port 27017          │     └──────────────────┬───────────────────┘
               │                     │ • Provides persistent MongoDB storage    │                        │
               ▼                     └──────────────────┬───────────────────────┘                        │ references
┌──────────────────────────────┐                        │                                                ▼
│ mongo-pv                     │                        │                               ┌───────────────────────────────────────┐
│ Kind: PersistentVolume       │                        │                               │ weather-app-deployment                │
│                              │                        │                               │ Kind: Deployment                      │
│ • Size: 6Gi                  │                        │                               │                                       │
│ • Type: Local Storage        │                        │                               │ • App listens on port 5000            │
│ • Host path:                 │                        │                               │ • Connects to MongoDB on port 27017   │
│   /mnt/data/weather-data-    │                        │                               │ • References 'weather-secret'         │
│   collector/mongo-db         │                        │                               │ • References 'mongo-config'           │
└──────────────┬───────────────┘                        │                               │ • Retrieves weather data via API      │
               │                                        │                               └────────────────┬──────────┬───────────┘
               ▼                                        │                                                │          │
┌──────────────────────────────┐                        │                                      references│          │ selected by
│ mongo-pvc                    │                        │                                                ▼          ▼
│ Kind: PersistentVolumeClaim  │                        │                         ┌───────────────────────┐  ┌───────────────────────┐
│                              │                        │                         │ mongo-config          │  │ weather-app-service   │
│ • Requests: 6Gi              │                        │                         │ Kind: ConfigMap       │  │ Kind: Service         │
│ • Claims 6Gi out of 6Gi      │                        │                         │                       │  │                       │
│   available in mongo-pv      │                        │                         │ • Stores MongoDB URL: │  │ • Type: NodePort      │
│ • Uses mongo-storageclass    │                        │                         │   mongodb://mongo-    │  │ • port: 5000          │
└──────────────────────────────┘                        │                         │   headless-service:   │  │ • targetPort: 5000    │
                                                        │                         │   27017               │  │ • Selects weather-app │
                                                        │                         └───────────┬───────────┘  │   Pods                │
                                                        │                                     │              └───────────────────────┘
                                                        │                                     │
                                                        │                                     │ DNS lookup:
                                                        │                                     │ mongo-headless-service
                                                        ▼                                     ▼
                                      ┌────────────────────────────────────────────────────────┐
                                      │ mongo-headless-service                                 │
                                      │ Kind: Service                                          │
                                      │                                                        │
                                      │ • Headless Service → ClusterIP: None                   │
                                      │ • Exposes MongoDB on port 27017                        │
                                      │ • Selects MongoDB StatefulSet Pod(s) by their labels   │
                                      │ • Does NOT provide one virtual ClusterIP               │
                                      │ • Kubernetes DNS resolves the Service name directly    │
                                      │   to the IP address(es) of its MongoDB Pod(s)          │
                                      │                                                        │
                                      │ Example:                                               │
                                      │ mongo-headless-service → 10.244.0.15 (mongo-0)         │
                                      └────────────────────────────┬───────────────────────────┘
                                                                   │
                                                                   │ traffic goes directly
                                                                   │ to selected MongoDB Pod
                                                                   ▼
                                      ┌────────────────────────────────────────────────────────┐
                                      │ mongo-0                                                │
                                      │ MongoDB Pod created by StatefulSet                     │
                                      │                                                        │
                                      │ Pod IP example: 10.244.0.15                            │
                                      │ MongoDB listens on: 27017                              │
                                      │                                                        │
                                      │ Receives connection from weather-app                   │
                                      └────────────────────────────────────────────────────────┘
```