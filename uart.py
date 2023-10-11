import serial
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

# Configure the serial port
serial_port = serial.Serial(
    port="/dev/ttyTHS1",  # Adjust the port to match your setup
    baudrate=115200,     # Match the ESP32's baud rate
    timeout=1            # Set a timeout for reading
)

# AWS IoT Core configuration
iot_client = AWSIoTMQTTClient("inverter-monitor-data")  # Replace with your own client ID
iot_client.configureEndpoint("a3hnp0canudwcy-ats.iot.eu-west-1.amazonaws.com", 8883)  # Replace with your AWS IoT endpoint
iot_client.configureCredentials("/home/moon/inverter/certs/AmazonRootCA1.pem", "/home/moon/inverter/certs/private.pem.key", "/home/moon/inverter/certs/certificate.pem.crt")  # Replace with your certificate and key paths
iot_client.configureOfflinePublishQueueing(-1)
iot_client.configureDrainingFrequency(2)
iot_client.configureConnectDisconnectTimeout(10)
iot_client.configureMQTTOperationTimeout(5)

def is_valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False

try:
    iot_client.connect()

    while True:
        data = serial_port.readline().decode('utf-8', errors='ignore')  # Read and decode data
        if data:
            print("Received data:", data)

            if is_valid_json(data):
                iot_client.publish("your-topic", data, 1)  # Replace with your IoT topic
            else:
                print("Invalid JSON format. Message not sent.")

except KeyboardInterrupt:
    print("Exiting Program")
except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))
finally:
    iot_client.disconnect()


