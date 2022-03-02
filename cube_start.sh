#!/bin/bash

docker run -it --rm -p 3000:3000 -p 4000:4000 -v $(pwd)/secrets:/secrets -v $(pwd)/cube:/cube/conf cubejs/cube:v0.29