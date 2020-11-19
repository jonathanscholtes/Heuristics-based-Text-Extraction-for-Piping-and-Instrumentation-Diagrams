#!/bin/sh

cd ../../

docker build --pull --rm -f "testing/param_testing/Dockerfile" -t jscholtes/pid_param_tune:latest .

docker push jscholtes/pid_param_tune:latest
read -rsn1