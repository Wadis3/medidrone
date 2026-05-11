#!/bin/bash
echo "startar medidrone-server"


start_flask () {
FILE=$1
PORT=$2

gnome-terminal -- bash -c "
export FLASK_APP=$FILE
export FLASK_DEBUG=1
flask run --port=$PORT --host=0.0.0.0
exec bash
" &
}

start_flask ~/Documents/programmering/medidrone/webserver/database.py 5001
gnome-terminal -- bash -c "python3 ~/Documents/programmering/medidrone/webserver/route_planner.py"
start_flask ~/Documents/programmering/medidrone/webserver/build.py 5000
start_flask ~/Documents/programmering/medidrone/webserver/new_drone.py 5003
start_flask ~/Documents/programmering/medidrone/webserver/new_request.py 5004
