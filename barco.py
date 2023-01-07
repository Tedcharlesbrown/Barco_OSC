import socket
from typing import Union
from utils import Target
import requests
import json

BARCO_IP_ADDRESS = ""

def set_barco_address(ip_address:str):
    global BARCO_IP_ADDRESS
    BARCO_IP_ADDRESS = ip_address

def convert_destination_id(n: Union[int,str]) -> int:
    if isinstance(n, int):
        return n - 1
    elif n.isdigit():
        n = int(n)

    return n - 1

def convert_layer_id(n: str) -> int:
    if n.isdigit():
        n = int(n)

    if n != 0:
        # always returns 
        return n * 2 - 2
    else:
        return n

def barco_payload(layer,opacity) -> str:
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

    return xml_layer

def send_barco_xml(target: list[Target,bool], screenDest_id: str, layers: str, opacity: int):
    global BARCO_IP_ADDRESS
    # global LATENCY, latency_average, over_average
    screenDest_id = convert_destination_id(screenDest_id)
    layers = layers.split(',')

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

    # for layer in layers:
    #     # get layer base
    #     layer = convert_layer_id(layer)
    #     if target[0] == Target.BOTH:
    #         for sub_layer in range(0,2):
    #             xml_layer = f"""
    #             <Layer id="{layer + sub_layer}">
    #             <LayerCfg id="0">
    #             <LayerState id="0">
    #             <PIP id="0">
    #             <Opacity>{opacity}</Opacity>
    #             </PIP>
    #             </LayerState>
    #             </LayerCfg>
    #             </Layer>
    #             """
    #             xml_data += xml_layer

    for layer in layers:
        # get layer base
        layer = convert_layer_id(layer)

        if target[0] == Target.BOTH:
            for sub_layer in range(0,2):
                xml_data += barco_payload(sub_layer,opacity)

        elif target[0] == Target.PROGRAM:
            # if program is odd
            if target[1]:
                layer = layer + 1
    
            xml_data += barco_payload(layer,opacity)

        elif target[0] == Target.PREVIEW:
            # if program is odd
            if target[1]:
                pass
            else:
                layer += 1

            xml_data += barco_payload(layer,opacity) 
    

    xml_data += xml_suffix

    # print(xml_data)

    print(f"Sending: DESTINATION: {screenDest_id + 1}, LAYER:{layers}, OPACITY:{opacity:.2f}")

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the specified host and port
    s.connect((BARCO_IP_ADDRESS, 9876))

    # Send the XML data over the socket
    s.sendall(xml_data.encode())

def get_barco_layers() -> bool: 
    """Returns false if 'evens' are program, true if 'odds' are program"""
    offline = True
    data = None

    # ---------------------------------------------------------------------------- #
    #                     REQUEST ONLY WORKS WITH ACTUAL BARCO                     #
    # ---------------------------------------------------------------------------- #
    if (offline == False):
        global BARCO_IP_ADDRESS
        # Set the URL and headers
        url = f"http://{BARCO_IP_ADDRESS}:9999"
        headers = {"Content-Type": "application/json"}

        # Create the JSON message
        message = {
            "params": {"id": 0},
            "method": "listContent",
            "id": "1234",
            "jsonrpc": "2.0"
        }

        # Send the request
        response = requests.post(url, headers=headers, json=message)
        
        # Extract the JSON data from the response
        data = response.json()
        # Print the response
        print(response.text)

    # ---------------------------------------------------------------------------- #
    #                   ONLY FOR OFFLINE EDITING, USE SAMPLE JSON                  #
    # ---------------------------------------------------------------------------- #

    else:
        # Open the JSON file
        with open('sample_json/sample.json', 'r') as f:
            # Load the JSON data into a Python object
            data = json.load(f)


    # ---------------------------------------------------------------------------- #
    #                                  END IF ELSE                                 #
    # ---------------------------------------------------------------------------- #
    # TODO IF NEEDED, GET ALL LAYERS
    
    # layer_0 = data['result']['response']['Layers'][0]['id']
    is_preview = bool(data['result']['response']['Layers'][0]['PvwMode'])
    print(f'PROGRAM IS ODD: {is_preview}')
    return is_preview