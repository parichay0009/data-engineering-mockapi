# data-engineering-mockapi

## Project overview
``` bash
├── crontab (script to run process everyday)
├── docker-compose.yml (setup container for postgres and application)
├── Dockerfile
├── entry_point.sh (script to build and up containers)
├── project
│   ├── config.py (configuration values)
│   ├── etl.py (extract transform and load data)
│   ├── models.py (database classes)
│   ├── sql_test.sql (sql queries for results)
│    
├── README.md
├── requirements.txt
    
```

## How to rebuild

1. To build and run docker container:
    ```
    ./entry_point.sh 
    ```
1. To check all the results of all queries (provide password as db_password):
    ```
    psql -U db_user -h 127.0.0.1 -p 5433 -d spark_net -a -f project/sql_test.sql 

    ```