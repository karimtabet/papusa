#!/bin/bash

echo $(awk -F. '/[0-9]+\./{$NF++;print}' OFS=. <<< cat VERSION) > VERSION
docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD";
docker push karimtabet/papusa:latest;
docker push karimtabet/papusa:$version;
