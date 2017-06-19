#!/usr/bin/env bash

nohup python3 nest_to_sql.py &> /dev/null &
nohup python3 web.py &> /dev/null &
