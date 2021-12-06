# This sample is provided for demonstration purposes only.
# It is not intended for production use.
# This example does not constitute trading advice.

# For a more verbose version of this example see swapping1_less_convenience.py

from hybridswap.v1.client import HybridswapTestnetClient


# Hardcoding account keys is not a great practice. This is for demonstration purposes only.
# See the README & Docs for alternative signing methods.
account = {
    'address': 'ALGORAND_ADDRESS_HERE',
    'private_key': 'base64_private_key_here', # Use algosdk.mnemonic.to_private_key(mnemonic) if necessary
}

client = HybridswapTestnetClient(user_address=account['address'])
# By default all subsequent operations are on behalf of user_address

# Check if the account is opted into Hybridswap and optin if necessary
if(not client.is_opted_in()):
    print('Account not opted into app, opting in now..')
    transaction_group = client.prepare_app_optin_transactions()
    transaction_group.sign_with_private_key(account['address'], account['private_key'])
    result = client.submit(transaction_group, wait=True)


# Fetch our two assets of interest
HYBRIDUSDC = client.fetch_asset(21582668)
ALGO = client.fetch_asset(0)

# Fetch the pool we will work with
pool = client.fetch_pool(HYBRIDUSDC, ALGO)


# Get a quote for a swap of 1 ALGO to HYBRIDUSDC with 1% slippage tolerance
quote = pool.fetch_fixed_input_swap_quote(ALGO(1_000_000), slippage=0.01)
print(quote)
print(f'HYBRIDUSDC per ALGO: {quote.price}')
print(f'HYBRIDUSDC per ALGO (worst case): {quote.price_with_slippage}')

# We only want to sell if ALGO is > 180 HYBRIDUSDC (It's testnet!)
if quote.price_with_slippage > 180:
    print(f'Swapping {quote.amount_in} to {quote.amount_out_with_slippage}')
    # Prepare a transaction group
    transaction_group = pool.prepare_swap_transactions_from_quote(quote)
    # Sign the group with our key
    transaction_group.sign_with_private_key(account['address'], account['private_key'])
    # Submit transactions to the network and wait for confirmation
    result = client.submit(transaction_group, wait=True)

    # Check if any excess remaining after the swap
    excess = pool.fetch_excess_amounts()
    if HYBRIDUSDC in excess:
        amount = excess[HYBRIDUSDC]
        print(f'Excess: {amount}')
        # We might just let the excess accumulate rather than redeeming if its < 1 HybridUSDC
        if amount > 1_000_000:
            transaction_group = pool.prepare_redeem_transactions(amount)
            transaction_group.sign_with_private_key(account['address'], account['private_key'])
            result = client.submit(transaction_group, wait=True)
