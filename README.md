# TempConverter DevOps project

This repository is a complete implementation package for the Intro to DevOps 2025/2026 project. It uses Docker Swarm as the simpler orchestration system and Kubernetes as the complex system.

## What is included

- A non-root Python image that updates OS packages, installs dependencies, exposes TCP 5000, and starts with Gunicorn.
- MySQL 8 local deployment with a non-root application database user.
- Podman Compose deployment.
- Unit tests, a container integration test, and a GitHub Actions test/build pipeline.
- Docker Swarm template: two app replicas on different nodes, one database replica, and ingress load balancing on port 80.
- Kubernetes template: two app replicas with required node anti-affinity, one database replica, and a LoadBalancer service on port 80.
- Resource-measurement helper, submission evidence checklist, troubleshooting log, and short video plan.

## 1. Configure local values

Copy `.env.example` to `.env`, then replace every placeholder. Keep `.env` private.

```powershell
Copy-Item .env.example .env
notepad .env
```

The supplied GitHub download is a ZIP without repository history. Create your own empty GitHub repository, then initialize and publish this folder:

```powershell
git init -b main
git add .
git commit -m "Complete TempConverter DevOps project"
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/tempconverter-devops.git
git push -u origin main
```

If Git asks for an identity, set your real `user.name` and `user.email` before committing.

## 2. Run locally with Podman

Install Podman Desktop and the `podman-compose` provider, start the Podman machine, then run:

```powershell
podman machine start
podman compose --env-file .env -f podman-compose.yml up --build -d
podman ps
podman logs tempconverter-main-app-1
```

Open <http://localhost:5000>, make a conversion, and confirm it appears in Recent Conversions. Verify the app connects as the non-root MySQL user:

```powershell
podman exec tempconverter-main-db-1 mysql -utempconverter -p -e "SELECT CURRENT_USER();" tempconverter
```

Container names can differ by Compose version; use `podman ps` to find the exact name. Stop with:

```powershell
podman compose --env-file .env -f podman-compose.yml down
```

## 3. Test

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q tests/test_app.py
docker compose -f compose.ci.yml up --build -d --wait
python -m pytest -q tests/integration_test.py
docker compose -f compose.ci.yml down -v
```

The same sequence is automated by `.github/workflows/pipeline.yml`.

## 4. Build and publish images

Sign in to Docker Hub, GHCR, or another registry. The first image in the assignment should be built from the original source and tagged `latest`; after the title change, build this source as `dev`.

```powershell
docker login ghcr.io
.\scripts\build-and-push.ps1 -Registry ghcr.io/YOUR_GITHUB_USERNAME -Tag dev
```

Confirm the pushed image exists in the registry UI and capture its tags/digests for the report. Update `REGISTRY_IMAGE` in `.env` and the Kubernetes image field to the real path.

## 5. Docker Swarm deployment

This needs at least two Swarm nodes to satisfy the different-node requirement. Label the chosen database node and deploy from a manager:

```powershell
docker node update --label-add tempconverter-db=true DATABASE_NODE_NAME
Get-Content .env | ForEach-Object { if ($_ -match '^([^#=]+)=(.*)$') { Set-Item -Path "env:$($matches[1])" -Value $matches[2] } }
docker stack deploy --with-registry-auth -c swarm/stack.yml tempconverter
docker stack services tempconverter
docker service ps tempconverter_app
```

The Swarm routing mesh publishes port 80 and balances requests across two app replicas. `max_replicas_per_node: 1` prevents both replicas from sharing a node. Scale to three replicas with:

```powershell
docker service scale tempconverter_app=3
```

Three replicas require at least three eligible nodes because of the one-replica-per-node rule.

## 6. Kubernetes deployment

Replace `YOUR_REGISTRY/tempconverter:dev` and all placeholder values in `kubernetes/tempconverter.yml`, then use a cluster with at least two schedulable worker nodes:

```powershell
kubectl apply -f kubernetes/tempconverter.yml
kubectl -n tempconverter rollout status deployment/mysql
kubectl -n tempconverter rollout status deployment/tempconverter
kubectl -n tempconverter get pods -o wide
kubectl -n tempconverter get service tempconverter
```

The required pod anti-affinity keeps the two app pods on different nodes. The LoadBalancer service exposes port 80. Scale to three replicas with:

```powershell
kubectl -n tempconverter scale deployment/tempconverter --replicas=3
kubectl -n tempconverter rollout status deployment/tempconverter
```

Again, three replicas need three eligible nodes. For a local cluster whose LoadBalancer stays pending, use `kubectl -n tempconverter port-forward service/tempconverter 8080:80` only as a test fallback; the submitted multi-node demonstration should use a functioning load balancer.

## 7. Finish the report and evidence

Use `docs/PROJECT_GUIDE.md` as the report-writing and evidence checklist. Enter real measurements in `docs/RESOURCE_COMPARISON.md`; do not invent values. Record actual problems and fixes in `docs/TROUBLESHOOTING.md`. Follow `docs/VIDEO_CHECKLIST.md` for the short demonstration.

The official project document template was not included with the assignment PDF. Copy the prepared material into the template from Infoeduka and place scripts/configuration files in its appendices before submission.
