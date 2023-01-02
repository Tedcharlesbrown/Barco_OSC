import socket
from typing import Union
# from osc_to_barco import BARCO_IP_ADDRESS

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
        return n * 2 - 2
    else:
        return n

# TODO: Lerp between opacity before and after sleep
# TODO: Add over average time, don't sleep, but wait a couple seconds to continue sending

# LATENCY = 0
# latency_average = []
# over_average = False

def send_barco_xml(screenDest_id: str, layers: list, opacity: int):
    global BARCO_IP_ADDRESS
    # global LATENCY, latency_average, over_average
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


    print(f"Sending: DESTINATION: {screenDest_id + 1}, LAYER:{layers}, OPACITY:{opacity:.2f}")

    # average_limit = 0.10
    # latency_limit = 0.15
    # if LATENCY < latency_limit:

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the specified host and port
    s.connect((BARCO_IP_ADDRESS, 9876))

    # Send the XML data over the socket
    s.sendall(xml_data.encode())

    # # Receieve Data
    # data = s.recv(9876)

    # # Calculate the elapsed time
    # LATENCY = time.time() - start_time

    # Close the socket
    # s.close()
    # else:
    #     print(f"LATENCY TOO HIGH, SLEEPING: {(LATENCY - latency_limit):.2f}")
    #     sleep(LATENCY - latency_limit)
    #     LATENCY = 0
    

    # ------------------------------ AVERAGE LATENCY ----------------------------- #

    # latency_average.append(LATENCY)
    # if len(latency_average) > 10:
    #     latency_average.pop(0)

    # # Calculate the average of the latencies
    # avg_latency = sum(latency_average) / len(latency_average)

    # if avg_latency > average_limit:
    #     print(f"AVERAGE LATENCY TOO HIGH: {avg_latency}, SLEEPING TO PREVENT CRASH")
    #     sleep(1)
        
    # else:
    #     # Print the average latency
    #     print(f'Average Latency: {avg_latency:.2f} seconds')