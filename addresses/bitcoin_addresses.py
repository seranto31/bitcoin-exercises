#!/usr/bin/env python
import base58
import ecdsa
import hashlib
import random

# Enter a random private key from https://bitcore.io/playground/#/address
private_key = 'e1e78ca3ebbce24977ddd8161905e7ee6821c0a100a6c1a58ac2e0cf79f98635'
pk = private_key.decode('hex')

# Generate a 512-bit public key from the private key (pk) using ECDSA
sk = ecdsa.SigningKey.from_string(pk, curve=ecdsa.SECP256k1)

# Get the verifying_key
xy = sk.verifying_key.to_string().encode('hex')

# Uncompressed public key (http://gobittest.appspot.com/Address)
# public_key = '04'.decode('hex') + xy.decode('hex')

# Compressed public key
if ((int(xy[64::],16)%2) == 1):
    public_key = '03'.decode('hex') + xy[0:64].decode('hex')
else:
    public_key = '02'.decode('hex') + xy[0:64].decode('hex')

sha256_hash = hashlib.sha256(public_key).digest()

ripemd160 = hashlib.new('ripemd160')
ripemd160.update(sha256_hash)
hash160 = ripemd160.digest() # Hash160

prefix = '\00' # P2PKH
prefixed_hash = prefix + hash160

# Calculate Checksum
hashed_hash = hashlib.sha256(prefixed_hash).digest()
hashed_hash = hashlib.sha256(hashed_hash).digest()
checksum = hashed_hash.encode('hex')[0:8].decode('hex')

# Append checksum
payload = prefixed_hash + checksum

print payload.encode('hex')
address = base58.b58encode(payload)
print address
