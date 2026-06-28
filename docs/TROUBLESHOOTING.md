# Troubleshooting log

Replace/add entries with issues you actually encounter. Include a screenshot or log excerpt for each material problem.

| Date | Symptom | Evidence/diagnosis | Fix | Verification |
|---|---|---|---|---|
| TODO | App cannot connect to MySQL | Check app logs, credentials, service DNS, and MySQL readiness | Correct the identified value or wait for healthy DB | `/healthz` returns 200 and a conversion persists |
| TODO | Second app replica remains pending | Check node count and anti-affinity/scheduling messages | Add an eligible node or correct labels/taints | Replicas run on different nodes |
| TODO | LoadBalancer has no external address | Check whether the cluster provides a load-balancer implementation | Configure the provider load balancer; use port-forward only for local diagnosis | Service receives an external address and port 80 responds |
| TODO | Registry image pull fails | Check image path, visibility, tag, and pull credentials | Correct the path or create an image-pull secret | Deployment rollout completes |
