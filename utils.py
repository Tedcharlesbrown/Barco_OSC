def remap(input_value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
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