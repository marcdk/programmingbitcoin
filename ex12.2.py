import bitcoin

from bitcoin.bloomfilter import BloomFilter, BIP37_CONSTANT
from bitcoin.helper import bit_field_to_bytes, murmur3

field_size = 10
function_count = 5
tweak = 99
items = (b'Hello World',  b'Goodbye!')
bit_field_size = field_size * 8
bit_field = [0] * bit_field_size

for item in items:
    for i in range(function_count):
        seed = i * BIP37_CONSTANT + tweak
        h = murmur3(item, seed=seed)
        bit = h % bit_field_size
        bit_field[bit] = 1

print(bit_field_to_bytes(bit_field).hex())
