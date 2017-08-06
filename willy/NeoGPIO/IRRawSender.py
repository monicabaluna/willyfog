from datetime import datetime
import shlex
import serial
import subprocess
import time
senders = {"NEC": "NECTransmitter.ino", "Sony":"SONYTransmitter.ino"}

class IRSender:
    def __init__(self):
        pass

    # for future use
    def send(self, code, protocol):
        print "sending IR code " + str(code)
        print senders[protocol]

    def send(self, code):
        # upload the SONYTransmitter on Arduino
        subprocess.call(shlex.split('udooneo-m4uploader /home/udooer/monica/lec_2017_willyfog/willy/NeoGPIO/RawTransmitter.cpp.bin'))
        print str(datetime.now()) + " sending IR code " + str(code)
        # Open a serial connection 
        ser = serial.Serial("/dev/ttyMCC", 115200)
        # Wait for arduino to establish the serial connection
        connect = False
        while not connect:
	        from_ard = ser.readline()
	        connect = True
        # Write the code to be sent on the serial connection
        code = code + " #"
        ser.write(str(code))
        time.sleep(2)
        ser.close()

ir = IRSender()
ir.send("4587 4562 464 1798 466 1761 618 1589 605 441 604 601 599 427 608 609 849 289 644 1606 613 1597 613 1594 613 600 606 429 747 475 448 610 604 432 604 602 613 604 436 1597 609 604 597 597 673 473 450 626 607 436 605 1741 617 1585 609 605 433 1792 453 1776 5677 917 1005 46614 4453 4526 628 1595 616 1552 634 1600 1963 490 453 616 611 433 598 603 602 1631 636 1594 603 1606 606 598 598 434 594 610 601 618 518 465 614 438 599 609 602 1580 605 602 601 433 608 603 592 553 483 625 617 1590 606 1587 787 494 441 3875 650 1627 619 1595 604 1746 615 46719 4938 4210 655 1449 619 1757 609 1608 634 445 594 607 597 434 610 604 611 425 595 1601 615 1730 643 1587 613 3203 352 289 624 615 694 315 641 621 437 1735 615 432 601 617 802 287 619 441 611 610 813 1359 629 1591 611 617 612 1588 618 1577 722 1521 620 1595 659 1911 304")
