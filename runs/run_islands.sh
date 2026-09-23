#!/bin/bash
cd /Users/jstav/code/program-ecologies
python3 src/islands.py --game pd --seedings programs prior hostile clustered > runs/log_islands_pd.txt 2>&1
python3 src/islands.py --game chicken --seedings programs hostile clustered > runs/log_islands_chicken.txt 2>&1
python3 src/islands.py --game chicken_norole --norole --seedings programs hostile clustered > runs/log_islands_chicken_norole.txt 2>&1
echo ALLDONE >> runs/log_islands_pd.txt
