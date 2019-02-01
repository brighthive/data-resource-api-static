#!/bin/bash

docker run --name postgres \
            -e POSTGRES_USER=test_user \
            -e POSTGRES_PASSWORD=test_password \
            -e POSTGRES_DB=tpot_programs \
            -p 5432:5432 \
            -d postgres