import time
from typing import Union

from utils import remap
from utils import Target
from utils import debug
from barco import send_barco_xml

# ---------------------------------------------------------------------------- #
#                                 OSC ARGUMENTS                                #
# ---------------------------------------------------------------------------- #

def handle_args_1(address, arg_1):
    msg = OSCMessage([address,[arg_1]])
    # print(msg)
    osc_to_barco(msg)

def handle_args_2(address, arg_1, arg_2):
    msg = OSCMessage([address,[arg_1,arg_2]])
    # print(msg)
    osc_to_barco(msg)


def handle_args_3(address, arg_1, arg_2, arg_3):
    msg = OSCMessage([address,[arg_1,arg_2,arg_3]])
    # print(msg)
    osc_to_barco(msg)


def osc_to_barco(msg):
    if msg.is_fade:
        fade_xml_value(msg.fade_start,msg.fade_end,msg.fade_time,msg.destination,msg.layer)
    else:
        send_barco_xml(msg.destination,msg.layer,msg.value)
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
# 
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


# ---------------------------------------------------------------------------- #
#                                   PARSE OSC                                  #
# ---------------------------------------------------------------------------- #

class OSCMessage:
    def __init__(self,packet):
        self.destination = None
        self.layer = None
        self.is_fade = False
        self.fade_start = None
        self.fade_end = None
        self.fade_time = None
        self.target = Target.BOTH

        self.has_destination = False
        self.has_layer = False
        self.value = None

        self.parse_address(packet[0])
        self.parse_arguments(packet[1])

    def __str__(self):
        return f'DESTINATION: {self.destination}, LAYER: {self.layer}, IS FADE: {self.is_fade}, FADE START: {self.fade_start}, FADE END: {self.fade_end}, FADE TIME: {self.fade_time}, LAYER TARGET: {self.target}, VALUE: {self.value}'


# ---------------------------------------------------------------------------- #
#                                    ADDRESS                                   #
# ---------------------------------------------------------------------------- #

    def parse_address(self, packet):
        address = packet.split('/')
        # remove the first '/' from the address list
        address.pop(0)
        # check if being sent to barco
        if address[0].lower() == "barco":
            
            # remove 'barco' from the address list
            address.pop(0)

            # get layer target
            self.parse_taget_layer(address)
            address = self.parse_taget_layer(address)

            # parse if predefined fade
            address = self.parse_defined_fade(address)

            # parse destination / layers from argument
            if self.is_fade == False and len(address) != 0:
                # parse destination 
                self.destination = str(self.parse_screens(address,2)[0])
                if self.destination != None:
                    self.has_destination = True

                # parse layer
                self.layer = str(self.parse_screens(address,2)[1])
                if self.layer != None:
                    self.has_layer = True


    def parse_taget_layer(self, address) -> list:
        if len(address) != 0:
            if address[0].lower() == "program":
                address.pop(0);
                self.target = Target.PROGRAM
            elif address[0].lower() == "preview":
                address.pop(0);
                self.target = Target.PREVIEW

        return address

    def parse_defined_fade(self, address) -> list:
        if len(address) != 0:
            if address[0].lower() == "fade":
                self.is_fade = True
                address.pop(0)
                self.fade_start = address[0]
                address.pop(0)
                self.fade_end = address[0]
                address.pop(0)
                self.fade_time = address[0]

        return address

# ---------------------------------------------------------------------------- #
#                                   ARGUMENTS                                  #
# ---------------------------------------------------------------------------- #


    def parse_arguments(self,arguments):
        if self.is_fade:
            self.layer = arguments[-1]
            if len(arguments) == 2:
                self.destination = arguments[0]
            else:
                self.destination = 1
        else:
            if self.has_destination == False:
                self.destination = str(self.parse_screens(arguments,3)[0])
            if self.has_layer == False:
                self.layer = str(self.parse_screens(arguments,3)[1])

            # self.value = arguments[-1]
            self.value = self.normalize_value(arguments[-1])


    def parse_screens(self,args,expected) -> list:
        if len(args) != 0:
            if len(args) >= expected:
                return [args[0],args[1]]
            else:
                return [1,args[0]]
            

# ---------------------------------------------------------------------------- #
#                                     VALUE                                    #
# ---------------------------------------------------------------------------- #

    def normalize_value(self, value):
        if isinstance(value, float):
            return remap(value,0,1,0,100)
        else:
            return value