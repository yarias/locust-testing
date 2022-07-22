from locust import TaskSet, HttpUser, task, between

"""
Will use influxDB to store the perfomance results and Grafana to render the results. Those apps will be running 
in a docker-compose


Steps:
    1. Intall Docker and Docker-compose in the host
    2. Download from Docker Hub influxdb and grafana images
    3. Create a custom network to monitor influxdb-grafana communication
        docker network create monitor_network
    4. We need to bind ports -p
        InfluxDB: default port 8086
        Grafana: default port 3000
    5. For persistent data, we can create a volume for each app
        docker volume create influxdb-volume
        docker volume create grafana-volume
    6. Create the docker compose file
        ./docker/docker-compose.yml
    7. Run docker-compose
        docker-compose up -d
        
Test Influxdb:
    1. Open in a browser: http://localhost:8086
        Configure User Name and Password
    2. Connect to the container
        docker exec -it influxdb_container sh
    3. Create a token using the UI or CLI
    4. Create config 
        influx config create --config-name <xx> --host-url <xx> --org <xx> --token <xx> --active
    5. Create a DB
        create database sampledb
        
"""