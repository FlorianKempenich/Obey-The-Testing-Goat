#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

fab -A deploy:host=floriank@goat-production.ddns.net -f $DIR/fabfile.py
