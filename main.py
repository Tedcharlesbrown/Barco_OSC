from time import sleep
from pythonping import ping

from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm

import osc4py3

from osc import *
from barco import set_barco_address

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

def main():
    global last_packet
    port_number = input("What port should be used to receive OSC? ")
    if port_number.isdigit():
        port_number = int(port_number)
    else:
        print("INVALID PORT NUMBER")
        main()
    barco_ip_address = input("What is the IP address of the Barco Device? ")
    if isinstance(barco_ip_address,str):
        print(f"Connecting to Barco Device at: {barco_ip_address}")
        try:
            ping(barco_ip_address)
        except:
            print("COULD NOT CONNECT TO BARCO DEVICE")
            main()
    # barco_ip_address = "127.0.0.1"
    # port_number = 7400
        
    print("PING SUCCESSFUL")
    set_barco_address(barco_ip_address)
    print("---------------")
    print("STARTING OSC SERVER")
    print("---------------")

    # Start the system.b
    osc_startup()

    print("OSC SERVER STARTED")
    print("---------------")

    

    # Make server channels to receive packets.
    # osc_udp_server("0.0.0.0", port_number, "anotherserver")
    osc_udp_server("0.0.0.0", port_number, "anotherserver")
    osc_method("/*", handle_args_1, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)
    osc_method("/*", handle_args_2, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)
    osc_method("/*", handle_args_3, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)


    # Periodically call osc4py3 processing method in your event loop.
    # finished = False
    # while not finished:
    while True:
        # …
        osc_process()
        sleep(0.0025)
        # …

    # Properly close the system.
    osc_terminate()

# ----------------------------------- MAIN ----------------------------------- #

if __name__ == "__main__":
    # get_barco_layers()
    main()



