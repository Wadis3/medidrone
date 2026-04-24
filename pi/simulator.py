import math
import requests
import argparse

def moveDrone(src, d_long, d_la):
    x, y = src
    x = x + d_long
    y = y + d_la        
    return (x, y)

def deltaLatLng(meters, angle, current):
    y_meters = meters * math.sin(angle)
    x_meters = meters * math.cos(angle)

    d_long = y_meters / 111111
    d_lat = x_meters / (111111 * math.cos(d_long + current[0]))

    return d_long, d_lat

def run(ip, current_coords, to_coords, SERVER_URL):
    drone_coords = current_coords
    while (drone_coords[0] - to_coords[0])**2 + (drone_coords[1] - to_coords[1])**2 > 0.02:
        angle = math.arctan((drone_coords[0] - to_coords[0]) / (drone_coords[1] - to_coords[1]))
        meters = 1000
        d_long, d_lat = deltaLatLng(angle, meters, drone_coords)
        drone_coords = moveDrone(drone_coords, d_long, d_lat)
        with requests.Session() as session:
            drone_info = {'ip': ip,
                          'longitude': drone_coords[0],
                          'latitude': drone_coords[1],
                          'status': 'busy'
                        }
            resp = session.post(SERVER_URL, json=drone_info)
    drone_coords = to_coords
    with requests.Session() as session:
        drone_info = {'ip': ip,
                        'longitude': drone_coords[0],
                        'latitude': drone_coords[1],
                        'status': 'idle'
                    }
        resp = session.post(SERVER_URL, json=drone_info)

    return drone_coords[0], drone_coords[1]
   
if __name__ == "__main__":
    SERVER_URL = "http://192.168.0.2:5001/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    parser.add_argument("--ip", help ='drones ID' ,type=str)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    to_coords = (args.tlong, args.tlat)

    print(current_coords, to_coords)
    drone_long, drone_lat = run(args.ip, current_coords, to_coords, SERVER_URL)
    with open("coordinates.txt", "w") as f:
        print(str(to_coords[0]) + "\n" + str(to_coords[1]))
        f.write(str(to_coords[0]) + "\n" + str(to_coords[1]))
    