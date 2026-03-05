# Deployment Guide

## Overview

This guide covers deploying the Diabetic Ulcer AI System to production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Docker Deployment](#docker-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Monitoring and Logging](#monitoring-and-logging)
6. [Security Considerations](#security-considerations)
7. [Scaling](#scaling)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

- Docker & Docker Compose
- Kubernetes (v1.20+) for K8s deployment
- Helm (optional, for package management)
- kubectl configured with cluster access
- GPU nodes (optional, for inference acceleration)

## Docker Deployment

### Build Images

```bash
# Build backend image
docker build -t diabetic-ulcer-backend:latest ./backend

# Build frontend image
docker build -t diabetic-ulcer-frontend:latest ./frontend
```

### Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9090

## Kubernetes Deployment

### Prerequisites

```bash
kubectl create namespace diabetic-ulcer
```

### Deploy Backend

```bash
kubectl apply -f deployment/kubernetes/backend-deployment.yaml -n diabetic-ulcer
```

### Deploy Frontend

```bash
kubectl apply -f deployment/kubernetes/frontend-deployment.yaml -n diabetic-ulcer
```

### Create Services

```bash
# Backend service
kubectl expose deployment backend --type=LoadBalancer --port=8000 --target-port=8000

# Frontend service
kubectl expose deployment frontend --type=LoadBalancer --port=3000 --target-port=3000
```

### Check Status

```bash
kubectl get pods -n diabetic-ulcer
kubectl get services -n diabetic-ulcer
```

## Environment Configuration

### Backend Environment Variables

Create `.env` file in backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@postgres:5432/diabetic_ulcer
DB_ECHO=False

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Model Configuration
DEVICE=cuda
CONFIDENCE_THRESHOLD=0.5

# API
BACKEND_PORT=8000
DEBUG=False
LOG_LEVEL=INFO

# CORS
FRONTEND_URL=http://localhost:3000

# MLflow
MLFLOW_TRACKING_URI=http://mlflow:5000
MLFLOW_BACKEND_STORE_URI=postgresql://user:password@postgres:5432/mlflow
```

### Frontend Environment Variables

Create `.env` in frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## Monitoring and Logging

### Prometheus Metrics

Prometheus is configured to scrape metrics from:
- Backend: http://backend:8000/metrics
- Database: postgres_exporter:9187

### Grafana Dashboards

1. Access Grafana at http://localhost:3001
2. Add Prometheus as datasource
3. Import dashboard from `deployment/monitoring/grafana-dashboard.json`

### Application Logs

Logs are stored in:
- Backend: `logs/` directory
- Docker: `docker logs <container-id>`
- Kubernetes: `kubectl logs <pod-name>`

## Security Considerations

### API Security

- Enable HTTPS in production
- Use strong SECRET_KEY
- Implement rate limiting
- Apply authentication to all endpoints

### Database Security

- Use strong passwords
- Enable SSL connections
- Regular backups
- Principle of least privilege

### Container Security

- Scan images for vulnerabilities
- Use non-root users in containers
- Implement resource limits
- Use private container registries

### Network Security

- Use network policies in Kubernetes
- Configure firewall rules
- Use VPN for remote access
- Enable CORS only for trusted origins

## Scaling

### Horizontal Scaling

```bash
# Kubernetes - Scale backend replicas
kubectl scale deployment backend --replicas=3 -n diabetic-ulcer

# Docker - Use docker-compose scale
docker-compose up -d --scale backend=3
```

### Vertical Scaling

Increase resource limits in deployment manifests:

```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

### Load Balancing

- Kubernetes: Use Service type LoadBalancer
- Docker: Use Nginx reverse proxy
- Cloud: Use managed load balancer service

## Troubleshooting

### Common Issues

#### Backend won't start

```bash
# Check logs
docker logs <container-id>

# Verify environment variables
docker exec <container-id> env | grep -E "DATABASE|SECRET"

# Check database connectivity
docker exec <container-id> python -c "import app.db.database; print('DB OK')"
```

#### High latency on predictions

- Check GPU availability
- Monitor CPU/Memory usage
- Review model inference time
- Scale to additional pods

#### Database connection issues

```bash
# Verify database is running
docker ps | grep postgres

# Check connection string
docker exec <backend-container> ping postgres

# Test connection
psql -h postgres -U user -d diabetic_ulcer -c "SELECT 1"
```

#### Frontend blank page

- Check browser console for errors
- Verify API URL in `.env`
- Check CORS configuration
- Verify backend is running

### Health Checks

Backend health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "database": "connected",
  "models_loaded": true
}
```

### Performance Tuning

1. **Database Optimization**
   - Create indexes on frequently queried columns
   - Use connection pooling
   - Regular vacuum and analyze

2. **Model Optimization**
   - Use model quantization for faster inference
   - Implement batch processing
   - Cache predictions when possible

3. **API Optimization**
   - Enable gzip compression
   - Implement caching headers
   - Use async endpoints

4. **Infrastructure**
   - Use SSD storage
   - Enable memory caching (Redis)
   - Distribute across multiple zones

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Database credentials secured
- [ ] Secret keys generated
- [ ] SSL/TLS certificates obtained
- [ ] Monitoring configured
- [ ] Backups scheduled
- [ ] Disaster recovery plan
- [ ] Security scan completed
- [ ] Load testing performed
- [ ] Documentation updated

## Support

For issues and questions:
- Check logs: `docker logs [container]`
- Review API docs: `/docs` endpoint
- Contact DevOps team
- File GitHub issues

---

Last Updated: 2026-03-05
