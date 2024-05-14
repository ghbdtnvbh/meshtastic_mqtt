from paho.mqtt import client as mqtt
from database import add_telemetry, add_node, add_position, node_exists
import json

Node_ID = "!65ca5152"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(f"msh/RU/2/json/LongFast/{Node_ID}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        if f"!{hex(data['from'])[2:]}" != Node_ID:
            print(data)
            if 'telemetry' in data['type']:
                user_id = f"!{hex(data['from'])[2:]}"
                air_util_tx = round(data['payload']['air_util_tx'],2)
                battery_level = round(data['payload']['battery_level'],2)
                channel_utilization = round(data['payload']['channel_utilization'],2)
                voltage = round(data['payload']['voltage'],2)
                rssi = data['rssi']
                snr = data['snr']
                add_telemetry(user_id, battery_level, voltage, air_util_tx, channel_utilization, snr, rssi)

            if 'nodeinfo' in data['type']:
                node_id = data['payload']['id']
                shortname = data['payload']['shortname']
                longname = data['payload']['longname']
                hardware = data['payload']['hardware']
                if not node_exists(node_id):
                    add_node(node_id, longname, shortname, hardware)
                else:
                    print('Нода уже добавлена')
            if 'position' in data['type'] and data['payload']['latitude_i'] != 0:
                user_id = f"!{hex(data['from'])[2:]}"
                altitude = data['payload']['altitude']
                latitude = f"{data['payload']['latitude_i']/10000000:.6f}"
                longitude = f"{data['payload']['longitude_i']/10000000:.6f}"
                lat_lon = f"{latitude},{longitude}"
                rssi = data['rssi']
                snr = data['snr']
                add_position(user_id, altitude, lat_lon, rssi, snr)
    except:
        print("Data NOT/Bad JSON")


if __name__ == '__main__':
    client = mqtt.Client()
    client.username_pw_set("user1", "1234")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()
