# ca-server
[![](https://dockeri.co/image/netreconlab/ca-server)](https://hub.docker.com/r/netreconlab/ca-server)
[![Docker](https://github.com/netreconlab/ca-server/actions/workflows/build.yml/badge.svg)](https://github.com/netreconlab/ca-server/actions/workflows/build.yml)
[![Docker](https://github.com/netreconlab/ca-server/actions/workflows/release.yml/badge.svg)](https://github.com/netreconlab/ca-server/actions/workflows/release.yml)

---
Quickly create Certificate Authorities (CAs) for your applications.

## Images
Multiple images are automatically built for your convenience. Images can be found at the following locations:
- [Docker - Hosted on Docker Hub](https://hub.docker.com/r/netreconlab/ca-server)
- [Singularity - Hosted on GitHub Container Registry](https://github.com/netreconlab/hipaa-postgres/pkgs/container/ca-server)

## Local Deployment
### Option 1
Use the docker-compose.yml file to run on a docker container or
1. In terminal, run `docker-compose up`
2. Then Go to `http://localhost:3000/docs` to view api docs and use as needed

### Option 2
Run directly on your local machine by:
1. Installing python 3.10.x and poetry
2. Running `poetry install in the root directory`
3. Run `poetry run uvicorn server.main:app --host 0.0.0.0 --port 3000`
4. Then Go to `http://localhost:3000/docs` to view api docs and use as needed