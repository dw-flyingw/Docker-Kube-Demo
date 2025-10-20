# Deployment Guide to Kubernetes

This guide provides step-by-step instructions to deploy the `docker-kube-demo` application to a Kubernetes cluster using Docker and Helm.

## Prerequisites

Before you begin, ensure you have the following:

1.  **Kubernetes Cluster:** Access to a running Kubernetes cluster (e.g., Minikube, Kind, GKE, EKS, AKS, or a self-managed cluster).
2.  **`kubectl`:** The Kubernetes command-line tool installed and configured to connect to your cluster. Verify with `kubectl get nodes`.
3.  **Helm:** The Helm CLI installed on your machine.
4.  **Docker:** Docker installed and running on your machine.
5.  **Container Registry Account:** An account with a container registry (e.g., Docker Hub, Google Container Registry, AWS ECR) to store your Docker images.

## Deployment Steps

### Step 0: Stop Local Docker Compose Services (if running)

If you have the application running locally via Docker Compose, stop it to free up ports and avoid conflicts.

```bash
docker compose down
```

### Step 1: Build Docker Images

Build the Docker images for your frontend and backend services. This ensures your latest code is packaged into the containers.

```bash
docker compose build
```

### Step 2: Tag and Push Docker Images to a Container Registry

You need to push your Docker images to a container registry that your Kubernetes cluster can access. Replace `your-dockerhub-username` with your actual Docker Hub username (or the path to your chosen registry).

1.  **Login to your Docker Registry:**
    If using Docker Hub:
    ```bash
    docker login
    ```
    For other registries, consult their specific login instructions.

2.  **Tag and Push Backend Image:**
    ```bash
docker tag docker-kube-demo-backend your-dockerhub-username/docker-kube-demo-backend:latest
docker push your-dockerhub-username/docker-kube-demo-backend:latest
    ```

3.  **Tag and Push Frontend Image:**
    ```bash
docker tag docker-kube-demo-frontend your-dockerhub-username/docker-kube-demo-frontend:latest
docker push your-dockerhub-username/docker-kube-demo-frontend:latest
    ```

    **Important:** If you use a private registry, ensure your Kubernetes cluster has the necessary credentials (ImagePullSecrets) configured to pull images from it.

### Step 3: Update Helm Chart Values

Modify the `values.yaml` file in your Helm chart to point to the images you just pushed to your container registry.

1.  **Open `helm/docker-kube-demo/values.yaml` for editing.**
    You can use a text editor (e.g., `nano helm/docker-kube-demo/values.yaml` or open it in your IDE).

2.  **Modify the `repository` fields:**
    Update the `repository` fields under `backend.image` and `frontend.image` to reflect the full path to your images in the container registry.

    Example `values.yaml` snippet (with your actual username):
    ```yaml
    # ... other values ...
    backend:
      image:
        repository: your-dockerhub-username/docker-kube-demo-backend # <--- UPDATE THIS
        tag: latest
        pullPolicy: IfNotPresent
      service:
        type: ClusterIP
        port: 8000

    frontend:
      image:
        repository: your-dockerhub-username/docker-kube-demo-frontend # <--- UPDATE THIS
        tag: latest
        pullPolicy: IfNotPresent
      service:
        type: LoadBalancer # Use LoadBalancer to expose the frontend externally
        port: 8501
    # ... other values ...
    ```

3.  **Consider `frontend.service.type`:**
    *   For cloud Kubernetes services (GKE, EKS, AKS), `LoadBalancer` is typically correct for external access.
    *   For local Kubernetes clusters (Minikube, Kind) without a LoadBalancer provisioner, change `type: LoadBalancer` to `type: NodePort` to access the frontend via a node's IP and a high-numbered port.

### Step 4: Deploy or Upgrade the Helm Chart to Kubernetes

Ensure your `kubectl` is configured to the correct Kubernetes cluster context. You can check your current context with `kubectl config current-context`.

1.  **Navigate to the project root directory.**

2.  **To install the application for the first time:**
    ```bash
    helm install docker-kube-demo ./helm/docker-kube-demo
    ```
    This command deploys your application to the Kubernetes cluster under a Helm release named `docker-kube-demo`.

3.  **To upgrade an existing deployment (after making code changes, pushing new images, or updating the Helm chart):**
    ```bash
    helm upgrade docker-kube-demo ./helm/docker-kube-demo
    ```
    This command updates your existing deployment with the new image references and any changes in your Helm chart.

### Step 5: Verify the Deployment on Kubernetes

After deploying, verify that your application components are running correctly in the Kubernetes cluster.

1.  **Check Pods:**
    ```bash
    kubectl get pods
    ```
    You should see pods for both `docker-kube-demo-backend` and `docker-kube-demo-frontend` in a `Running` state.

2.  **Check Services:**
    ```bash
    kubectl get services
    ```
    Look for the `docker-kube-demo-frontend` service.
    *   If `type: LoadBalancer`, it might take a few moments for an `EXTERNAL-IP` to be assigned. Keep running `kubectl get services` until an IP appears.
    *   If `type: NodePort`, you'll need to get the IP of one of your cluster nodes (`kubectl get nodes -o wide`) and the `NodePort` assigned to the frontend service (e.g., `3xxxx`).

3.  **Access the Frontend:**
    Once you have the `EXTERNAL-IP` (for LoadBalancer) or Node IP and NodePort, you can access your Streamlit application in your web browser. For example, if the external IP is `XXX.XXX.XXX.XXX`, you would go to `http://XXX.XXX.XXX.XXX:8501`.

---

## DEMO PORTAL
https://hpedemoportal.ext.hpe.com/home
https://hpedemoportal.ext.hpe.com?demoid=9303
