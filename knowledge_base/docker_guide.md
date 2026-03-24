# Docker Guide

## What is Docker?
Docker is an open-source platform that automates the deployment, scaling, and management of applications using containerization. Containers package an application with all its dependencies, libraries, and configuration files, ensuring it runs consistently across different environments — from a developer's laptop to production servers.

## Docker vs Virtual Machines
Containers share the host OS kernel, making them lightweight and fast to start (seconds vs minutes for VMs). Virtual machines include a full guest operating system and hypervisor layer, consuming more resources. Containers are ideal for microservices and CI/CD pipelines, while VMs are better for running different operating systems or complete isolation.

## Key Docker Concepts
- **Image**: A read-only template containing the application code, runtime, libraries, and dependencies. Built from a Dockerfile.
- **Container**: A running instance of an image. Containers are isolated but share the host kernel.
- **Dockerfile**: A text file with instructions to build a Docker image (e.g., `FROM`, `RUN`, `COPY`, `CMD`).
- **Docker Compose**: A tool for defining and running multi-container applications using a `docker-compose.yml` file.
- **Registry**: A storage for Docker images. Docker Hub is the default public registry.

## Common Docker Commands
- `docker build -t myapp .` — Build an image from a Dockerfile.
- `docker run -p 8080:80 myapp` — Run a container, mapping port 8080 to container port 80.
- `docker ps` — List running containers.
- `docker stop <container_id>` — Stop a running container.
- `docker-compose up` — Start all services defined in `docker-compose.yml`.
- `docker images` — List all local images.
- `docker pull <image>` — Download an image from a registry.

## Docker Best Practices
Use small base images (e.g., `python:3.11-slim` instead of `python:3.11`). Leverage multi-stage builds to reduce final image size. Never store secrets in images — use environment variables or Docker secrets. Use `.dockerignore` to exclude unnecessary files from the build context.
