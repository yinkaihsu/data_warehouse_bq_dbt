# Use the offical golang image to create a binary.
# This is based on Debian and sets the GOPATH to /go.
# https://hub.docker.com/_/golang
FROM golang:1.14-buster as builder

# Create and change to the app directory.
WORKDIR /app

# Retrieve application dependencies.
# This allows the container build to reuse cached dependencies.
# Expecting to copy go.mod and if present go.sum.
# COPY go.* ./
# RUN go mod download

# Copy local code to the container image.
COPY invoke.go ./

# Build the binary.
# RUN go build -mod=readonly -v -o server
RUN go build -v -o server

# Use dbt image
# https://hub.docker.com/r/xemuliam/dbt
FROM xemuliam/dbt:1.0.1-bigquery
USER root
WORKDIR /dbt
COPY crypto_data_warehouse/ ./
# It will be mount using GCP Secret Manager
# COPY secrets/ /secrets

# Copy the binary to the production image from the builder stage.
COPY --from=builder /app/server /app/server
COPY dbt_script.sh ./

# Run the web service on container startup.
CMD ["/app/server"]
