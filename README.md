# BrightHive Data Resource API

[![CircleCI](https://circleci.com/gh/brighthive/data-resource-api.svg?style=svg)](https://circleci.com/gh/brighthive/data-resource-api)

[![Coverage Status](https://coveralls.io/repos/github/brighthive/programs-api/badge.svg?branch=master)](https://coveralls.io/github/brighthive/programs-api?branch=master)

A simple API for storing and retrieving data resources.

## Scripts

### create_sample_data.py

Creates a collection of sample datasets in JSON format from the programs, participants, and providers sample datasheets found [here](https://github.com/workforce-data-initiative/tpot-data-definitions/tree/master/datasheets).

#### Usage

```
$ ./scripts/create_sample_data.py /path/to/csv/files
```

### launch_postgres.sh

Stands up a PostgreSQL Docker Container suitable for use in development.

#### Usage

```
$ ./scripts/launch_postgres.sh
```