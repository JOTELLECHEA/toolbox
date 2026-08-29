# Docker

## Inspecting
- `docker ps` — running containers
- `docker ps -a` — all containers, including stopped
- `docker images` — local images
- `docker inspect <container>` — full JSON config/state
- `docker logs -f <container>` — tail logs

## Running
- `docker run -it --rm <image> bash` — interactive, auto-remove on exit
- `docker run -d -p 8080:80 <image>` — detached, with port mapping
- `docker run -v $(pwd):/app <image>` — mount current dir into container
- `docker run --gpus all <image>` — expose GPUs (needs nvidia-container-toolkit)
- `docker exec -it <container> bash` — shell into an already-running container

## Building
- `docker build -t <name>:<tag> .` — build an image from the Dockerfile in the current directory
- `docker build --no-cache -t <name> .` — force rebuild every layer

## Cleanup
- `docker stop <container>` — stop a running container
- `docker rm <container>` — remove a stopped container
- `docker rmi <image>` — remove an image
- `docker system prune` — remove stopped containers, dangling images, unused networks
- `docker system prune -a --volumes` — remove everything unused, including volumes (careful — irreversible)

## Compose
- `docker compose up -d` — start services detached
- `docker compose down` — stop and remove
- `docker compose logs -f <service>` — tail logs for one service

## Gotchas
- `docker system prune -a` also removes images you haven't run recently but still want — check `docker images` first.
- `--rm` + forgetting `-it` on an interactive image just runs and exits immediately.
