from neo  import Gpio
import math
import os
from datetime import datetime
from time import sleep


class IRLearner:

	def getCode(self, protocol):
		if protocol == "sony":
			return self.getSonyCode()
		if protocol == "samsung":
			return self.getSamsungCode()
		if protocol == "epson":
			return self.getEpsonCode()
		return ""
	
	def getEpsonCode(self):
		
		# Learning mode feedback led
		pinLED = 26
		# IR receiver 
		pinIR = 25

		neo = Gpio()
		neo.pinMode(pinIR, neo.INPUT) 
		neo.pinMode(pinLED, neo.OUTPUT)
		neo.digitalWrite(pinLED, neo.HIGH)

		sample_number = 0
		# Compute the average result after MAX_SAMPLES
		bits_sum = [0] * 32
		MAX_SAMPLES = 3
		while True:

			# stop the receiver after MAX_SAMPLES 
			if sample_number == MAX_SAMPLES:
				for x in range(0, len(bits_sum)):
					bits_sum[x] = bits_sum[x] / (MAX_SAMPLES * 1.0)	 
				break

			value = 1

			# Loop until get IR data
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

			# The end of the "command" happens when we read more than
			# a certain number of 1s (1 is off for the IR receiver)
			numOnes = 0

			# Used to keep track of transitions from 1 to 0
			previousVal = 0

			while True:

				if value != previousVal:
					# The value has changed, so calculate the length of this run
					now = datetime.now()
					pulseLength = now - startTime
					startTime = now

					command.append((previousVal, pulseLength.microseconds))
	#				print str(previousVal) + " " + str(pulseLength.microseconds)
				if value:
					numOnes = numOnes + 1
				else:
					numOnes = 0

				# Stop the sample if no more IR signal is detected
				if numOnes > 100:
					break

				previousVal = value
				value = neo.digitalRead(pinIR)
			
			# A Sony IR signal starts with 2400 microseconds on and 600 microseconds off;
			# that's the first wide pulse. A "1" bit is transmitted with 1200 microseconds on and 600 microseconds off,
			# while a "0" bit is transmitted with 600 microseconds on and 600 microseconds off. 
			# (This encoding is also called SIRC or SIRCS encoding.)

			# Chop the header of the received IR signali
			for (i, j) in command:
				print str(i) + " " + str(j)
			print len(command)
			command = command[2:]
			command = command[:64]
			print len(command)
			# Establish the payload of the received IR signal
			binaryString = "".join(map(lambda x: "1" if x[1] > 1080 else "0", filter(lambda x: x[0] == 1, command)))

			# The length of the payload, according to SONY protocol is 12 bits; skip otherwise
			if len(binaryString) != 32:
				continue;
			print "OK Length"
			sample_number = sample_number + 1
			binaryString = map(int, binaryString)

			bits_sum = [sum(x) for x in zip(bits_sum, binaryString)]

		# compute the IR code based on MAX_SAMPLES
		result = ""
		for x in bits_sum:
			if x < 0.5:
				result += '0'
			else:
				result += '1'
		neo.digitalWrite(pinLED, neo.LOW)
		print result
		return result

 	
	def getSonyCode(self):
		
		# Learning mode feedback led
		pinLED = 26
		# IR receiver 
		pinIR = 25

		neo = Gpio()
		neo.pinMode(pinIR, neo.INPUT) 
		neo.pinMode(pinLED, neo.OUTPUT)
		neo.digitalWrite(pinLED, neo.HIGH)

		sample_number = 0
		# Compute the average result after MAX_SAMPLES
		bits_sum = [0] * 12
		MAX_SAMPLES = 3
		while True:

			# stop the receiver after MAX_SAMPLES 
			if sample_number == MAX_SAMPLES:
				for x in range(0, len(bits_sum)):
					bits_sum[x] = bits_sum[x] / (MAX_SAMPLES * 1.0)	 
				break

			value = 1

			# Loop until get IR data
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

			# The end of the "command" happens when we read more than
			# a certain number of 1s (1 is off for the IR receiver)
			numOnes = 0

			# Used to keep track of transitions from 1 to 0
			previousVal = 0

			while True:

				if value != previousVal:
					# The value has changed, so calculate the length of this run
					now = datetime.now()
					pulseLength = now - startTime
					startTime = now

					command.append((previousVal, pulseLength.microseconds))
	#				print str(previousVal) + " " + str(pulseLength.microseconds)
				if value:
					numOnes = numOnes + 1
				else:
					numOnes = 0

				# Stop the sample if no more IR signal is detected
				if numOnes > 100:
					break

				previousVal = value
				value = neo.digitalRead(pinIR)
			
			# A Sony IR signal starts with 2400 microseconds on and 600 microseconds off;
			# that's the first wide pulse. A "1" bit is transmitted with 1200 microseconds on and 600 microseconds off,
			# while a "0" bit is transmitted with 600 microseconds on and 600 microseconds off. 
			# (This encoding is also called SIRC or SIRCS encoding.)

			# Chop the header of the received IR signali
			print command
			command = command[1:]
			# Establish the payload of the received IR signal
			binaryString = "".join(map(lambda x: "1" if x[1] > 900 else "0", filter(lambda x: x[0] == 0, command)))

			# The length of the payload, according to SONY protocol is 12 bits; skip otherwise
			if len(binaryString) != 12:
				continue;
			sample_number = sample_number + 1
			binaryString = map(int, binaryString)

			bits_sum = [sum(x) for x in zip(bits_sum, binaryString)]

		# compute the IR code based on MAX_SAMPLES
		result = ""
		for x in bits_sum:
			if x < 0.5:
				result += '0'
			else:
				result += '1'
		neo.digitalWrite(pinLED, neo.LOW)

		return result
	
	def getSamsungCode(self):
		
		# Learning mode feedback led
		pinLED = 26
		# IR receiver 
		pinIR = 25

		command_length_samasung = 65

		neo = Gpio()
		neo.pinMode(pinIR, neo.INPUT) 
		neo.pinMode(pinLED, neo.OUTPUT)
		neo.digitalWrite(pinLED, neo.HIGH)

		sample_number = 0
		# Compute the average result after MAX_SAMPLES
		bits_sum = [0] * 32
		MAX_SAMPLES = 3
		while True:

			# stop the receiver after MAX_SAMPLES 
			if sample_number == MAX_SAMPLES:
				for x in range(0, len(bits_sum)):
					bits_sum[x] = bits_sum[x] / (MAX_SAMPLES * 1.0)	 
				break

			value = 1

			# Loop until get IR data
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

			# The end of the "command" happens when we read more than
			# a certain number of 1s (1 is off for the IR receiver)
			numOnes = 0

			# Used to keep track of transitions from 1 to 0
			previousVal = 0

			while True:

				if value != previousVal:
					# The value has changed, so calculate the length of this run
					now = datetime.now()
					pulseLength = now - startTime
					startTime = now

					command.append((previousVal, pulseLength.microseconds))
