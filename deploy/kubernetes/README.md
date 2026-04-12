# Kubernetes deployment guide

## Prerequisites

- A Kubernetes cluster (1.26+) with:
  - [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
  - [cert-manager](https://cert-manager.io/) (for automated TLS)
  - Prometheus scraping enabled (for `/metrics`)
- A reachable Neo4j instance (in-cluster or external)
- `kubectl` connected to the target cluster

---

## Apply order

Apply manifests in this exact order so dependencies (ConfigMap, Secret) are
present before the Deployment references them.

```bash
# 1. Network isolation
kubectl apply -f networkpolicy.yaml

# 2. Config and secrets (edit secret.example.yaml → secret.yaml first)
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml        # NOT secret.example.yaml

# 3. Workload
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 4. Autoscaling + disruption budget
kubectl apply -f hpa.yaml
kubectl apply -f pdb.yaml

# 5. TLS certificate (cert-manager must be installed)
kubectl apply -f certificate.yaml

# 6. Ingress (edit hostname in ingress.yaml first)
kubectl apply -f ingress.yaml
```

---

## Prepare the secret

```bash
# Copy the example, fill real values, apply — never commit secret.yaml to git
cp secret.example.yaml secret.yaml
# Edit WAGGLE_NEO4J_USERNAME and WAGGLE_NEO4J_PASSWORD
kubectl apply -f secret.yaml
```

---

## Replace the image reference

`deployment.yaml` uses `waggle-mcp:latest` as a placeholder.
Push your image to a registry and update the field:

```bash
# Example using Docker Hub
docker build -t yourorg/waggle-mcp:v0.1.0 .
docker push yourorg/waggle-mcp:v0.1.0
# Then update deployment.yaml:  image: yourorg/waggle-mcp:v0.1.0
kubectl apply -f deployment.yaml
```

---

## Verify the deployment

```bash
# Watch pods come up
kubectl rollout status deployment/waggle

# Check health endpoints via port-forward
kubectl port-forward svc/waggle 8080:80
curl http://localhost:8080/health/ready
curl http://localhost:8080/health/live
curl http://localhost:8080/metrics

# Check HPA status after a few minutes
kubectl get hpa waggle
```

---

## Verify the Ingress and TLS

```bash
# After DNS is pointed at the ingress controller's external IP:
curl -v https://waggle.example.com/health/ready

# Check cert-manager issued the certificate
kubectl describe certificate waggle-tls
kubectl get certificaterequest
```

---

## Rollback

```bash
kubectl rollout undo deployment/waggle
# Or to a specific revision:
kubectl rollout undo deployment/waggle --to-revision=2
```

---

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Pods stuck in `Pending` | `kubectl describe pod <name>` → resource limits, node capacity |
| Readiness probe failing | `kubectl logs <pod>` — embedding model may still be downloading |
| TLS certificate not issued | `kubectl describe certificate waggle-tls` → cert-manager events |
| 401 from `/mcp` | Ensure `X-API-Key` header is set to a valid active key |
| Rate-limit 429 from `/mcp` | Adjust `WAGGLE_RATE_LIMIT_RPM` in configmap.yaml |
