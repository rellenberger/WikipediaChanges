# WikipediaChanges

## Overview
This project sets up a Docker-based Kafka environment to stream recent changes from the Wikipedia recent changes SSE endpoint, using Kafka, Kafka Connect, Schema Registry, and Minio for storage.

## Usage
Services within the docker-compose.yaml file use variables to configure credentials. 
For example, the Minio service uses the following variables to configure the root user and password:
    MINIO_ROOT_USER: ${MINIO_ROOT_USER-minioadmin}
    MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD-minio123}
See https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#ways-to-set-variables-with-interpolation for this inerpolation syntax. Effectively, if a .env file is located next to the docker-compose.yaml file, and the .env file contains the variables:
    MINIO_ROOT_USER=minioRootUser
    MINIO_ROOT_PASSWORD=minioRootPassword
then these values will be used, otherwise the default values will be used (the default values are after the dash - ie minioadmin and minio123).

Navigate to the project directory and run the following Docker command bring the services up:
```
docker compose up -d
```
(launches the services, with terminal output supressed)

This will launch a docker environment with the following services running:
- Kafka Broker
- Schema Registry
- Kafka Connect
- Minio

We will only be running Kafka Connect in standalone (ie. non distributed) mode for this proejct.
To do this, again in terminal, execute
```
docker exec -it -w /bin kafka-connect bash
```
This will open a bash shell in the Kafka Connect container. 

Once the environment is running, navigate to `localhost:3030` to view the Kafka Connect interface. From here, you can monitor the status of the connectors and topics.

## Issues:
- The JSON schema supplied to the Wikimedia Kafka Connect SSE is hard coded, so schema updates won't flow automatically. Wikimedia supply schema files here https://schema.wikimedia.org/#!/primary/jsonschema but they are .yaml and so need to be converted to JSON first.
