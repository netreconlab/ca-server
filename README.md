# ca-server
[![](https://dockeri.co/image/netreconlab/ca-server)](https://hub.docker.com/r/netreconlab/ca-server)
[![Docker](https://github.com/netreconlab/ca-server/actions/workflows/build.yml/badge.svg)](https://github.com/netreconlab/ca-server/actions/workflows/build.yml)
[![Docker](https://github.com/netreconlab/ca-server/actions/workflows/release.yml/badge.svg)](https://github.com/netreconlab/ca-server/actions/workflows/release.yml)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

---
Quickly create Certificate Authorities (CAs) for your applications.

## Software Designed for `ca-server`
- [ParseCertificateAuthority](https://github.com/netreconlab/ParseCertificateAuthority) - Send CSR's and retreive certificates to/from `ca-server` from [Parse-Swift](https://github.com/netreconlab/Parse-Swift) based clients and servers
- [CertificateSigningRequest](https://github.com/cbaker6/CertificateSigningRequest) - Generate CSR's on Swift clients and servers that can later be signed by `ca-server`
- [Parse-Swift](https://github.com/netreconlab/Parse-Swift) - Write Parse client apps in Swift. When coupled with - [ParseCertificateAuthority](https://github.com/netreconlab/ParseCertificateAuthority) and - [CertificateSigningRequest](https://github.com/cbaker6/CertificateSigningRequest), provides the complete client-side stack for generating CSR's, sending/receiving certificates to/from `ca-server`
- [ParseServerSwift](https://github.com/netreconlab/parse-server-swift) - Write Parse Server Cloud Code apps in Swift. When coupled with - [ParseCertificateAuthority](https://github.com/netreconlab/ParseCertificateAuthority), [CertificateSigningRequest](https://github.com/cbaker6/CertificateSigningRequest), and [Parse-Swift](https://github.com/netreconlab/Parse-Swift) provides the complete server-side stack for generating CSR's, sending/receiving certificates to/from `ca-server`


## Images
Multiple images are automatically built for your convenience. Images can be found at the following locations:
- [Docker - Hosted on Docker Hub](https://hub.docker.com/r/netreconlab/ca-server)
- [Singularity - Hosted on GitHub Container Registry](https://github.com/netreconlab/hipaa-postgres/pkgs/container/ca-server)

## Environment Variables
Below is a list of environment variables available to configure `ca-server`. It is required to mount the folder containing `CA_SERVER_PRIVATE_KEY_FILE` and `CA_SERVER_ROOT_CA_CERT`. It is recommended to mount the folder containing `CA_SERVER_DATABASE_NAME` to persist your database during restarts. See https://rajanmaharjan.medium.com/secure-your-mongodb-connections-ssl-tls-92e2addb3c89 to learn how to create a private key and root certificate. It is also recommended to mount the folder containing `CA_SERVER_CA_DIRECTORY` to persist any files created by `ca-server`.

```bash
CA_SERVER_PRIVATE_KEY_FILE=./server/ca/private/cakey.pem # (Required) Location and name of private key 
CA_SERVER_ROOT_CA_CERT=./server/ca/private/cacert.der # (Required) Location and name of CA certificate
CA_SERVER_DATABASE_NAME=./server/dbs/appdb.sqlite # (Required) Location and name of the database
CA_SERVER_CA_DIRECTORY=./server/ca # Location to store CA related files
CA_SERVER_ROUTE_ROOT_CERTIFICATE_PREFIX=/ca_certificate # The prefix to add root certificate related routes
CA_SERVER_ROUTE_USER_PREFIX=/appusers # The prefix to add to all user related routes
CA_SERVER_ROUTE_CERTIFICATE_PREFIX=/certificates # The prefix to add to all certificate related routes
CA_SERVER_ROUNDS=5 # Number of rounds
```

## Local Deployment
### Option 1
Use the docker-compose.yml file to run on a docker container or
1. Fork this repo
2. In terminal, run `docker-compose up`
3. Then Go to `http://localhost:3000/docs` to view api docs and use as needed

### Option 2
Run directly on your local machine by:
1. Fork this repo
2. Install python 3.10.x and poetry
3. Running `poetry install in the root directory`
4. Run `poetry run uvicorn server.main:app --host 0.0.0.0 --port 3000`
5. Then Go to `http://localhost:3000/docs` to view api docs and use as needed

## Running behind a proxy
If you need to run `ca-server` behind a proxy, `--root-path` needs to be added to command to start `ca-server` in the `docker-compose.yml` file. The root path should match the exact endpoint proxying to `ca-server`. For example, if your endpoint is `/ca`, then the proper command is below:

```bash
# `docker-compose.yml` 
command: [ "./start-poetry.sh", "poetry", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "3000", "--root-path", "/ca" ]
```

In addition, two endpoints to the nginx configuration file:
```bash
# Allow access to the docs of your ca-server
location /ca/docs {
    proxy_pass http://ca-server:3000/docs;
}

# Allow access to the rest of your ca-server api
location /ca/ {
    proxy_pass http://ca-server:3000/;
}
```
