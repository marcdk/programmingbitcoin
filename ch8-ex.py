from bitcoin import ecc
from bitcoin import tx
from bitcoin import helper
from bitcoin import script
from io import BytesIO

############
# Exercise 4
############

# modify the transaction
# start with version
# add number of inputs
# modify the single TxIn to have the ScriptSig to be the RedeemScript
# add the number of outputs
# add each output serialization
# add the locktime
# add the SIGHASH_ALL
# hash256 the result
# interpret as a Big-Endian number
# parse the S256Point
# parse the Signature
# verify that the point, z and signature work"

hex_tx = '0100000001868278ed6ddfb6c1ed3ad5f8181eb0c7a385aa0836f01d5e4789e6bd304d87221a000000db00483045022100dc92655fe37036f47756db8102e0d7d5e28b3beb83a8fef4f5dc0559bddfb94e02205a36d4e4e6c7fcd16658c50783e00c341609977aed3ad00937bf4ee942a8993701483045022100da6bee3c93766232079a01639d07fa869598749729ae323eab8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e75402201475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152aeffffffff04d3b11400000000001976a914904a49878c0adfc3aa05de7afad2cc15f483a56a88ac7f400900000000001976a914418327e3f3dda4cf5b9089325a4b95abdfa0334088ac722c0c00000000001976a914ba35042cfe9fc66fd35ac2224eebdafd1028ad2788acdc4ace020000000017a91474d691da1574e6b3c192ecfb52cc8984ee7b6c568700000000'
hex_sec = '03b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb71'
hex_der = '3045022100da6bee3c93766232079a01639d07fa869598749729ae323eab8eef53577d611b02207bef15429dcadce2121ea07f233115c6f09034c0be68db99980b9a6c5e754022'
hex_redeem_script = '475221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152ae'
sec = bytes.fromhex(hex_sec)
der = bytes.fromhex(hex_der)
redeem_script = script.Script.parse(BytesIO(bytes.fromhex(hex_redeem_script)))
stream = BytesIO(bytes.fromhex(hex_tx))

tx_obj = tx.Tx.parse(stream)

# 1. Version
s = helper.int_to_little_endian(tx_obj.version, 4)

# 2. Inputs
s += helper.encode_varint(len(tx_obj.tx_ins))
tx_in0 = tx_obj.tx_ins[0]
# 2.1 Previous transaction ID
# 2.2 Previous transaction index
# 2.3 ScriptSig
# 2.4 Sequence
s += tx.TxIn(tx_in0.prev_tx, tx_in0.prev_index, redeem_script, tx_in0.sequence).serialize()

# 3. Outputs
s += helper.encode_varint(len(tx_obj.tx_outs))
for tx_out in tx_obj.tx_outs:
    s += tx_out.serialize()

# 4. Locktime
s += helper.int_to_little_endian(tx_obj.locktime, 4)
s += helper.int_to_little_endian(tx.SIGHASH_ALL, 4)

z = int.from_bytes(helper.hash256(s), 'big')
point = ecc.S256Point.parse(sec)
sig = ecc.Signature.parse(der)
print(point.verify(z, sig))

############
# Exercise 5
############


