import bitcoin

from bitcoin.ecc import PrivateKey
from bitcoin.tx import Tx, TxIn, TxOut
from bitcoin.helper import hash256, little_endian_to_int, decode_base58
from bitcoin.script import p2pkh_script

# Mission: Send BTC
# We'll rather use tBTC :P

# Generate two (private) keys & addresses
secret = little_endian_to_int(hash256(b'Some kind of seed like BIP32'))
private_key = PrivateKey(secret)

secret2 = little_endian_to_int(hash256(b'I am the receiver of tBTC'))
private_key2 = PrivateKey(secret2)

print("Marc-controlled address receiving tBTC from faucet")
print(private_key.point.address(testnet=True))

print("Marc-controlled address of new home for tBTC")
print(private_key2.point.address(testnet=True))

prev_tx = bytes.fromhex('75a1c4bc671f55f626dda1074c7725991e6f68b8fcefcfca7b64405ca3b45f1c')
prev_index = 1

target_address = 'miKegze5FQNCnGw6PKyqUbYUeBa4x2hFeM'
target_amount = 0.01

change_address = 'mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2'
change_amount = 0.009

priv = PrivateKey(secret=secret)

tx_ins = []
tx_ins.append(TxIn(prev_tx, prev_index))

tx_outs = []
h160 = decode_base58(target_address)
script_pubkey = p2pkh_script(h160)
target_satoshis = int(target_amount*100000000)
tx_outs.append(TxOut(target_satoshis, script_pubkey))

h160 = decode_base58(change_address)
script_pubkey = p2pkh_script(h160)
change_satoshis = int(change_amount*100000000)
tx_outs.append(TxOut(change_satoshis, script_pubkey))

tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)

print(tx_obj.sign_input(0, priv))
print(tx_obj.serialize().hex())
