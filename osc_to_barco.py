import requests
import random
from time import sleep
import time
import threading
import socket

import xml.etree.ElementTree as ET

import json

import pythonping
from pythonping import ping

from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm


BARCO_IP_ADDRESS = ""

# ---------------------------------------------------------------------------- #
#                                   TCP BARCO                                  #
# ---------------------------------------------------------------------------- #

# def is_pingable(ip_address: str) -> bool:
#     response = pythonping.ping(ip_address)
#     return response.success

def convert_destination_id(n: int) -> int:
    return n - 1

def convert_layer_id(n: str) -> int:
    if n.isdigit():
        n = int(n)

    if n != 0:
        return n * 2 - 2
    else:
        return n

# def send_barco_xml_threaded(url: str, screenDest_id: int, layers: list, opacity: int):
#     threading.Thread(target=send_barco_xml, args=(url, screenDest_id, layers, opacity)).start()
# #   50 = 0.3
#   # 25 = 0.5
#   # 15 = 0.75
#   # 11.25 = 1
#     sleep_time = 0.1 / 11.25
#     # sleep_time = 0.5
#     sleep(sleep_time)

# def send_barco_xml(url: str, screenDest_id: int, layers: list, opacity: int):
#     screenDest_id = convert_destination_id(screenDest_id)

#     xml_data =f"""
#     <System id="0" GUID="0" OPID="0">
#     <DestMgr id="0">
#     <ScreenDestCol id="0">
#     <ScreenDest id="{screenDest_id}">
#     <LayerCollection id="0">
#     """

#     xml_suffix = f"""
#     </LayerCollection>
#     </ScreenDest>
#     </ScreenDestCol>
#     </DestMgr>
#     </System>
#     """

#     for layer in layers:
#         layer = convert_layer_id(layer)

#         # print(layer)

#         xml_layer = f"""
#         <Layer id="{layer}">
#         <LayerCfg id="0">
#         <LayerState id="0">
#         <PIP id="0">
#         <Opacity>{opacity}</Opacity>
#         </PIP>
#         </LayerState>
#         </LayerCfg>
#         </Layer>
#         """

#         xml_data += xml_layer

#     xml_data += xml_suffix

#     # print(f"Sending: DESTINATION:{screenDest_id}, LAYER:{layer_id}, OPACITY:{opacity}")
#     # print(f"Sending: DESTINATION:{screenDest_id}, OPACITY:{opacity}")
    
#     # Create a TCP socket
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # Connect to the specified host and port
#     s.connect((url, 9876))

#     # Send the XML data over the socket
#     s.sendall(xml_data.encode())

#     # Receieve Data
#     data = s.recv(9876)

#     # Close the socket
#     s.close()

#     # # Send 4 ICMP echo request packets to the specified host and measure the latency
#     # latency = pythonping.ping(url, count=1)

#     # # Print the latency
#     # print(f'Latency: {latency.rtt_avg:.2f} seconds')

def send_barco_xml_threaded(url: str, screenDest_id: int, layers: list, opacity: int, start_time: float):
    threading.Thread(target=send_barco_xml, args=(url, screenDest_id, layers, opacity,start_time)).start()
#   50 = 0.3
  # 25 = 0.5
  # 15 = 0.75
  # 11.25 = 1
    # sleep_time = 0.1 / 11.25
    sleep_time = 1
    sleep(sleep_time)

LATENCY = 0

