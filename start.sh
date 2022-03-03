#!/bin/bash

docker run -it --rm -p 5000:5000 -p 8080:8080 -v $(pwd)/secrets:/secrets data_warehouse_bq_dbt:latest