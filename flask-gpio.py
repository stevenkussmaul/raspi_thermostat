from flask import Flask, render_template
import datetime
import RPi.GPIO as GPIO
import tempSensor

app = Flask(__name__)
GPIO.cleanup()
pin_list = [17,27,22,23]
GPIO.setmode(GPIO.BCM)
try:
  GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.HIGH)
  #GPIO.setup(pin_list, GPIO.HIGH)
except:
  print ("error: gpio not set up right")
  GPIO.cleanup()
  GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.HIGH)
finally: 
  print ("reached finally")

setPoint = 20

@app.route("/")
def index():
  #now = datetime.datetime.now()
  #timeString = now.strftime("%Y-%m-%d %H:%M")
  templateData = returnData()
  return render_template('index.html', **templateData)

@app.route("/relay/<pin>/")
def relay(pin):
  currentPin = int(pin)
  print ("relaypowered : " + str(not GPIO.input(currentPin)))
  if GPIO.input(currentPin):
    GPIO.output(currentPin, GPIO.LOW)
  else:
    GPIO.output(currentPin, GPIO.HIGH)
 # return "relaypowered : " + str(not GPIO.input(currentPin))
  return index()
      
@app.route('/temperature/<actionType>', methods=["GET"])
def button(actionType):
    global setPoint
    if actionType == "up": 
      setPoint += 1
    elif actionType == "down":
      setPoint -= 1
    return render_template("index.html", returnData())

@app.route("/exit/")
def exit():
  GPIO.cleanup()
  sys.exit()

def returnData():
  global setPoint
  templateData = {
    #'title' : 'HELLO!',
    #'time': timeString,
    relay17: not GPIO.input(17),
    relay22: not GPIO.input(22),
    relay23: not GPIO.input(23),
    relay27: not GPIO.input(27),
    temperature: tempSensor.getTemp("C"),
    setPoint: setPoint
  }
  return templateData
    

try:
  if __name__ == "__main__":
    print ("tempSensor file location: " + tempSensor.device_file )
    tempSensor.temp_sensor_init()
    print ("tempSensor file location: " + tempSensor.device_file)
    temperatures = tempSensor.read_temp()
    print ("temperature: " + str(temperatures[0]) + "C" + str(temperatures[1]) + "F")
    app.run(host='0.0.0.0', port=80, debug=False)
except KeyboardInterrupt:
  print ("keyboard inturrupt")
finally:
  print ("exiting with cleanup")
  GPIO.cleanup()

