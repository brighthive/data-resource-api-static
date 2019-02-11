# ----------------------------------------------------------------------------
# test_environment.sh
#  
#
#
# ----------------------------------------------------------------------------
#!/bin/bash

usage() {
    echo "Hello"
}

start_test_environment() {
    echo "Starting Test Environment"
}

stop_test_environment() {
    echo "Stopping Test Environment"
}


ARGS=$1

case "$ARGS" in
    start)
        start_test_environment
        ;;
    stop)
        stop_test_environment
        ;;
    *)
        usage
        exit 1
esac