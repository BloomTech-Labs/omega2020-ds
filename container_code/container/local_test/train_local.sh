#!/bin/sh

image=$1

mkdir -p test_dir/model
mkdir -p test_dir/output

rm test_dir/model/*
rm test_dir/output/*

sudo docker run -v $(pwd)/test_dir:/opt/ml --rm  --memory 8G --cpus="4" ${image} train 
