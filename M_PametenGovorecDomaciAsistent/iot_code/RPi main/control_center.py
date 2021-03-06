from flask import Flask
from flask_ask import Ask, statement, convert_errors
import logging
import srmlib_ublox as srmlib

url = "https://193.2.179.243:46300"
https_check = srmlib.HTTPS_BASIC
verbose = True
client = srmlib.SRMClient(url=url, https_check=https_check, verbose=verbose)

rewards = [(-1,"did not do well"), (1,"is ok"), (2,"did well")]
algoreward = [0]

leds = []
for i in range(3):
    led_url = srmlib.url_builder(url=url, path='/log/integer/{}/value'.format(i))
    led = srmlib.SRMClient(url=led_url, https_check=https_check, verbose=verbose)
    leds.append(led)

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@app.route('/')
def home_page():
    return '<h1>Welcome to my site!</h1>'

@ask.intent('RewardIntent', mapping={'reward': 'reward'})
def reward_control(reward):
    reward = reward.lower()
    for val, command in rewards:
        if reward in command:
            algoreward[0] += val
            return statement('Added {}, avarage reward is now {}.'.format(val, algoreward[0]))
    return statement('Reward {} is not defined.'.format(reward))

@ask.intent('LightControlIntent', mapping={'status': 'status', 'light': 'light'})
def light_control(status, light):

    led_state = 0
    if status in 'on':    led_state = 1
    elif status in 'off':    led_state = 0
    else:    return statement('Status {} is invalid.'.format(status))

    light_num = int(light)
    if light_num > 0 and light_num < 4:
        leds[light_num-1].put(data=led_state)
        return statement('Turning light {} {}'.format(light, status))
    else:
        return statement('Light {} does not exist.'.format(light))

if __name__ == '__main__':
    app.run()
