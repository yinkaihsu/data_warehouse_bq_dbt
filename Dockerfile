FROM xemuliam/dbt:1.0.1-bigquery

# It will be mount using GCP Secret Manager
# COPY secrets/ /secrets

WORKDIR /dbt
COPY crypto_data_warehouse/ .
