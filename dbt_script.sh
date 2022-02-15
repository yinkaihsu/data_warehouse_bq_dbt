#!/bin/bash

# dbt debug --profiles-dir .
dbt deps --profiles-dir .  # Pulls the most recent version of the dependencies listed in your packages.yml from git
dbt seed --profiles-dir .
# dbt test --models source:* --profiles-dir .
dbt run --profiles-dir .
# dbt test --exclude source:* --profiles-dir .
# dbt docs generate --profiles-dir .
# dbt docs serve --profiles-dir .