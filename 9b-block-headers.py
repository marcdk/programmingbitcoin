"""
- Below is the ScriptSig of the coinbase transaction of the genesis block as set by Satoshi
"""

import bitcoin

from bitcoin.helper import hash256

block_hash = hash256(bytes.fromhex('020000208ec39428b17323fa0ddec8e887b4a7\
c53b8c0a0a220cfd0000000000000000005b0750fce0a889502d40508d39576821155e9c9e3f5c\
3157f961db38fd8b25be1e77a759e93c0118a4ffd71d'))[::-1]
block_id = block_hash.hex()
print(block_id)

# 0000000000000000007e9e4c586439b0cdbe13b1370bdd9435d76a644d047523
