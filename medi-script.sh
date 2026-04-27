#!/bin/bash
echo "startar medidrone-server"


start_flask () {
FILE=$1
PORT=$2

gnome-terminal -- bash -c "
export FLASK_APP=$FILE
export FLASK_DEBUG=1
flask run --port=$PORT
exec bash
" &
}

start_flask ~/medidrone/webserver/database.py 5001
start_flask ~/medidrone/webserver/route_planner.py 5002
start_flask ~/medidrone/webserver/build.py 5000
start_flask ~/medidrone/webserver/new_drone.py 5003

