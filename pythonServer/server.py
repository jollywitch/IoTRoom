import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from flask import *
import threading
import serial
import time
import json
import get
import re
import os

HOST = "localhost"
PORT = 1883
LED_PIN = 14
MOTOR_PIN1 = 5
MOTOR_PIN2 = 6

class Sensor():
    def __init__(self):
        self.serialPort = os.popen("ls /dev/ttyACM*").read().strip()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.setup(MOTOR_PIN1, GPIO.OUT)
        GPIO.setup(MOTOR_PIN2, GPIO.OUT)
        self.arduino = serial.Serial(self.serialPort, '9600', timeout=1)
        self.client = mqtt.Client("Publisher")
        time.sleep(2)
        self.dataList = []
        self.optimalTemp = 0.0
        self.optimalLumi = 0.0
        self.initMemberVar()

    def initMemberVar(self):
        self.client.connect(HOST, PORT)
        if not os.path.exists("setting.json"):
            with open("setting.json", "w") as file:
                json.dump({"temp": 24.0, "lumi": 30.0}, file, indent=4)
                print("Setting file created with default values")
        with open("setting.json", "r") as file:
            data = json.load(file)
        self.optimalTemp = data["temp"]
        self.optimalLumi = data["lumi"]
        print("Init complete")

    def getDataBySerial(self):
        dataString = self.arduino.readline().decode().strip()
        dataList = list(map(float, dataString.split(",")))
        if len(dataList) != 4:
            raise IndexError
        
        return dataList

    def loopGetDataBySerial(self):
        while True:
            try:
                self.dataList = self.getDataBySerial()
                self.checkActuator()
                self.publishData()
            except Exception as e:
                print(e)


    def publishData(self):
        self.client.publish("/temp", self.dataList[0])
        self.client.publish("/humi", self.dataList[1])
        self.client.publish("/heat_index", self.dataList[2])
        self.client.publish("/lumi", self.dataList[3])

    def checkActuator(self):
        if self.dataList[3] <= self.optimalLumi:
            GPIO.output(LED_PIN, GPIO.HIGH)
        elif self.dataList[3] > self.optimalLumi:
            GPIO.output(LED_PIN, GPIO.LOW)
        if self.dataList[2] <= self.optimalTemp:
            GPIO.output(MOTOR_PIN1, GPIO.LOW)
            GPIO.output(MOTOR_PIN2, GPIO.LOW)
        elif self.dataList[2] > self.optimalTemp:
            GPIO.output(MOTOR_PIN1, GPIO.HIGH)
            GPIO.output(MOTOR_PIN2, GPIO.LOW)
    
    def __del__(self):
        self.arduino.close()
        self.client.disconnect()
        GPIO.cleanup()

app = Flask(__name__)
sensor = Sensor()

@app.route('/', methods = ["GET", "POST"])
def index():
    temp = sensor.optimalTemp
    lumi = sensor.optimalLumi

    if request.method == "POST":
        sensor.optimalTemp = float(request.form.get("temp"))
        sensor.optimalLumi = float(request.form.get("lumi"))
        with open("setting.json", "w") as file:
            json.dump({"temp": sensor.optimalTemp, "lumi": sensor.optimalLumi}, file, indent=4)
        return render_template("index.html", title="IoT 설정 페이지", temp=sensor.optimalTemp, lumi=sensor.optimalLumi, toast_message="적용 완료")
    return render_template("index.html", title="IoT Configure", temp=temp, lumi=lumi)

if __name__ == "__main__":
    threading.Thread(target=sensor.loopGetDataBySerial).start()
    threading.Thread(target=app.run, kwargs={"debug": False, "host": "0.0.0.0"}).start()
