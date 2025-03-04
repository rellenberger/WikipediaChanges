# WikipediaChanges

## Overview
This project sets up a Docker-based Kafka environment to stream events from the Wikipedia recent changes SSE endpoint, using Kafka, Kafka Connect, Schema Registry, and Minio for storage.

## Configuration
Services within the docker-compose.yaml file use variables to configure credentials. 
For example, the Minio service uses the following variables to configure the root user and password:
```
    MINIO_ROOT_USER: ${MINIO_ROOT_USER-minioadmin}
    MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD-minio123}
```
See https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#ways-to-set-variables-with-interpolation for this inerpolation syntax. 
Effectively, if a .env file is located next to the docker-compose.yaml file, and the .env file contains the variables:
```
    MINIO_ROOT_USER=minioRootUser
    MINIO_ROOT_PASSWORD=minioRootPassword
```
then these values will be used, otherwise the default values will be used (the default values are after the dash - ie minioadmin and minio123).

We will be using Kafka Connect in standalone (non-distributed) mode, so we provide
- Worker configurations details in the connect-avro-standalone.properties file
- Wikimedia SEE connector configurations in the wikimedia-changes.properties file
- Minio sink configurations in the minio-sink.properties file

The Wikimedia SSE connector sends each event with an ID section and a Data section. As we are only interested in the Data, we utilitise the transform org.apache.kafka.connect.transforms.ExtractField$Value to extract the Data section from the event. We then use the com.github.jcustenborder.kafka.connect.json.FromJson$Value transform to convert the JSON string to a Kafka Connect Struct. This is configured in the wikimedia-changes.properties file as follows:
```
transforms = extractData, fromJson
transforms.extractData.type = org.apache.kafka.connect.transforms.ExtractField$Value
transforms.extractData.field = data
transforms.fromJson.type = com.github.jcustenborder.kafka.connect.json.FromJson$Value
transforms.fromJson.json.exclude.locations = #/properties/server_script_path,#/properties/log_params,#/properties/log_action,#/properties/log_action_comment,#/properties/log_id,#/properties/log_type,#/properties/\$schema,#/\$schema
transforms.fromJson.json.schema.url = https://raw.githubusercontent.com/rellenberger/WikipediaChanges/refs/heads/main/mediawiki-recentchange-1.0.1.json
transforms.fromJson.schema.validation.enabled = false
```
The JSON schema is supplied in the transforms.fromJson.json.schema.url field.

Volumes are used to mount the configurations and data files into the Kafka Connect container, but no data persists once the docker services are stopped.

## Usage
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

From here, we can start the Kafka Connect service with the following command:
```
/bin/connect-standalone /data/connect-properties/connect-avro-standalone.properties /data/connect-properties/minio-sink-parquet.properties /data/connect-properties/wikimedia-changes.properties
```
This command starts the Kafka Connect service in standalone mode, using the configurations in the connect-avro-standalone.properties, minio-sink-parquet.properties, and wikimedia-changes.properties files.

You should see the Kafka Connect service start up and begin streaming events from the Wikipedia recent changes SSE endpoint into the S3/Minio bucket.

To verify that the events are being streamed correctly, you can check the Minio bucket by accessing the Minio web interface at `http://localhost:9000` and logging in with the credentials specified in your `.env` file or the default credentials.

To terminate the process, press Ctrl+C in the terminal where the Kafka Connect service is running.

## Reading the data
The data is stored in the Minio bucket in Parquet format. To read the data, we can use DuckDb to query the data naively from the S3 Parquet files. The wiki-jupyter notebook contains an example of how to read the data from the Minio bucket and query it using DuckDb.

## Issues
- The JSON schema supplied to the Wikimedia Kafka Connect SSE is hard coded, so schema updates won't flow automatically. Wikimedia supply schema files here https://schema.wikimedia.org/#!/primary/jsonschema but they are .yaml and so need to be converted to JSON first.
- Using seaborn and matplotlib to read dataframes means duckDb needs to be converted to pandas first. This is not ideal for large datasets as it leads to the entire dataset being loaded into memory.
