# This sample is provided for demonstration purposes only.
# It is not intended for production use.
# This example does not constitute trading advice.

from hybridswap.v1.client import HybridswapTestnetClient


# Hardcoding account keys is not a great practice. This is for demonstration purposes only.
# See the README & Docs for alternative signing methods.
account = {
    'address': 'ALGORAND_ADDRESS_HERE',
    'private_key': 'base64_private_key_here', # Use algosdk.mnemonic.to_private_key(mnemonic) if necessary
}

client = HybridswapTestnetClient(user_address=account['address'])
# By default all subsequent operations are on behalf of user_address

# Fetch our two assets of interest
BYBRIDUSDC = client.fetch_asset(21582668)
ALGO = client.fetch_asset(0)

# Fetch the pool we will work with
pool = client.fetch_pool(BYBRIDUSDC, ALGO)

info = pool.fetch_pool_position()
share = info['share'] * 100
print(f'Pool Tokens: {info[pool.liquidity_asset]}')
print(f'Assets: {info[BYBRIDUSDC]}, {info[ALGO]}')
print(f'Share of pool: {share:.3f}%')
