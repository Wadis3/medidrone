from flask import Flask, request
from flask_cors import CORS
import subprocess
import  requests

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

battery = 100.0

#drone_info = {'id': myID,
 #               'longitude': current_longitude,
  #              'latitude': current_latitude,
   #             'status': 'idle'
    #        }

# Fill in the IP address of server, and send the initial location of the drone to the SERVER
#===================================================================
#===================================================================

myIP = '192.168.0.3'

@app.route('/', methods=['POST']) #Körs i new_drone
def main():
    coords = request.json

    with open("data.txt", "w") as f:
        print(str(coords[0]) + "\n" + str(coords[1]))
        f.write(str(coords[0]) + "\n" + str(coords[1]))
        
    return 'OK'

@app.route('/route', methods=['POST'])
def route():
    to_coords = request.json

    f = open("data.txt")
    
    current_longitude = float(f.readline())
    current_latitude = float(f.readline())
    
    f.close()
    print('Nu kör jag')

    subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
                                                 '--tlong', str(to_coords[0]), '--tlat', str(to_coords[1]),
                                                 '--ip', myIP, '--battery', battery
                    ])
    

#    SERVER="http://192.168.0.2:5001/drone"
#    with requests.Session() as session:
#        resp = session.post(SERVER, json=drone_info)

    return 'New route received'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
