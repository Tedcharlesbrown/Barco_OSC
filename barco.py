import socket
from typing import Union

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

def send_barco_xml(screenDest_id: str, layers: str, opacity: int):
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

    for layer in layers:
        
        # get layer base
        layer = convert_layer_id(layer)

        for sub_layer in range(0,2):
            xml_layer = f"""
            <Layer id="{layer + sub_layer}">
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


    print(f"Sending: DESTINATION: {screenDest_id + 1}, LAYER:{layers}, OPACITY:{opacity:.2f}")

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the specified host and port
    s.connect((BARCO_IP_ADDRESS, 9876))

    # Send the XML data over the socket
    s.sendall(xml_data.encode())
