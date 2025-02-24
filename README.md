# WikipediaChanges

## Overview
This project sets up a Docker-based Kafka environment to stream recent changes from the Wikipedia recent changes SSE endpoint, using Kafka, Kafka Connect, Schema Registry, and Minio for storage.

## Usage
Navigate to the project directory and run the following Docker command bring the services up (the -d flag suppresses terminal output):
```
docker compose up -d
(launches the docker services, with terminal output supressed)

This will launch a docker environment with the following services running:
- Kafka Broker
- Schema Registry
- Kafka Connect
- Minio

Again in terminal, run the following command
docker exec -it -w /bin kafka-connect bash
This will open a bash shell in the Kafka Connect container. From here, run the following command to create the connector:
```
Once the environment is running, navigate to `localhost:3030` to view the Kafka Connect interface. From here, you can monitor the status of the connectors and topics.
