import math
import requests
import argparse

def moveDrone(src, d_long, d_la):
    x, y = src
    x = x + d_long
    y = y + d_la
    
    return (x, y)

def delta(meters, angle, current, battery):
    battery = battery - meters * 0.001
    y_meters = meters * math.sin(angle)
    x_meters = meters * math.cos(angle)

    d_long = (y_meters / 111111) * -1
    d_lat = x_meters / (111111 * math.cos(d_long + current[0])) * -1

    return d_long, d_lat, battery

def update_coords(ip, SERVER_URL, coords, battery):
    with open("data.txt", "w") as f:
        print(str(coords[0]) + "\n" + str(coords[1]) + '\n' + str(battery))
        f.write(str(coords[0]) + "\n" + str(coords[1]) + '\n' + str(battery))

    with requests.Session() as session:
        drone_info = {'ip': ip,
                        'longitude': coords[0],
                        'latitude': coords[1],
                        'status': 'busy',
                        'battery': battery
                    }
        resp = session.post(SERVER_URL, json=drone_info)

def run(ip, current_coords, to_coords, battery, SERVER_URL):
    drone_coords = current_coords
    while math.sqrt((drone_coords[0] - to_coords[0])**2 + (drone_coords[1] - to_coords[1])**2) > 0.001:
        angle = math.atan((drone_coords[0] - to_coords[0]) / (drone_coords[1] - to_coords[1]))
        meters = 10
        d_long, d_lat, battery = delta(meters, angle, drone_coords, battery)
        drone_coords = moveDrone(drone_coords, d_long, d_lat)
        update_coords(ip, SERVER_URL, drone_coords, battery)
#        with requests.Session() as session:
#            drone_info = {'ip': ip,
#                          'longitude': drone_coords[0],
#                          'latitude': drone_coords[1],
#                          'status': 'busy',
#                          'battery': battery
#                        }
#            resp = session.post(SERVER_URL, json=drone_info)
    drone_coords = to_coords
    update_coords(ip, SERVER_URL, drone_coords, battery)
#    with requests.Session() as session:
#        drone_info = {'ip': ip,
#                        'longitude': drone_coords[0],
#                        'latitude': drone_coords[1],
#                        'status': 'idle',
#                        'battery': battery
#                    }
#        resp = session.post(SERVER_URL, json=drone_info)

    return drone_coords[0], drone_coords[1], battery
   
if __name__ == "__main__":
    SERVER_URL = "http://192.168.0.2:5001/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    parser.add_argument("--ip", help ='drones ID' ,type=str)
    parser.add_argument("--battery", help='drone battery', type=float)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    to_coords = (args.tlong, args.tlat)

    print(current_coords, to_coords)
    drone_long, drone_lat, final_battery = run(args.ip, current_coords, to_coords, args.battery, SERVER_URL)
    with open("data.txt", "w") as f:
        print(str(to_coords[0]) + "\n" + str(to_coords[1]) + "\n" + str(final_battery))
        f.write(str(to_coords[0]) + "\n" + str(to_coords[1]) + "\n" + str(final_battery)) #har ej battery
    