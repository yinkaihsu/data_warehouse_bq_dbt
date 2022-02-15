#!/bin/bash

docker run -it --rm -p 8080:8080 -v $(pwd)/secrets:/secrets -v $(pwd)/crypto_data_warehouse:/dbt xemuliam/dbt:1.0.1-bigquery bash
