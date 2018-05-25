import math
import struct

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

def float_to_hex(number):
    return "%0.8x" % struct.unpack('<I', struct.pack('<f', number))[0]

def hex_to_float(hex_string):
    return struct.unpack('!f', bytes.fromhex(hex_string))[0]

def equal(f):
    test_f = truncate(hex_to_float(float_to_hex(f)), 8)
    
    return f == test_f, test_f, test_f - f
    
print(equal(12.2))
