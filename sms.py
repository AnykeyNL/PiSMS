from flask import Flask
import os
import time
import serial

port="/dev/ttyUSB0"   # Using adafruit Fona connected thru USB FTDI serial cable with 3.3v logic
ser = serial.Serial(port,9600,timeout=1)

app = Flask(__name__)

@app.route('/')
def info():
    print ("Main page")
    return "SMS Gateway"

@app.route('/send/<number>/<msg>')
def send(number, msg):
    print ("{} - {}".format(number,msg))
    cmd = "AT+CMGF=1\n"

    ser.write(cmd)
    cmd = "AT+CMGS=\"" + str(number) + "\"\n"
    msgend = chr(26)
    ser.write(cmd)
    ser.write(str(msg))
    ser.write(msgend)
    return "Message send!"

@app.route('/battery')
def battery():
    cmd = "AT+CBC\n"
    ser.write(cmd)
    w = 0
    while (w<10):
        line = ser.readline()
        w = w + 1
        f = line.split(" ")
        if (f[0] == "+CBC:"):
                d = f[1].split(",")
                print ("Charging: {} - Battery level: {} - Voltage: {}".format(d[0],d[1],d[2]))
                w = 11
    return("Charging: {} - Battery level: {} - Voltage: {}".format(d[0],d[1],d[2]))

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
