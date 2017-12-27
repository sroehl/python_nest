#!/usr/bin/env bash

nohup python3 nest_to_sql.py &> log_n_t_s.log &
nohup python3 web.py &> log_web.log &
