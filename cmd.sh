#!/bin/bash

gunicorn --bind=0.0.0.0 data_resource_api:app