from enum import Enum
from typing import Union

class Target(Enum):
    BOTH = 0
    PROGRAM = 1
    PREVIEW = 2

def remap(input_value: Union[int, float], in_min: Union[int, float], in_max: Union[int, float], out_min: Union[int, float], out_max: Union[int, float]) -> Union[int, float]:
    # Scale the input value from the input range to the 0-1 range
    input_value_scaled = (input_value - in_min) / (in_max - in_min)
    # Scale the input value from the 0-1 range to the output range
    output_value = input_value_scaled * (out_max - out_min) + out_min
    return output_value

def normalize(input_value: float) -> float:
    # Scale the input value from the input range to the 0-1 range
    input_value_scaled = (input_value - 0) / (1 - 0)
    # Scale the input value from the 0-1 range to the output range
    output_value = input_value_scaled * (100 - 0) + 0
    return output_value

def debug():
    print("TEST")