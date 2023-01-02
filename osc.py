import time
from typing import Union

from utils import normalize
from barco import send_barco_xml

def get_address(address: str, x: int) -> str:
    # print(address, type(address))

    address_list = address.split('/')
    address_list.pop(0)

    if x > len(address_list):
        return False
    elif x == -1:
        return len(address_list)
    else:
        return address_list[x]

# ---------------------------------------------------------------------------- #
#                                 OSC ARGUMENTS                                #
# ---------------------------------------------------------------------------- #

def handle_args_1(address, arg_1):
    address_length = (get_address(address,-1) - 1)

    main_address = get_address(address,0).lower()

    # IF NO SCREEN DESTINATION GIVEN, ASSUME SCREEN DESTINATION 1
    if main_address == "barco":
        if get_address(address,1).lower() == "fade" and address_length == 4:
            low_value = get_address(address,2)
            high_value = get_address(address,3)
            speed = get_address(address,4)
            layers = arg_1.split(',')
            fade_xml_value(low_value,high_value,speed,1,layers)
        elif address_length == 1:
            layers = get_address(address,1)
            layers = layers.split(',')
            send_barco_xml(1,layers,normalize(arg_1))
        elif address_length == 2:
            screen = get_address(address,1)
            layers = get_address(address,2)
            layers = layers.split(',')
            send_barco_xml(screen,layers,normalize(arg_1))
        else:
            print(f"INVALID OSC RECEIVED - CHECK ADDRESS: {address}")
    else:
        print(f"INVALID OSC RECEIVED - CHECK ADDRESS: {address}")

def handle_args_2(address, arg_1, arg_2):

    address_length = (get_address(address,-1) - 1)

    main_address = get_address(address,0).lower()

    if main_address == "barco":
        if get_address(address,1).lower() == "fade" and address_length == 4:
            low_value = get_address(address,2)
            high_value = get_address(address,3)
            speed = get_address(address,4)
            arg_2 = arg_2.split(',')
            fade_xml_value(low_value,high_value,speed,arg_1,arg_2)
        if address_length == 0:
            arg_1 = arg_1.split(',')
            send_barco_xml(1,arg_1,normalize(arg_2))
        else:
            pass
            # print(f"INVALID OSC RECEIVED - CHECK ADDRESS: {address}")
    else:
        print(f"INVALID OSC RECEIVED - CHECK ADDRESS: {address}")

def handle_args_3(address, arg_1, arg_2, arg_3):

    address_length = (get_address(address,-1) - 1)

    main_address = get_address(address,0).lower()

    if main_address == "barco":
        if address_length == 0:
            arg_2 = arg_2.split(',')
            send_barco_xml(arg_1,arg_2,normalize(arg_3))
        else:
            print(f"INVALID OSC RECEIVED - CHECK ADDRESS: {address}")
    else:
        print(f"INVALID OSC RECEIVED - CHECK ADDRESS: {address}")


# ---------------------------------------------------------------------------- #
#                                  FADE VALUE                                  #
# ---------------------------------------------------------------------------- #

def fade_xml_value(value_1: str, value_2: str, speed: str, screen: Union[int,str],layers: list):

    try:
        value_1 = float(value_1)
        value_2 = float(value_2)

        if value_1 > value_2:
            high_value = value_1
            low_value = value_2
            count_up = False
        else: 
            high_value = value_2
            low_value = value_1
            count_up = True

        speed = float(speed)
    except:
        pass

    # Calculate the total number of values to print
    num_values = high_value - low_value + 1

    # Calculate the delay between each value
    delay = speed / num_values

    if count_up:
        # Count up from low_value to high_value
        value = low_value
        increment = (high_value - low_value) / num_values
        while value <= high_value:
            send_barco_xml(screen,layers,value)
            time.sleep(delay)
            value += increment
    else:
        # Count down from high_value to low_value
        value = high_value
        increment = (low_value - high_value) / num_values
        while value >= low_value:
            send_barco_xml(screen,layers,value)
            time.sleep(delay)
            value += increment


