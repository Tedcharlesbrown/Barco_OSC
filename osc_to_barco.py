import requests
import random
from time import sleep
import time
import threading
import socket

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

def convert_layer_id(n: int) -> int:
    if n != 0:
        return n * 2 - 2
    else:
        return n

def send_barco_xml_threaded(url: str, screenDest_id: int, layer_id: int, opacity: int):
  threading.Thread(target=send_barco_xml, args=(url, screenDest_id, layer_id, opacity)).start()
  # 50 = 0.3
  # 25 = 0.5
  # 15 = 0.75
  # 11.25 = 1
  sleep_time = 0.1 / 11.25
  sleep(sleep_time)

def send_barco_xml(url: str, screenDest_id: int, layer_id: int, opacity: int):
    layer_id = convert_layer_id(layer_id)
    # <System id="0" GUID="a05950e12070-00296c" OPID="-1">
    xml_data = f"""
    <System id="0" GUID="0" OPID="0">
    <DestMgr id="0">
        <ScreenDestCol id="0">
        <ScreenDest id="{screenDest_id}">
            <LayerCollection id="0">
            <Layer id="{layer_id}">
                <LayerCfg id="0">
                <LayerState id="0">
                    <PIP id="0">
                    <Opacity>{opacity}</Opacity>
                    </PIP>
                </LayerState>
                </LayerCfg>
            </Layer>
            </LayerCollection>
        </ScreenDest>
        </ScreenDestCol>
    </DestMgr>
    </System>
    """
    print(f"Sending: DESTINATION:{screenDest_id}, LAYER:{layer_id}, OPACITY:{opacity}")

    # ------------------------------------ TCP ----------------------------------- #

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the specified host and port
    s.connect((url, 9876))

    # Send the XML data over the socket
    s.sendall(xml_data.encode())

    # Close the socket
    s.close()

    # ------------------------------------ UDP ----------------------------------- #

    # # Connect to the specified host and port
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect((url, 9876))
    
    # # Send the XML data over the socket
    # s.sendall(xml_data.encode())
    
    # # Close the socket
    # s.close()

    # ------------------------------- HTTP REQUEST ------------------------------- #

    # headers = {'Content-Type': 'application/xml'}
    # url = f'http://{url}:9876'

    # try:
    #     requests.post(url, data=xml_data, headers=headers, timeout=1.5)
    # except:
    #     pass



# #Zero Based, Screen Destination, Sequential (0,1,2,3)
# destination = 0
# #Zero Based, Layer ID, iterates by 2 (0,2,4,6)
# layer = 0

# opacity = 100
# opacity = random.randint(0, 100)

# time_start = time.time()

# print(f"START")

# for i in range(0,101):
#     send_barco_xml_threaded("127.0.0.1",destination,1,i)
#     # sleep(0.05)
#     # send_barco_xml("127.0.0.1",destination,1,i)

# print(f"FINISHED IN: {(time.time() - time_start):.2f}")

# ---------------------------------------------------------------------------- #
#                                      OSC                                     #
# ---------------------------------------------------------------------------- #


def remap(input_value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    # Scale the input value from the input range to the 0-1 range
    input_value_scaled = (input_value - in_min) / (in_max - in_min)
    # Scale the input value from the 0-1 range to the output range
    output_value = input_value_scaled * (out_max - out_min) + out_min
    return output_value

def parse_layer(address: str) -> list:
    
    if address[:7] == "/barco/":
        
        address_list = address[7:].split("/")
        return address_list

def handle_args_1(address, x):
    dest = int(parse_layer(address)[0])
    layer = int(parse_layer(address)[1])
    send_barco_xml_threaded(BARCO_IP_ADDRESS,dest,layer,int(remap(x,0,1,0,100)))


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

def main():
    global BARCO_IP_ADDRESS

    PORT_NUMBER = input("What port should be used to receive OSC? ")
    if PORT_NUMBER.isdigit():
        PORT_NUMBER = int(PORT_NUMBER)
    else:
        print("INVALID PORT NUMBER")
        main()
    BARCO_IP_ADDRESS = input("What is the IP address of the Barco Device? ")
    if isinstance(BARCO_IP_ADDRESS,str):
        print(f"Connecting to Barco Device at: {BARCO_IP_ADDRESS}")
        try:
            ping(BARCO_IP_ADDRESS)
        except:
            print("COULD NOT CONNECT TO BARCO DEVICE")
            main()
        

    print("PING SUCCESSFUL")
    print("---------------")
    print()

    # Start the system.b
    osc_startup()

    # Make server channels to receive packets.
    osc_udp_server("0.0.0.0", PORT_NUMBER, "anotherserver")


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