def send_barco_xml(url: str, screenDest_id: int, layers: list, opacity: int, start_time: float):
    global LATENCY
    screenDest_id = convert_destination_id(screenDest_id)

    xml_data =f"""
    <System id="0" GUID="0" OPID="0">
    <DestMgr id="0">
    <ScreenDestCol id="0">
    <ScreenDest id="{screenDest_id}">
    <LayerCollection id="0">
    """

    xml_suffix = f"""
    </LayerCollection>
    </ScreenDest>
    </ScreenDestCol>
    </DestMgr>
    </System>
    """

    for layer in layers:
        layer = convert_layer_id(layer)

        # print(layer)

        xml_layer = f"""
        <Layer id="{layer}">
        <LayerCfg id="0">
        <LayerState id="0">
        <PIP id="0">
        <Opacity>{opacity}</Opacity>
        </PIP>
        </LayerState>
        </LayerCfg>
        </Layer>
        """

        xml_data += xml_layer

    xml_data += xml_suffix

    # print(f"Sending: DESTINATION:{screenDest_id}, LAYER:{layer_id}, OPACITY:{opacity}")
    # print(f"Sending: DESTINATION:{screenDest_id}, OPACITY:{opacity}")
    # print(LATENCY)

    if LATENCY < 0.1:
    
        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the specified host and port
        s.connect((url, 9876))

        # Send the XML data over the socket
        s.sendall(xml_data.encode())

        # Receieve Data
        data = s.recv(9876)

        # Calculate the elapsed time
        LATENCY = time.time() - start_time

        # Print the latency
        print(f'Latency: {LATENCY:.2f} seconds')
    
    else: 
        sleep(0.5)
        LATENCY = 0



        # Close the socket
        s.close()

# ---------------------------------------------------------------------------- #
#                                      OSC                                     #
# ---------------------------------------------------------------------------- #


def remap(input_value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    # Scale the input value from the input range to the 0-1 range
    input_value_scaled = (input_value - in_min) / (in_max - in_min)
    # Scale the input value from the 0-1 range to the output range
    output_value = input_value_scaled * (out_max - out_min) + out_min
    return output_value

def remap_value(input_value: float) -> float:
    # Scale the input value from the input range to the 0-1 range
    input_value_scaled = (input_value - 0) / (1 - 0)
    # Scale the input value from the 0-1 range to the output range
    output_value = input_value_scaled * (100 - 0) + 0
    return output_value

def get_address(address: str, x: int) -> str:
    address_list = address.split('/')
    address_list.pop(0)

    if x > len(address_list):
        return False
    elif x == -1:
        return len(address_list)
    else:
        return address_list[x]

def handle_args_1(address, value):
    # Record the current time
    start_time = time.time()

    address_length = (get_address(address,-1) - 1)

    # print(address_length)
    main_address = get_address(address,0).lower()

    # IF NO SCREEN DESTINATION GIVEN
    if main_address == "barco" and address_length == 1:
        layers = get_address(address,1)
        layers = layers.split(',')
        # send_barco_xml("192.168.0.143",1,layers,remap_value(value))
        send_barco_xml("192.168.0.143",1,layers,remap_value(value),start_time)



# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

def main():
    # global BARCO_IP_ADDRESS

    # PORT_NUMBER = input("What port should be used to receive OSC? ")
    # if PORT_NUMBER.isdigit():
    #     PORT_NUMBER = int(PORT_NUMBER)
    # else:
    #     print("INVALID PORT NUMBER")
    #     main()
    # BARCO_IP_ADDRESS = input("What is the IP address of the Barco Device? ")
    # if isinstance(BARCO_IP_ADDRESS,str):
    #     print(f"Connecting to Barco Device at: {BARCO_IP_ADDRESS}")
    #     try:
    #         ping(BARCO_IP_ADDRESS)
    #     except:
    #         print("COULD NOT CONNECT TO BARCO DEVICE")
    #         main()
        

    # print("PING SUCCESSFUL")
    # print("---------------")
    # print()

    # Start the system.b
    osc_startup()

    # Make server channels to receive packets.
    # osc_udp_server("0.0.0.0", PORT_NUMBER, "anotherserver")
    osc_udp_server("0.0.0.0", 7400, "anotherserver")


    osc_method("/*", handle_args_1, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)

    # Periodically call osc4py3 processing method in your event loop.
    finished = False
    while not finished:
        # …
        osc_process()
        sleep(0.0025)
        # …

    # Properly close the system.
    osc_terminate()

# ----------------------------------- MAIN ----------------------------------- #

if __name__ == "__main__":
    main()


