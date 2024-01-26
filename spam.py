from functions import *

import random

token = "token lol"
channel = input("enter the channel id -> ")

words = []

with open("words.txt") as f:
    for i in f: words.append(i)

sb = Selfbot(token, channel, "!")

while 1:
    sb.send_message(random.choice(words), channel)
