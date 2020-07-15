import bitcoin

from bitcoin.network import *

envelope_bytes = bytes.fromhex("f9beb4d976657261636b000000000000000000005df6e0e2")
stream = BytesIO(envelope_bytes)

envelope = NetworkEnvelope.parse(stream)
print(envelope.command)
