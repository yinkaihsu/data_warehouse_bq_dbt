# Use dbt base image from Docker Hub.
# https://hub.docker.com/r/xemuliam/dbt
FROM xemuliam/dbt:1.0.1-bigquery
USER root

# Set the current working directory to /code.
WORKDIR /code

# Install the package dependencies in the requirements file.
COPY app/requirements.txt .
RUN pip install --upgrade -r /code/requirements.txt

# Copy the app directory and dbt_script file for web server.
COPY app ./app
COPY dbt_script.sh .

# Copy the dbt directory for dbt tools.
COPY dbt ./dbt
# It will be mount using GCP Secret Manager
# COPY secrets/ /secrets

# Run the web service on container startup.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]