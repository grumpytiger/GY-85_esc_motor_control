#This function reads from ADXL345 and return x,y,z,time

#from __future__ import division #from base.py, for 11/4 would evaluate to 2.75, without it would be 2.
#import math #from base.py
import smbus #from i2c.py, it is a i2c communication library
import time
#assigning variables from data sheet.
REG_DEVICE_ID = 0x00
REG_THRESH_TAP = 0x1D
REG_OFSX = 0x1E
REG_OFSY = 0x1F
REG_OFSZ = 0x20
REG_DUR = 0x21
REG_LATENT = 0x22
REG_WINDOW = 0x23
REG_THRESH_ACT = 0x24
REG_THRESH_INACT = 0x25
REG_TIME_INACT = 0x26
REG_ACT_INACT_CTL = 0x27
REG_THRESH_FF = 0x28
REG_TIME_FF = 0x29
REG_TAP_AXES = 0x2A
REG_ACT_TAP_STATUS = 0x2B
REG_BW_RATE = 0x2C
REG_POWER_CTL = 0x2D
REG_INT_ENABLE = 0x2E
REG_INT_MAP = 0x2F
REG_INT_SOURCE = 0x30
REG_DATA_FORMAT = 0x31
REG_DATAX0 = 0x32
REG_DATAX1 = 0x33
REG_DATAY0 = 0x34
REG_DATAY1 = 0x35
REG_DATAZ0 = 0x36
REG_DATAZ1 = 0x37
REG_FIFO_CTL = 0x38
REG_FIFO_STATUS = 0x39

STD_ADDRESS = 0x1D
ALT_ADDRESS = 0x53

#output data rate variable:
rate_code_3200 = 0b1111
rate_code_1600 = 0b1110
rate_code_800 = 0b1101
rate_code_400 = 0b1100
rate_code_200 = 0b1011
rate_code_50 = 0b1001
rate_code_25 = 0b1000
rate_code_25_2 = 0b0111
rate_code_25_4 = 0b0110
rate_code_25_8 = 0b0101
rate_code_25_16 = 0b0100
rate_code_25_32 = 0b0011
rate_code_25_64 = 0b0010
rate_code_25_128 = 0b0001
rate_code_25_128_less = 0

SCALE_FACTOR = 1/0x100

bus=smbus.SMBus(1) #setting i2c port to 1: from i2c.py
bus.write_byte_data(ALT_ADDRESS, REG_BW_RATE, 0b1111) #i2c address, reg_bw_rate,rate code
#set_register(ADXL345_Base.REG_DATA_FORMAT, data_format): def _send_data_format from base.py
#bus.write_byte_data(ALT_ADDRESS,REG_DATA_FORMAT, 0x08) #i2c address, data format, full resolution=0x08,rate code

bus.write_byte_data(ALT_ADDRESS,REG_POWER_CTL, 0x08)  #power_ctl: sleep=0x04, measure=0x08, auto sleep=0x10, link=0x20


def acc_read(ALT_ADDRESS, REG_DATAX0):
    #set counter i =0
    i=0
    n=30
    raw_g_array=[]
    g_array=[]
    t_array=[]
    while i<n:
        t0=time.time()
        bytes = bus.read_i2c_block_data(ALT_ADDRESS, REG_DATAX0,6)

        x = bytes[0] | (bytes[1]<<8)
        if x >= 0x8000: #since x is an unsign integer, we are checking if x is negative.  0x8000 = 32768
            x = (-x^0xFFFF)+1 # two's complement: invert the bit and add 1.
        y = bytes[2] | (bytes[3]<<8)
        if y & 0x8000:
            y = (-y ^ 0xFFFF)+1
        z = bytes[4] | (bytes[5]<<8)
        if z & 0x8000:
            z = (-z ^ 0xFFFF)+1
    
        t1 = time.time()
        total_time = t1-t0
        i+=1
        raw_g_array.append(x)
        t_array.append(total_time)
        #time.sleep(1/80)

    g_array = list(map(lambda p: p*SCALE_FACTOR, raw_g_array))
    avg_t = sum(t_array)/len(t_array) #calculating the average time per sample
    return g_array, t_array, avg_t

_g_array, _t_array, avg_t =acc_read(ALT_ADDRESS, REG_DATAX0)
print("g_array= ", _g_array)
print("t_array= ", _t_array)
print("average time= ",avg_t)

