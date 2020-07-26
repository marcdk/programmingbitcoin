import bitcoin

from bitcoin.helper import hash160

bit_field_size = 10
bit_field = [0] * bit_field_size

for item in (b'hello world', b'goodbye'):
    h = hash160(item)
    bit = int.from_bytes(h, 'big') % bit_field_size
    bit_field[bit] = 1

print(bit_field)