import machine
import time
import ssd1306
import network
from umqtt.simple import MQTTClient

MQTT_CLIENT_ID = ""
MQTT_BROKER = "broker.mqtt.cool"
MQTT_USER = "deeja"
MQTT_PASSWORD = "deeja123"
MQTT_TOPIC_ID = "project"
MQTT_TOPIC_LOG = "log"

i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

row_pins = [machine.Pin(12, machine.Pin.OUT),
            machine.Pin(14, machine.Pin.OUT),
            machine.Pin(27, machine.Pin.OUT),
            machine.Pin(26, machine.Pin.OUT)]

col_pins = [machine.Pin(32, machine.Pin.IN, machine.Pin.PULL_DOWN),
            machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_DOWN),
            machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_DOWN),
            machine.Pin(34, machine.Pin.IN, machine.Pin.PULL_DOWN)]

key_map = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

print("Connecting to WiFi...", end="")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Wokwi-GUEST", "")
while not wifi.isconnected():
    time.sleep(0.5)
    print(".", end="")
print(" Connected!")

print("Connecting to MQTT...")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)

def publish_log(msg):
    client.publish(MQTT_TOPIC_LOG, msg)

def display_text(text):
    oled.fill(0)
    oled.text(text, 0, 20)
    oled.show()

def mqtt_message(topic, msg):
    try:
        decoded = msg.decode()
        print("Received from panel:", decoded)
        if decoded.isdigit() and len(decoded) == 10:
            display_text("Panel ID: " + decoded)
            publish_log("ID from panel: " + decoded)
        else:
            display_text("Invalid Panel ID")
            publish_log("Invalid ID from panel")
    except Exception as e:
        print("Error handling panel msg:", e)
        publish_log("Error handling panel input")

client.set_callback(mqtt_message)
client.connect()
client.subscribe(MQTT_TOPIC_ID)
print("MQTT connected and subscribed to", MQTT_TOPIC_ID)

def scan_keypad():
    for row_num, row_pin in enumerate(row_pins):
        row_pin.value(1)
        for col_num, col_pin in enumerate(col_pins):
            if col_pin.value() == 1:
                time.sleep(0.1)
                if col_pin.value() == 1:
                    while col_pin.value() == 1:
                        pass
                    row_pin.value(0)
                    return key_map[row_num][col_num]
        row_pin.value(0)
    return None

def read_code():
    code = ""
    display_text("Enter 10-digit ID:")
    while True:
        client.check_msg()
        key = scan_keypad()
        if key:
            if key == '#':
                if len(code) == 10:
                    return code
                else:
                    display_text("Enable")
                    publish_log("Enable: Not enough digits")
                    time.sleep(1)
                    display_text(code)
            elif key == 'B':
                code = ""
                display_text("Cleared")
                publish_log("Input Cleared")
                time.sleep(1)
                display_text(code)
            elif key in '0123456789':
                if len(code) < 10:
                    code += key
                    display_text(code)
        time.sleep(0.1)

try:
    while True:
        client.check_msg()
        id_input = read_code()
        display_text("ID: " + id_input)
        client.publish(MQTT_TOPIC_ID, id_input)
        publish_log("ID from keypad: " + id_input)
        time.sleep(3)
        oled.fill(0)
        oled.show()
finally:
    client.disconnect()