import network
import urequests
import json
from machine import Pin, PWM, I2C, Timer
from time import sleep_ms, sleep
import ssd1306

### init LED Display
oled_width = 128
oled_height = 64
i2c_rst = Pin(16, Pin.OUT)
i2c_rst.value(0)
sleep(1)
i2c_rst.value(1)
i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl = i2c_scl, sda=i2c_sda)
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

### Port Definition
ledPins = [Pin(32, Pin.OUT), 
Pin(33, Pin.OUT), 
Pin(12, Pin.OUT), 
Pin(13, Pin.OUT)]

btnPins = [Pin(22, Pin.IN, Pin.PULL_UP),
Pin(2, Pin.IN, Pin.PULL_UP),
Pin(23, Pin.IN, Pin.PULL_UP),
Pin(17, Pin.IN, Pin.PULL_UP)]

pwm1 = PWM(Pin(0))
pwm1.deinit()

timer0 = Timer(0)

delay_ms = 200

def server_post(url, json_data):
  return urequests.post(server_url + url, headers = {'content-type': 'application/json'}, data=json_data).json()
  
def server_get(url):
  return urequests.get(server_url + url).json()

def server_get_par(url, parameter):
  return urequests.get(server_url + url + '?' + parameter).json()

# print text on Display
def show_text(text):
  oled.fill(0)
  oled.text(text, 0, 15)
  oled.show()
  
def show_text2(text):
  oled.text(text, 0, 30)
  oled.show()
  
def show_text3(text):
  oled.text(text, 0, 45)
  oled.show()
  
def ind_freq(index):
  if index == 3:
    freq = 196
  elif index == 2:
    freq = 262
  elif index == 1:
    freq = 330
  elif index == 0:
    freq = 392
  else:
    freq = 440
  return freq
  
def showLEDs(leds):
  for led in ledPins:
    led.value(0)
      
  for led in leds:
    play_sound(ind_freq(led), 200)
    ledPins[led].value(1)
    sleep_ms(delay_ms)
    ledPins[led].value(0)
    sleep_ms(delay_ms * 2)

def read_button_input(n):
  buttonInput = []
  i = 0
  prevButtons = [1, 1, 1, 1]
  show_text('progress ' + str(i) + '/' + str(n))
  while i < n:
    tracked = False
    for count, btn in enumerate(btnPins):
      if btn.value() == 0 and prevButtons[count] == 1:
        play_sound(ind_freq(count), 200)
        tracked = True
        buttonInput.append(count)
      ledPins[count].value(1 - btn.value())
      prevButtons[count] = btn.value()
    sleep_ms(5)
      
    if tracked == True:
      i = i + 1
      tracked = False
      show_text('progress ' + str(i) + '/' + str(n))
  for led in ledPins:
    led.value(0)
  return buttonInput
  
def speaker_deinit(self):
  pwm1.deinit()
  
def play_sound(freq, duration):
  pwm1.init()
  pwm1.freq(freq)
  timer0.init(period=duration, mode=Timer.ONE_SHOT, callback=speaker_deinit)

def light_all():
  for led in ledPins:
    led.value(1)
  sleep_ms(delay_ms)
  for led in ledPins:
    led.value(0)
  sleep_ms(delay_ms)
  


### connect to wifi
print('connect to wifi')
show_text('Connecting...')

wifi_ssid = "abcdefg"
wifi_password = "1gF05721"
server_url = "http://128.131.206.83:5000"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while not wlan.isconnected():
  pass

print('connected')
show_text('Welcome!')
show_text2('Please wait...')

  
light_all()
light_all()

response = server_post('/ready', {})
#print(response)

client = response['clientnumber']
print('client number: ' + str(client))

response = {'message':'not ok'}
while response['message'] != 'OK':
  response = server_get('/start')
  #print(response)
  sleep(1)

max_rounds = response['rounds']
  
finished = False
new_round = True
cur_round = 0
while not finished:
  if new_round == True:
    cur_round += 1
    show_text('Round ' + str(cur_round) + ' of ' + str(max_rounds))
    server_post('/round_start', {})
    new_round = False
    
  response = server_get('/round')
  leds = response['leds']
  print('leds:', leds)
  showLEDs(leds)
  sleep_ms(delay_ms)

  input = read_button_input(response['round'] + 1)
  print('input:', input)
  show_text('Waiting for')
  show_text2('other players...')


  parameters = {"player": client, "leds": input}
  #print(parameters)
  response = server_post('/round_finished', json.dumps(parameters))['message']
  print('round was ' + response)
  
  while response == 'WAIT':
    response = server_post('/round_finished', json.dumps(parameters))['message']
    print('round was ' + response)
    sleep_ms(100)
    
  if response == 'OK':
    show_text('Correct!')  
    play_sound(1000, 250)
  elif response == 'FINISH':
    response = server_get('/score')
    play_sound(1200, 400)
    show_text('Your score: ' + str(response['score'][client]))
    response = server_get_par('/my_place', 'player=' + str(client))
    show_text2('Your rank: ' + str(response['place']) + '.')
    show_text3('Thx for playing!')
    finished = True
  else:
    show_text('FAIL!')
    play_sound(100, 250)
    
  new_round = True
  sleep(2)

