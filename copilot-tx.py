import bitcoin

from bitcoin.ecc import PrivateKey
from bitcoin.tx import Tx, TxIn, TxOut
from bitcoin.helper import hash256, little_endian_to_int, decode_base58
from bitcoin.script import p2pkh_script

# Task: Send BTC
# We'll rather use tBTC :P

# Generate two (private) keys & addresses
secret = little_endian_to_int(hash256(b'Some kind of seed like BIP32'))
private_key = PrivateKey(secret)

print("Marc-controlled address receiving tBTC from faucet")
print(private_key.point.address(testnet=True))

print('')

# Get some tBTC from the faucet!

# Send those tBTC to another Marc-controlled address (lockbox)
# raw_tx = bytes.fromhex('020000000001010af082cadada4587318cfa13b0f55fc947884cb7689caaafc697d927dc3be16601000000171600142f8e9a6ce133cc47d2a0e9c61ba1417c2decb5a6feffffff0210270000000000001976a9145eebe4425d6c1589e1687b1005a3175b3d67b96f88ac9515bd340000000017a9140f66dc88285738e182273fe19ebbe83402d643498702473044022008d9841de73cf5bafc62fc80577efd99506a8dfb59fc46b1089c129e420f43a202203d213472d0e4ad685a3b14fbd3780a4c64869a31bc0befea5a85c4549567831201210207584719e15c0729ceb4f028184d27dfdca8169041de416e6a6c85a6f815efe0c60c1b00')
# stream = BytesIO(raw_tx)
# zx = tx.Tx.parse(stream, testnet=True)

# Tx from tBTC faucet, kindly sponsored by https://testnet-faucet.mempool.co
tx_ins = []

prev_tx = bytes.fromhex('4e7f585ff16f6364e521feea2eab29a803274077192c5ed26eea1e566035281a')
prev_index = 7
tx_ins.append(TxIn(prev_tx, prev_index))

input_amount = tx_ins[0].value(testnet=True)

target_amount = input_amount - 1000
target_h160 = decode_base58('mm7gA5bREc1yN4U6huxcqAnYqn11UynZLh')
target_script = p2pkh_script(target_h160)

tx_outs = []
tx_outs.append(TxOut(amount=target_amount, script_pubkey=target_script))

new_tx = Tx(1, tx_ins, tx_outs, 0, True)
new_tx.sign_input(0, private_key)

print(new_tx)
print('')
print(new_tx.serialize().hex())
print()

True