#					print str(previousVal) + " " + str(pulseLength.microseconds)
				#if len(command) == command_length_samasung:
				#	break
				if value:
					numOnes = numOnes + 1
				else:
					numOnes = 0
				if numOnes > 100:
					break
				#if numOnes > 300:
				#	break
				previousVal = value
				value = neo.digitalRead(pinIR)


			
			# A Sony IR signal starts with 2400 microseconds on and 600 microseconds off;
			# that's the first wide pulse. A "1" bit is transmitted with 1200 microseconds on and 600 microseconds off,
			# while a "0" bit is transmitted with 600 microseconds on and 600 microseconds off. 
			# (This encoding is also called SIRC or SIRCS encoding.)

			# Chop the header of the received IR signal
			# print command
			
			command = command[2:]
			command = command[:64]
			#print "Command length: " + str(len(command))
			# Establish the payload of the received IR signal
			binaryString = "".join(map(lambda x: "1" if x[1] > 1080 else "0", filter(lambda x: x[0] == 1, command)))

			# The length of the payload, according to SONY protocol is 12 bits; skip otherwise
			#print len(binaryString)
			if len(binaryString) != 32:
				continue
			#print "Good length!"
			sample_number = sample_number + 1
			binaryString = map(int, binaryString)

			bits_sum = [sum(x) for x in zip(bits_sum, binaryString)]

		# compute the IR code based on MAX_SAMPLES
		result = ""
		for x in bits_sum:
			if x < 0.5:
				result += '0'
			else:
				result += '1'
		neo.digitalWrite(pinLED, neo.LOW)

		print result
		return result

#ir = IRLearner()
#ir.getEpsonCode()
