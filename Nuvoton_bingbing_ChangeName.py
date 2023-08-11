# pip install PySimpleGUI
# pip install pyserial

# 1. Connect BingBing board to PC
# 2. Run this script
# 3. Input your name
# 4. Click "Write Name" button
# 5. Click "Close Application" button

"""
This script is used to change BingBing board name
author: Wright Wu
email wright0418.wu@gmail.com
"""

import serial.tools.list_ports
import PySimpleGUI as sg
import datetime
from time import sleep

#  Create a PySimpleGUI window
layout = [
    [sg.Text('Please input your name')],
    [sg.InputText(key='TEXT_INPUT')],
    [sg.Button('Write Name', key='write_btn'), sg.Button(
        'Close Application', key='close_btn')],
]


window = sg.Window('BingBing Board Change Name Tool',
                   layout, font=("Arial", 20))

# Nuvoton Nu-Link USB PID/VID
NuLink_usb_ID = 'VID:PID=0416:2004'

#find and open Nu-Link Serial port
def open_serial(ports):
    global ser
    if ports:
        for index, port in enumerate(ports):
            if NuLink_usb_ID in port.hwid:
                ser = serial.Serial(port.name, baudrate=115200,
                                    bytesize=8, parity='N', stopbits=1, timeout=1)
                return "success"
            return "fail"


ser = None
ports = None
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'close_btn'):
        break
    elif event == 'write_btn':
        text = values['TEXT_INPUT'].encode()
        if ser == None:
            ports = list(serial.tools.list_ports.comports())
            status = open_serial(ports)
            if status == "fail":
                sg.popup("Please connect BlingBling board to USB port",
                         font=("Arial", 20), background_color="red")
                continue
        # send string data +\r  to BingBing board
        # board will change name to data string
        ser.write(text + b'\r')
        sg.popup("Change name success", font=(
            "Arial", 20), background_color="red")

ser.close()
window.close()
