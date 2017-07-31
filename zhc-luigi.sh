#!/usr/bin/env bash

# 1) start luigi and mysql using docker-compose
docker-compose up -d

# 2) login the luigi containter and create the zhc_lugi_demo.py script from test code 

# 3) start the luigi task by: 

python zhc_luigi_demo.py

# 4) check the central task history in mysql contaitner:
 mysql -uroot -proot
 use luigid
 select * from task_events;
 
 # 5) make sure delete the input and output folder when resubmit a luigi task 
 rm -rf ./outoput
