import time

from bitcoin.bloomfilter import BloomFilter
from bitcoin.ecc import PrivateKey
from bitcoin.helper import (
     decode_base58,
     hash256,
     little_endian_to_int,
 )
from bitcoin.merkleblock import MerkleBlock
from bitcoin.network import (
     GetDataMessage,
     GetHeadersMessage,
     HeadersMessage,
     SimpleNode,
     TX_DATA_TYPE,
     FILTERED_BLOCK_DATA_TYPE,
 )
from bitcoin.script import p2pkh_script
from bitcoin.tx import Tx, TxIn, TxOut

last_block_hex = '00000000000000a03f9432ac63813c6710bfe41712ac5ef6faab093fe2917636'
secret = little_endian_to_int(hash256(b'Jimmy Song'))
private_key = PrivateKey(secret=secret)
addr = private_key.point.address(testnet=True)
h160 = decode_base58(addr)
target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
target_h160 = decode_base58(target_address)
target_script = p2pkh_script(target_h160)
fee = 5000  # fee in satoshis
# connect to testnet.programmingbitcoin.com in testnet mode
node = SimpleNode('testnet.programmingbitcoin.com', testnet=True, logging=False)
# Create a Bloom Filter of size 30 and 5 functions. Add a tweak.
bf = BloomFilter(30, 5, 90210)
# add the h160 to the Bloom Filter
bf.add(h160)
# complete the handshake
node.handshake()
# load the Bloom Filter with the filterload command
node.send(bf.filterload())
# set start block to last_block from above
start_block = bytes.fromhex(last_block_hex)
# send a getheaders message with the starting block
getheaders = GetHeadersMessage(start_block=start_block)
node.send(getheaders)
# wait for the headers message
headers = node.wait_for(HeadersMessage)
# store the last block as None
last_block = None
# initialize the GetDataMessage
getdata = GetDataMessage()
# loop through the blocks in the headers
for b in headers.blocks:
     # check that the proof of work on the block is valid
     if not b.check_pow():
         raise RuntimeError('proof of work is invalid')
     # check that this block's prev_block is the last block
     if last_block is not None and b.prev_block != last_block:
         raise RuntimeError('chain broken')
     # add a new item to the getdata message
     # should be FILTERED_BLOCK_DATA_TYPE and block hash
     getdata.add_data(FILTERED_BLOCK_DATA_TYPE, b.hash())
     # set the last block to the current hash
     last_block = b.hash()
# send the getdata message
node.send(getdata)
# initialize prev_tx, prev_index, and prev_amount to None
prev_tx, prev_index, prev_amount = None, None, None
# loop while prev_tx is None
while prev_tx is None:
     # wait for the merkleblock or tx commands
     message = node.wait_for(MerkleBlock, Tx)
     # if we have the merkleblock command
     if message.command == b'merkleblock':
         # check that the MerkleBlock is valid
         if not message.is_valid():
             raise RuntimeError('invalid merkle proof')
     # else we have the tx command
     else:
         # set the tx's testnet to be True
         message.testnet = True
         # loop through the tx outs
         for i, tx_out in enumerate(message.tx_outs):
             # if our output has the same address as our address we found it
             if tx_out.script_pubkey.address(testnet=True) == addr:
                 # we found our utxo; set prev_tx, prev_index, and tx
                 prev_tx = message.hash()
                 prev_index = i
                 prev_amount = tx_out.amount
                 print('found: {}:{}'.format(prev_tx.hex(), prev_index))
#found: b2cddd41d18d00910f88c31aa58c6816a190b8fc30fe7c665e1cd2ec60efdf3f:7
# create the TxIn
tx_in = TxIn(prev_tx, prev_index)
# calculate the output amount (previous amount minus the fee)
output_amount = prev_amount - fee
# create a new TxOut to the target script with the output amount
tx_out = TxOut(output_amount, target_script)
# create a new transaction with the one input and one output
tx_obj = Tx(1, [tx_in], [tx_out], 0, testnet=True)
# sign the only input of the transaction
print(tx_obj.sign_input(0, private_key))
True
# serialize and hex to see what it looks like
print(tx_obj.serialize().hex())
#01000000013fdfef60ecd21c5e667cfe30fcb890a116688ca51ac3880f91008dd141ddcdb20700\
#00006b483045022100ff77d2559261df5490ed00d231099c4b8ea867e6ccfe8e3e6d077313ed4f\
#31428022033a1db8d69eb0dc376f89684d1ed1be75719888090388a16f1e8eedeb8067768012103\
#dc585d46cfca73f3a75ba1ef0c5756a21c1924587480700c6eb64e3f75d22083ffffffff019334\
#e500000000001976a914ad346f8eb57dee9a37981716e498120ae80e44f788ac00000000
# send this signed transaction on the network
node.send(tx_obj)
# wait a sec so this message goes through with time.sleep(1)
time.sleep(1)
# now ask for this transaction from the other node
# create a GetDataMessage
getdata = GetDataMessage()
# ask for our transaction by adding it to the message
getdata.add_data(TX_DATA_TYPE, tx_obj.hash())
# send the message
node.send(getdata)
# now wait for a Tx response
received_tx = node.wait_for(Tx)
# if the received tx has the same id as our tx, we are done!
if received_tx.id() == tx_obj.id():
     print('success!')