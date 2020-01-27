#!/bin/sh

image=$1

docker run -v $(pwd)/test_dir:/opt/ml -p 8080:8080 --rm --memory 8G --cpus=4  ${image} serve 