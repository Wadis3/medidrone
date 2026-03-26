export class Drone {
    static SPEED = 100;

    static dBattery(delta) {
        return 1;
    }

    constructor(id, position, battery) {
        this.id = id;
        this.marker = L.marker(position);
        this.battery = battery;
        //L.marker([50.10574, 36.01122], {icon: drone}).addTo(map);
    }

    deltaLatLng(delta, angle) {


        y_meters = meters * math.sin(angle)
        x_meters = meters * math.cos(angle)

        d_long = y_meters / 111111
        d_lat = x_meters / (111111 * math.cos(d_long + current[0]))

        return (current[0] + d_long, current[1] + d_lat)
    }

    update(delta) {
        this.marker.setLatLng(position);
        battery -= dBattery();
    }
}