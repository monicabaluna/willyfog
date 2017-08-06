from neo  import Gpio
import math
import os
from datetime import datetime
from time import sleep


class IRRawLearner:

	def getCode(self):
		
		# Learning mode feedback led
		pinLED = 26
		# IR receiver 
		pinIR = 25

		neo = Gpio()
		neo.pinMode(pinIR, neo.INPUT) 
		neo.pinMode(pinLED, neo.OUTPUT)
		neo.digitalWrite(pinLED, neo.HIGH)

		# Compute the average result after MAX_SAMPLES
		gap_number = 0
		MAX_GAPS = 3
		GAP_TIME = 20000
		
		value = 1

		time_to_live = 45000 
		while value and time_to_live:
			value = neo.digitalRead(pinIR)
			time_to_live -= 1

		if time_to_live == 0:
			neo.digitalWrite(pinLED, neo.LOW)
			return ""

		# Grab the start time of the command
		startTime = datetime.now()

		# Used to buffer the command pulses
		command = []

		# Used to keep track of transitions from 1 to 0
		previousVal = 0

		while True:

			if value != previousVal:
				# The value has changed, so calculate the length of this run
				now = datetime.now()
				pulseLength = now - startTime
				startTime = now
				if pulseLength.microseconds > GAP_TIME:
					gap_number = gap_number + 1
				if gap_number == MAX_GAPS:
					break
				command.append((previousVal, pulseLength.microseconds))

			previousVal = value
			value = neo.digitalRead(pinIR)
		
		
		neo.digitalWrite(pinLED, neo.LOW)
		result = ""
		for (i, j) in command:
			result = result + " " + str(j)
		#result = result.replace(",", "")
		result = result[1:]
		print result
		return result

ir = IRRawLearner()
ir.getCode()
