from io import BytesIO
from bitcoin.block import Block, GENESIS_BLOCK
from bitcoin.network import SimpleNode, GetHeadersMessage

from io import BytesIO
from bitcoin.network import SimpleNode, GetHeadersMessage, HeadersMessage
from bitcoin.block import Block, GENESIS_BLOCK, LOWEST_BITS
from bitcoin.helper import calculate_new_bits

previous = Block.parse(BytesIO(GENESIS_BLOCK))
first_epoch_timestamp = previous.timestamp
expected_bits = LOWEST_BITS
count = 1
node = SimpleNode('mainnet.programmingbitcoin.com', testnet=False)
node.handshake()
for _ in range(19):
    getheaders = GetHeadersMessage(start_block=previous.hash())
    node.send(getheaders)
    headers = node.wait_for(HeadersMessage)
    for header in headers.blocks:
        if not header.check_pow():
            raise RuntimeError('bad PoW at block {}'.format(count))

        if header.prev_block != previous.hash():
            raise RuntimeError('discontinuous block at {}'.format(count))

        if count % 2016 == 0:
            time_diff = previous.timestamp - first_epoch_timestamp expected_bits = calculate_new_bits(previous.bits, time_diff) print(expected_bits.hex())
            first_epoch_timestamp = header.timestamp
        if header.bits != expected_bits:
        raise RuntimeError('bad bits at block {}'.format(count))
            previous = header
            count += 1