# Docker & Kubernetes Assessment Report

> [!TIP]
> Use this document to explain your design choices, optimisations and any challenges you faced.

## Dockerfile

<!-- TODO: (Optional) Explain any specific goals or design decisions -->

### Forked repository

<!-- TODO: If you submitted your changes to a fork, replace with your forked repository -->
`https://github.com/your-username/academic-calendar-api`

## Kubernetes

I wrote a short manifest, and tried to run it using minikubes on windows, but got stuck on pulling images, so moved to
kubernetes on docker desktop which had issues finding files being mounted, and so moved to minkubes on wsl, which had
issues finding the files, which I found out you need to mount the files, however mounting after starting caused an error
with connection refused, so I had to add command line arguments to mount it. Then I also found out I had to port forward
it, so I did that.

The commands to run it on my machine are:
minikube start --mount --mount-string="/mnt/c/Users/Angelo/Desktop/2026-recruitment-technical-assessment/platforms/docker-kubernetes/navidrome:/navidrome" --driver=docker

kubectl get pods (to get the pod name)

kubectl port-forward {pod name} 4533:4533 -n default

there is probably a better way to do this but it's 1:30am and I have been working on this for the past solid 5 hours
