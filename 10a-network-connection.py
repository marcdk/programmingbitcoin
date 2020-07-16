import socket
from bitcoin.network import NetworkEnvelope, VersionMessage

host = 'testnet.programmingbitcoin.com'
port = 18333
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))
stream = socket.makefile('rb', None)
version = VersionMessage()
envelope = NetworkEnvelope(version.command, version.serialize(), testnet=True)
socket.sendall(envelope.serialize())
while True:
    new_message = NetworkEnvelope.parse(stream, testnet=True)
    print(new_message)
