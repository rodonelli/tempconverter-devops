# Project report and evidence guide

Use the official Infoeduka project template for the final document. This file supplies the technical content and the evidence list; add your own screenshots, registry URL, measurements, and troubleshooting experience.

## 1. Container image

Explain that the image uses Python 3.12 slim, updates Debian packages during the build, installs Python requirements, exposes TCP 5000, runs as the unprivileged `app` user, and starts the Flask application through Gunicorn. Include the `Dockerfile` in the appendix.

Evidence to capture:

1. Successful image build and `docker image inspect` showing port 5000 and user `app`.
2. Registry page showing `tempconverter:latest`.
3. Browser before the title update, then source diff and registry page showing `tempconverter:dev`.
4. Browser developer tools or page source showing `<title>TempConverter</title>`.

## 2. Local Podman deployment and tests

Describe the two services in `podman-compose.yml`. MySQL creates `tempconverter`, a non-root account used by the app. Only the web port is published. The named volume preserves database data. Health checks and retry logic handle startup ordering.

Evidence to capture:

1. `podman ps` with healthy app and MySQL containers.
2. Browser showing your real name and college.
3. A submitted conversion and its database-backed history row.
4. `SELECT CURRENT_USER();` proving the app user is not root.
5. Unit and integration test output.
6. GitHub Actions green pipeline page.

## 3. Resource comparison

Follow `RESOURCE_COMPARISON.md`. Capture raw measurements under comparable idle and load conditions. Explain that containers share the host kernel, while a VM reserves resources for a guest OS, but let your actual figures support the conclusion.

## 4. Choice of orchestration systems

Docker Swarm was chosen as the simple option because its Compose-like stack format, built-in routing mesh, and small operational surface make it quick to run for a small team. Kubernetes was chosen as the complex option because its declarative API, ecosystem, health management, scheduling constraints, and cloud portability fit larger environments.

## 5. Docker Swarm

The stack has one MySQL replica and two app replicas. The ingress routing mesh publishes port 80 and uses the virtual-IP endpoint mode. `max_replicas_per_node: 1` places each app task on a different node. A node label pins the stateful database to the intended host.

Evidence to capture:

1. All Swarm nodes as Ready.
2. `docker stack services tempconverter` showing 1/1 database and 2/2 app.
3. `docker service ps tempconverter_app` showing different nodes.
4. Browser access through port 80.
5. Scale command and 3/3 state on three nodes.

## 6. Kubernetes

The manifest defines a namespace, configuration, secrets, storage, one MySQL Deployment and ClusterIP Service, and a two-replica app Deployment. Required pod anti-affinity spreads app replicas across hostnames. Readiness and liveness probes use `/healthz`. A LoadBalancer Service maps external port 80 to container port 5000.

Evidence to capture:

1. Cluster nodes as Ready.
2. Pods healthy and app pods placed on different nodes (`kubectl get pods -o wide`).
3. Deployments at 1/1 and 2/2.
4. External service address and browser access on port 80.
5. Scale command and 3/3 state on three nodes.

## 7. Reflection

For small internal systems, labs, or teams needing minimal operational overhead, Swarm is the simpler fit. It is easy to learn and deploy, but has a smaller ecosystem and fewer policy/autoscaling extensions. Kubernetes requires more concepts and operational work, yet gives mature scheduling, self-healing, extensibility, access control, observability integrations, and managed-cloud choices. I would use Swarm for a genuinely small and stable environment; for production platforms with multiple teams, variable load, or strong governance needs, I would use Kubernetes, preferably as a managed service.

## 8. Troubleshooting and appendices

Include the real entries from `TROUBLESHOOTING.md`. Append the Dockerfile, Compose files, pipeline, Swarm stack, Kubernetes manifest, tests, and scripts. Do not include live passwords or `.env`.

## Submission gate

- Public/private Git repository contains all source files and a green pipeline.
- Registry contains both required tags and the report names the registry URL.
- Report uses the official template and includes procedures, screenshots, code appendices, real measurements, reflection, and troubleshooting.
- Video demonstrates running solutions, not only static configuration files.
- Infoeduka submission is completed before 31 August 2026 at 23:59:59.
