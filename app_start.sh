#!/bin/bash

docker run -it --rm -p 5000:5000 -p 8080:8080 -v $(pwd)/secrets:/secrets -v $(pwd)/app:/app python:3.6 bash