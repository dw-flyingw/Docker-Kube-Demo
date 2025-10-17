# Start
minikube start
helm install docker-kube-demo ./helm/docker-kube-demo
kubectl get pods -l app.kubernetes.io/instance=docker-kube-demo
minikube service docker-kube-demo-frontend

# Stop
helm uninstall docker-kube-demo
minikube stop
