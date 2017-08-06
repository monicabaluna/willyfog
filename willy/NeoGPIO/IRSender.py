from datetime import datetime
import shlex
import serial
import subprocess
import time
senders = {"nec": "NECTransmitter.cpp.bin", "sony":"SONYTransmitter.cpp.bin", "samsung":"SamsungTransmitter.cpp.bin", "epson":"EpsonTransmitter.cpp.bin"}

class IRSender:
    def __init__(self):
        pass

    # for future use
    def send(self, code, protocol):
        if protocol:
            print "sending IR code " + str(code) + " on " + protocol + " protocol"
            print senders[protocol]

            # upload the SONYTransmitter on Arduino
            subprocess.call(shlex.split('udooneo-m4uploader /home/udooer/monica/lec_2017_willyfog/willy/NeoGPIO/' + senders[protocol]))

            # Open a serial connection
            ser = serial.Serial("/dev/ttyMCC", 115200)
            ser.flush()

            connect = False
            while not connect:
                from_ard = ser.readline()
                connect = True
            print from_ard
            
            ser.write(str(code))
            time.sleep(2)
            ser.close()
        else:
            print "unknown device"

    # def send(self, code):
        # # upload the SONYTransmitter on Arduino
        # subprocess.call(shlex.split('udooneo-m4uploader /home/udooer/monica/lec_2017_willyfog/willy/NeoGPIO/SONYTransmitter.cpp.bin'))
        # print str(datetime.now()) + " sending IR code " + str(code)
        # Open a serial connection 
# 	ser = serial.Serial("/dev/ttyMCC", 115200)

# 	ser.flush()
# 	connect = False
#         while not connect:
# 	        from_ard = ser.readline()
# 	        connect = True
#         print from_ard
# 	ser.write(str(code))
# 	time.sleep(2)
# 	ser.close()
#ir = IRSender()
#ir.send("11000001101010100000100111110110", "epson")
#ir.send("000000010000")
