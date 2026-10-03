# DevOps Engineer Homework

This repository contains a small FastAPI service, its Docker image, a Helm chart, Terraform configuration for deploying the chart, and a GitLab CI pipeline.

## What You Changed

- Implemented the requested JSON API in `app/main.py`. Configurations can be created, read, and deleted; an unknown configuration returns HTTP 404, and deleting an absent key returns `{"deleted": false}`.
- Added automated endpoint tests, pinned runtime and test dependencies, and a minimal Python container that runs as a non-root user.
- Completed the Helm chart with consistent selectors, configurable image/environment/replicas, health probes, resource requests and limits, restrictive container security settings, a ClusterIP Service, and an optional Ingress.
- Repaired Terraform provider requirements, made the kubeconfig and deployment values configurable, and corrected the chart path and release configuration.
- Replaced placeholder CI commands with Python tests, Helm and Terraform validation, a rootless BuildKit container build/push to the GitLab registry, and a default-branch deployment job.

## Assumptions

- The API listens on port `8000`; Kubernetes exposes it through a Service on port `80`.
- `ENVIRONMENT` is an optional environment variable and is returned as an empty string when unset.
- The demo configuration store is in-memory and local to one application process.
- The GitLab runner can run the rootless BuildKit executor image. The project GitLab Container Registry is used for images.
- The deploy job targets a Kubernetes cluster reachable using a GitLab file-type CI/CD variable named `KUBE_CONFIG`. The release namespace defaults to `production`.
- Terraform uses the kubeconfig at `~/.kube/config` by default and deploys to the local/current Kubernetes context.

## Known Limitations

- Configuration values are not persisted, shared across replicas, or protected by authentication; they are suitable only for this demonstration and must not be used for secrets.
- The default Helm ingress is disabled. Enable and configure it for a cluster that has an Ingress controller.
- Terraform and deployment jobs require access to the target cluster and registry. No cloud resources or local Kubernetes cluster are provisioned.
- Rootless BuildKit requires the runner to allow the system calls and user namespaces it uses for builds. Some self-managed runners need security-profile adjustments.
- The CI deployment is intentionally limited to the default branch. Registry authentication uses GitLab's predefined CI registry credentials.

## Production Improvements

- Store configuration in a durable, access-controlled backend and use a dedicated secret-management system for sensitive values.
- Add authentication/authorization, request rate limits, structured logs, metrics, tracing, and API-level resource limits.
- Build and scan a minimal image, pin base images by digest, generate an SBOM, and sign artifacts.
- Use dedicated least-privilege cluster identities, environment protections/approvals, and a staged promotion/rollback strategy.
- Add integration tests against a Kubernetes test environment, chart schema validation, Terraform plan review, and policy/security scans.
- Configure autoscaling, disruption budgets, network policies, external TLS, and cluster-specific resource sizing.

## Run Locally

Requirements: Python 3.14+ and Docker Desktop (or another Docker Engine).

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r app\requirements-dev.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The interactive API documentation is at `http://localhost:8000/docs`.

```powershell
docker build -t myapp:1.0.0 .
docker run --rm -p 8000:8000 -e ENVIRONMENT=local myapp:1.0.0
```

Then open `http://localhost:8000/health`. Stop the container with `Ctrl+C`. To run it in the background, add `-d` to `docker run`; view its output with `docker logs <container-id>` and stop it with `docker stop <container-id>`.

## API

| Method | Path | Behavior |
| --- | --- | --- |
| `GET` | `/health` | Returns `{"status":"ok"}` |
| `GET` | `/version` | Returns `{"version":"1.0.0"}` |
| `GET` | `/env` | Returns the `ENVIRONMENT` value |
| `POST` | `/config` | Stores and returns a JSON `{"name":"...","value":"..."}` item |
| `GET` | `/config/{name}` | Returns a stored item, or HTTP 404 |
| `DELETE` | `/config/{name}` | Returns whether an item was removed |

Run tests with:

```powershell
pip install -r app\requirements-dev.txt
python -m pytest -q app\test_main.py
```

## Kubernetes and Terraform

Build the image and make it available to the selected cluster first. Then install the chart directly:

```powershell
helm upgrade --install myapp helm `
  --namespace dev --create-namespace `
  --set image.repository=myapp --set image.tag=1.0.0 `
  --set environment=dev
```

For kind, load the locally built image into the cluster with `kind load docker-image myapp:1.0.0` before installing the chart. The default chart uses one replica and does not create an Ingress.

Terraform requires a working kubeconfig/current context. It creates the namespace and Helm release:

```powershell
terraform -chdir=terraform init
terraform -chdir=terraform plan
terraform -chdir=terraform apply
```

Override `namespace`, `environment`, `image_repository`, `image_tag`, `replica_count`, or `kubeconfig_path` with Terraform variables as needed.

## GitLab CI

The pipeline tests the API, lints the chart, validates Terraform, builds and pushes a commit-tagged image with rootless BuildKit (without Docker-in-Docker), and deploys that image from the default branch. Configure `KUBE_CONFIG` as a protected GitLab **file-type** CI/CD variable containing a kubeconfig with permission to manage the release namespace. The GitLab runner must support the BuildKit rootless image and required user namespaces; the cluster must be reachable from the deploy runner. The namespace can be overridden with the `KUBE_NAMESPACE` CI/CD variable.
