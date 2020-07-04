"""
- The coinbase transaction has no previous output that it’s spending
- Must be 2-100 bytes long
- ScriptSig of the coinbase transaction is set by whoever mined the transaction
- Can by anything so long as evaluation of the ScriptSig evaluates to `1`

- Below is the ScriptSig of the coinbase transaction of the genesis block as set by Satoshi
"""

import bitcoin

from io import BytesIO
from bitcoin.script import Script

stream = BytesIO(bytes.fromhex('4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73'))
s = Script.parse(stream)

for cmd in s.cmds:
    print(cmd)

z = '<IRRELEVANT>' # Since no CHECKSIG
print(f"ScriptSig is valid: %s" % s.evaluate(z))

True
