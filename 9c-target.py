import bitcoin

from bitcoin.helper import hash256
from bitcoin.helper import little_endian_to_int

bits = bytes.fromhex('3c0118')
exponent = bits[-1]
coefficient = little_endian_to_int(bits[:-1])

target = coefficient * 256**(exponent-3)

True

#3c0118