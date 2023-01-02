from time import sleep
from pythonping import ping

from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm

from osc import *
from barco import set_barco_address

# BARCO_IP_ADDRESS = ""

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
    barco_ip_address = input("What is the IP address of the Barco Device? ")
    if isinstance(barco_ip_address,str):
        print(f"Connecting to Barco Device at: {barco_ip_address}")
        try:
            ping(barco_ip_address)
        except:
            print("COULD NOT CONNECT TO BARCO DEVICE")
            main()

    # PORT_NUMBER = 9876
    # barco_ip_address = "192.168.0.143"
        

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
    # osc_udp_server("0.0.0.0", PORT_NUMBER, "anotherserver")
    osc_udp_server("0.0.0.0", 7400, "anotherserver")
    osc_method("/*", handle_args_1, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)
    osc_method("/*", handle_args_2, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)
    osc_method("/*", handle_args_3, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)

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


