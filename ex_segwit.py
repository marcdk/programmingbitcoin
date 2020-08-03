from io import BytesIO
from bitcoin.tx import Tx


def main():
    # Pay-to-Witness-Pubkey-Hash (p2wpkh) Transactions

    # Transaction malleability is fixed by emptying the ScriptSig field and putting the data in another field
    # that’s not used for ID calculation. For p2wpkh, the signature and pubkey are the items from ScriptSig,
    # so those get moved to the witness field, which is not used for ID calculation.

    raw_p2wpkh_tx_pre_bip0141 = bytes.fromhex(
        '01000000'  # version
        '01'  # number of inputs
        '15e180dc28a2327e687facc33f10f2a20da717e5548406f7ae8b4c811072f856'  # prev tx hash
        '01000000'  # prev tx index
        '00'  # ScriptSig is empty
        'ffffffff'  # sequence
        '01'  # number of outputs
        '00b4f50500000000'  # output amount
        '1976a914338c84849423992471bffb1a54a8d9b1d69dc28a88ac'  # ScriptPubKey: OP_0 <20-byte hash>
        '00000000'  # locktime
    )
    stream = BytesIO(raw_p2wpkh_tx_pre_bip0141)
    tx = Tx.parse(stream)
    print("p2wpkh_tx_pre_bip0141:", tx)

    # Segwit serialization
    raw_p2wpkh_tx_post_bip0141 = bytes.fromhex(
        '01000000'  # version
        '00'  # Segwit marker
        '01'  # Segwit flag
        '01'  # number of inputs
        '15e180dc28a2327e687facc33f10f2a20da717e5548406f7ae8b4c811072f856'  # prev tx hash
        '01000000'  # prev tx index
        '00'  # ScriptSig is empty
        'ffffffff'  # sequence
        '01'  # number of outputs
        '00b4f50500000000'  # output amount
        '1976a914338c84849423992471bffb1a54a8d9b1d69dc28a88ac'  # ScriptPubKey: OP_0 <20-byte hash>
        '02483045022100df7b7e5cda14ddf91290e02ea10786e03eb11ee36ec02dd862'  # witness
        'fe9a326bbcb7fd02203f5b4496b667e6e281cc654a2da9e4f08660c620a10513'
        '37fa8965f727eb19190121038262a6c6cec93c2d3ecd6c6072efea86d02ff8e3'
        '328bbd0242b20af3425990ac'
        '00000000'  # locktime
    )
    stream = BytesIO(raw_p2wpkh_tx_post_bip0141)
    tx = Tx.parse(stream)
    print("p2wpkh_tx_post_bip0141:", tx)

    # Pay-to-Script-Hash-Pay-to-Witness-Pubkey-Hash (p2sh-p2wpkh) Transactions

    # p2wpkh is great, but unfortunately, this is a new type of script and older wallets cannot send bitcoins to
    # p2wpkh ScriptPubKeys. p2wpkh uses a new address format called Bech32, defined in BIP0173,
    # whose ScriptPubKeys older wallets don’t know how to create.
    #
    # The Segwit authors found an ingenious way to make Segwit backward compatible by "wrapping" p2wpkh inside p2sh.
    # This is called "nested" Segwit as the Segwit script is nested in a p2sh RedeemScript.
    # The difference is that the ScriptSig is no longer empty and has a RedeemScript,
    # which is equal to the ScriptPubkey in p2wpkh
    raw_p2sh_p2wpkh_tx_pre_bip0141 = bytes.fromhex(
        '01000000'  # version
        '01'  # number of inputs
        '712e5b4e97ab549d50ca60a4f5968b2225215e9fab82dae4720078711406972f'  # prev tx hash
        '00000000'  # prev tx index
        '17160014848202fc47fb475289652fbd1912cc853ecb0096'  # ScriptSig is not empty
        'feffffff'  # sequence
        '02'  # number of outputs
        '3236000000000000'  # output amount
        '1976a914121ae7a2d55d2f0102ccc117cbcb70041b0e037f88ac'  # ScriptPubKey
        '1027000000000000'  # output amount
        '1976a914ec0be50951651261765cfa71d7bd41c7b9245bb388ac'  # ScriptPubKey
        '075a0700'  # locktime
    )
    stream = BytesIO(raw_p2sh_p2wpkh_tx_pre_bip0141)
    tx = Tx.parse(stream)
    print("p2sh_p2wpkh_tx_pre_bip0141:", tx)

    raw_p2sh_p2wpkh_tx_post_bip0141 = bytes.fromhex(
        '01000000'  # version
        '00'  # Segwit marker
        '01'  # Segwit flag
        '01'  # number of inputs
        '712e5b4e97ab549d50ca60a4f5968b2225215e9fab82dae4720078711406972f'  # prev tx hash
        '00000000'  # prev tx index
        '17160014848202fc47fb475289652fbd1912cc853ecb0096'  # ScriptSig is not empty
        'feffffff'  # sequence
        '02'  # number of outputs
        '3236000000000000'  # output amount
        '1976a914121ae7a2d55d2f0102ccc117cbcb70041b0e037f88ac'  # ScriptPubKey
        '1027000000000000'  # output amount
        '1976a914ec0be50951651261765cfa71d7bd41c7b9245bb388ac'  # ScriptPubKey
        '024830450221009263c7de80c297d5b21aba846cf6f0a970e1d3'  # witness
        '39568167d1e4c1355c7711bc1602202c9312b8d32fd9c7acc54c'
        '46cab50eb7255ce3c012214c41fe1ad91bccb16a13012102ebdf'
        '6fc448431a2bd6380f912a0fa6ca291ca3340e79b6f0c1fdaff7'
        '3cf54061'
        '075a0700'  # locktime
    )
    stream = BytesIO(raw_p2sh_p2wpkh_tx_post_bip0141)
    tx = Tx.parse(stream)
    print("p2sh_p2wpkh_tx_post_bip0141:", tx)

    # Pay-to-Witness-Script-Hash (p2wsh) Transactions

    # While p2wpkh takes care of a major use case, we need something more flexible
    # if we want more complicated (e.g., multisig) scripts.
    # This is where pay-to-witness-script-hash (p2wsh) comes in.
    # p2wsh is like p2sh, but with all the ScriptSig data in the witness field instead.

    raw_p2wsh_tx_pre_bip0141 = bytes.fromhex(
        '01000000'  # version
        '01'  # number of inputs
        '593a2db37b841b2a46f4e9bb63fe9c1012da3ab7fe30b9f9c974242778b5f898'  # prev tx hash
        '00000000'  # prev tx index
        '00'  # ScriptSig is empty
        'ffffffff'  # sequence
        '01'  # number of outputs
        '806fb30700000000'  # output amount
        '1976a914bbef244bcad13cffb68b5cef3017c7423675552288ac'  # ScriptPubKey:  OP_0 <32-byte hash>
        '00000000'  # locktime
    )
    stream = BytesIO(raw_p2wsh_tx_pre_bip0141)
    tx = Tx.parse(stream)
    print("p2wsh_tx_pre_bip0141:", tx)

    # Newer nodes will recognize the special sequence OP_0 <32-byte hash>
    # and do additional validation by looking at the witness field.

    # The WitnessScript is very similar to the RedeemScript in that the sha256 of the serialization
    # is addressed in the ScriptPubKey, but only revealed when the output is being spent.
    # Once the sha256 of the WitnessScript is found to be the same as the 32-byte hash,
    # the WitnessScript is interpreted as script commands and added to the command set.
    # The rest of the witness field is then added to the command set as well,
    # producing the final set of commands to be evaluated. p2wsh is particularly important, as unmalleable
    # multisig transactions are required for creating bidirectional payment channels for the Lightning Network.

    raw_p2wsh_tx_post_bip0141 = bytes.fromhex(
        '01000000'  # version
        '00'  # Segwit marker
        '01'  # Segwit flag
        '01'  # number of inputs
        '593a2db37b841b2a46f4e9bb63fe9c1012da3ab7fe30b9f9c974242778b5f898'  # prev tx hash
        '00000000'  # prev tx index
        '00'  # ScriptSig is empty
        'ffffffff'  # sequence
        '01'  # number of outputs
        '806fb30700000000'  # output amount
        '1976a914bbef244bcad13cffb68b5cef3017c7423675552288ac'  # ScriptPubKey:  OP_0 <32-byte hash>
        # witness start...
        '04'  # number of witness elements
        '00'  # OP_0
        '47'  # length of signature
        '304402203cdcaf02a44e37e409646e8a506724e9e1394b890cb5'  # signature
        '2429ea65bac4cc2403f1022024b934297bcd0c21f22cee0e4875'
        '1c8b184cc3a0d704cae2684e14858550af7d01'
        '69'  # length of witness script
        # witness script start...
        '52'  # OP_2
        '21'  # length of pubkey
        '026ccfb8061f235cc110697c0bfb3afb99d82c886672f6b9b5393b25a434c0cbf3'  # pubkey 
        '21'  # length of pubkey
        '03befa190c0c22e2f53720b1be9476dcf11917da4665c44c9c71c3a2d28a933c35'  # pubkey 
        '21'  # length of pubkey
        '02be46dc245f58085743b1cc37c82f0d63a960efa43b5336534275fc469b49f4ac'  # pubkey 
        '53'  # OP_3
        'ae'  # OP_CHECKMULTISIG 
        # ...witness script end
        # ...witness end
        '00000000'  # locktime
    )
    stream = BytesIO(raw_p2wsh_tx_post_bip0141)
    tx = Tx.parse(stream)
    print("p2wsh_tx_post_bip0141:", tx)

    # Pay-to-Script-Hash-Pay-to-Witness-Script-Hash (p2sh-p2wsh) Transactions

    # p2sh-p2wsh is a way to make p2wsh backward compatible.
    # As with p2sh-p2wpkh, the ScriptPubKey is indistinguishable from any other p2sh address
    # and the ScriptSig is only the RedeemScript
    # The RedeemScript is OP_0 32-byte hash, which is the same as the ScriptPubKey for p2wsh

    # raw_p2sh_p2wsh_tx_pre_bip0141 = bytes.fromhex(
    #     '01000000'  # version
    #     '01'  # number of inputs
    #     '593a2db37b841b2a46f4e9bb63fe9c1012da3ab7fe30b9f9c974242778b5f898'  # prev tx hash
    #     '00000000'  # prev tx index
    #     '00'  # ScriptSig is empty
    #     'ffffffff'  # sequence
    #     '01'  # number of outputs
    #     '806fb30700000000'  # output amount
    #     '1976a914bbef244bcad13cffb68b5cef3017c7423675552288ac'  # ScriptPubKey:  OP_0 <32-byte hash>
    #     '00000000'  # locktime
    # )
    raw_p2sh_p2wsh_tx_pre_bip0141 = bytes.fromhex(
        '01000000'  # version
        '01'  # number of inputs
        '708256c5896fb3f00ef37601f8e30c5b460dbcd1fca1cd7199f9b56fc4ecd540'  # prev tx hash
        '00000000'  # prev tx index
        '23220020615ae01ed1bc1ffaad54da31d7805d0bb55b52dfd3941114330368c1bbf69b4c'  # ScriptSig
        'ffffffff'  # sequence
        '01'  # number of outputs
        '603edb0300000000'  # output amount
        '160014bbef244bcad13cffb68b5cef3017c74236755522'  # ScriptPubKey
        '00000000'  # locktime
    )
    stream = BytesIO(raw_p2sh_p2wsh_tx_pre_bip0141)
    tx = Tx.parse(stream)
    print("p2sh_p2wsh_tx_pre_bip0141:", tx)

    # Post-Segwit nodes will recognize the special script sequence OP_0 <32-byte hash> for p2wsh
    # This makes p2wsh backward compatible, allowing older wallets to send to p2sh ScriptPubKeys that they can handle.

    raw_p2sh_p2wsh_tx_post_bip0141 = bytes.fromhex(
        '01000000'  # version
        '00'  # Segwit marker
        '01'  # Segwit flag
        '01'  # number of inputs
        '708256c5896fb3f00ef37601f8e30c5b460dbcd1fca1cd7199f9b56fc4ecd540'  # prev tx hash
        '00000000'  # prev tx index
        '23220020615ae01ed1bc1ffaad54da31d7805d0bb55b52dfd3941114330368c1bbf69b4c'  # ScriptSig
        'ffffffff'  # sequence
        '01'  # number of outputs
        '603edb0300000000'  # output amount
        '160014bbef244bcad13cffb68b5cef3017c74236755522'  # ScriptPubKey
        # witness start...
        '04'  # number of witness elements
        '00'  # OP_0
        '47'  # length of signature
        '30440220010d2854b86b90b7c33661ca25f9d9f15c24b88c5c4992630f77ff004'  # signature
        'b998fb802204106fc3ec8481fa98e07b7e78809ac91b6ccaf60bf4d3f729c5a75'
        '899bb664a501473044022046d66321c6766abcb1366a793f9bfd0e11e0b080354'
        'f18188588961ea76c5ad002207262381a0661d66f5c39825202524c45f29d500c'
        '6476176cd910b1691176858701'
        '69'  # length of witness script
        # witness script start...
        '52'  # OP_2
        '21'  # length of pubkey
        '026ccfb8061f235cc110697c0bfb3afb99d82c886672f6b9b5393b25a434c0cbf3'  # pubkey
        '21'  # length of pubkey
        '03befa190c0c22e2f53720b1be9476dcf11917da4665c44c9c71c3a2d28a933c35'  # pubkey
        '21'  # length of pubkey
        '02be46dc245f58085743b1cc37c82f0d63a960efa43b5336534275fc469b49f4ac'  # pubkey
        '53'  # OP_3
        'ae'  # OP_CHECKMULTISIG
        # ...witness script end
        # ...witness end
        '00000000'  # locktime
    )
    stream = BytesIO(raw_p2sh_p2wsh_tx_post_bip0141)
    tx = Tx.parse(stream)
    print("p2sh_p2wsh_tx_post_bip0141:", tx)


if __name__ == '__main__':
    main()
