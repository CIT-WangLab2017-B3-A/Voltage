#!/usr/bin/python
#coding: utf-8
import os
import wiringpi as wp
import time

class Voltage:
    def __init__(self):
        # SPI channle (0 or 1)
        self.MCP_CH = 0
        # pin base (above 64)
        self.PIN_BASE = 70
        # setup
        wp.mcp3002Setup (self.PIN_BASE, self.MCP_CH)
        wp.wiringPiSetupGpio()
    def Read(self):
        # registance
        #R1 = 4.10*1000.0  # [Ω]
        #R2 = 5.32*1000.0  # [Ω]
        R1 = 3.9 * 1000.0  # [Ω]
        R2 = 5.6 * 1000.0  # [Ω]
        SumRegistance = R1 + R2

        #voltage
        Vcc_MAX = 12.0 # [V]
        Vdd = 4.8 # [V]
        Vref = Vdd
        Vlsb = Vref/1024.0

        #amplitude
        #Iin = 0.0 # [A]
        Iin = 0.000655 # [A]

        mcp3002_data = float(wp.analogRead(self.PIN_BASE + self.MCP_CH))
        Vin = ((mcp3002_data/1024.0) * Vdd) # 2.988[V] if Vcc=7.4[V]
        return ((Vin/R2) + Iin) * SumRegistance

# class setup
v = Voltage()

# value
flag = False

# limit
Vcc_cat = 3.0
Vset = 7.4 if v.Read()<9.0 else 11.1
Vcc_shutdown = Vset*0.85
Vcc_beep = Vset*0.9

while True:
    Vcc = 0.0
    for i in xrange(10):
    	Vcc += v.Read()
    Vcc = Vcc / 10

    if Vcc < Vcc_cat:
        pass
    elif Vcc < Vcc_shutdown:
        print "<ここでシャットダウン操作>"
        time.sleep(1.0)
        os.system('sudo poweroff')
    elif Vcc < Vcc_shutdown+0.2: # <3.15[V/cel](絶対目安)
        os.system("sudo  /home/pi/Program/Voltage/buzzer tel")
        print "ヤバイ(早く充電): ",
    elif Vcc < Vcc_beep: # 3.15<3.3[V/cel](安心目安)
    	if flag == False:
            os.system("sudo /home/pi/Program/Voltage/buzzer mac")
	    flag = True
        print "ピンチ(そろそろ充電): ",
    else:
        print "大丈夫(使用可能): ",
        pass
    print Vcc
    time.sleep(0.1)
