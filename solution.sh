# The sequence of commands to bring up our environment and application for the kubernetes cluster
# 1. Create the namespace for the application
kubectl apply -f kubernetes/app-namespace.yaml

# 2. Create the secrets for the application
kubectl apply -f kubernetes/secrets/mongo-secret.yaml
kubectl apply -f kubernetes/secrets/weather-secret.yaml

# 3. Create the configmap for the application
kubectl apply -f kubernetes/configmaps/mongo-config.yaml
# 4. Create the storage class for the application
kubectl apply -f kubernetes/storage/mongo-storageClass.yaml
# 5. Create the persistent volume for the application
kubectl apply -f kubernetes/storage/mongo-pv.yaml
# 6. Create the persistent volume claim for the application
kubectl apply -f kubernetes/storage/mongo-pvc.yaml
# 7. Create the deployment for the application
kubectl apply -f kubernetes/deployments/weather-app-deployment.yaml
# 8. Create the service for the application
kubectl apply -f kubernetes/services/weather-app-service.yaml
# 9. Create the headless service for the MongoDB database
kubectl apply -f kubernetes/services/mongo-headless-service.yaml
# 10. Create the statefulset for the MongoDB database
kubectl apply -f kubernetes/statefulsets/mongo-statefulset.yaml



