# secure-cap
A security system with a Raspberry Pi at its core

#Code that I found from: https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python , that will return the current date and time in Python
  from datetime import datetime
  datetime.today().strftime('%Y-%m-%d') <-just for displaying year, month, and day
  datetime.today().strftime('%Y-%m-%d-%H:%M:%S') <-will return the year, month, day, hour, minute, and seconds values (we will want           to use this one)
