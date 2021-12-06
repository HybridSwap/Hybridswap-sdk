# This sample is provided for demonstration purposes only.
# It is not intended for production use.
# This example does not constitute trading advice.


# This example has exactly the same functionality as swapping1.py but is purposely more verbose, using less convenience functions.
# It is intended to give an understanding of what happens under those convenience functions.

from hybridswap.v1.pools import Pool
from hybridswap.assets import Asset
from hybridswap.utils import wait_for_confirmation
from algosdk.v2client.algod import AlgodClient
from hybridswap.v1.client import HybridswapClient


# Hardcoding account keys is not a great practice. This is for demonstration purposes only.
# See the README & Docs for alternative signing methods.
account = {
    'address': 'ALGORAND_ADDRESS_HERE',
    'private_key': 'base64_private_key_here', # Use algosdk.mnemonic.to_private_key(mnemonic) if necessary
}


algod = AlgodClient('', 'https://api.testnet.algoexplorer.io', headers={'User-Agent': 'algosdk'})

client = HybridswapClient(
    algod_client=algod,
    validator_app_id=21580889,
)


# Check if the account is opted into Hybridswap and optin if necessary
if(not client.is_opted_in(account['address'])):
    print('Account not opted into app, opting in now..')
    transaction_group = client.prepare_app_optin_transactions(account['address'])
    for i, txn in enumerate(transaction_group.transactions):
        if txn.sender == account['address']:
            transaction_group.signed_transactions[i] = txn.sign(account['private_key'])
    txid = client.algod.send_transactions(transaction_group.signed_transactions)
    wait_for_confirmation(txid)


# Fetch our two assets of interest
HYBRIDUSDC = Asset(id=21582668, name='HybridUSDC', unit_name='HYBRIDUSDC', decimals=6)
ALGO = Asset(id=0, name='Algo', unit_name='ALGO', decimals=6)

# Create the pool we will work with and fetch its on-chain state
pool = Pool(client, asset_a=HYBRIDUSDC, asset_b=ALGO, fetch=True)


# Get a quote for a swap of 1 ALGO to HYBRIDUSDC with 1% slippage tolerance
quote = pool.fetch_fixed_input_swap_quote(ALGO(1_000_000), slippage=0.01)
print(quote)
print(f'HYBRIDUSDC per ALGO: {quote.price}')
print(f'HYBRIDUSDC per ALGO (worst case): {quote.price_with_slippage}')

# We only want to sell if ALGO is > 180 HYBRIDUSDC (It's testnet!)
if quote.price_with_slippage > 180:
    print(f'Swapping {quote.amount_in} to {quote.amount_out_with_slippage}')
    # Prepare a transaction group
    transaction_group = pool.prepare_swap_transactions(
        amount_in=quote.amount_in,
        amount_out=quote.amount_out_with_slippage,
        swap_type='fixed-input',
        swapper_address=account['address'],
    )
    # Sign the group with our key
    for i, txn in enumerate(transaction_group.transactions):
        if txn.sender == account['address']:
            transaction_group.signed_transactions[i] = txn.sign(account['private_key'])
    txid = algod.send_transactions(transaction_group.signed_transactions)
    wait_for_confirmation(algod, txid)

    # Check if any excess remaining after the swap
    excess = pool.fetch_excess_amounts(account['address'])
    if HYBRIDUSDC.id in excess:
        amount = excess[HYBRIDUSDC.id]
        print(f'Excess: {amount}')
        # We might just let the excess accumulate rather than redeeming if its < 1 HybridUSDC
        if amount > 1_000_000:
            transaction_group = pool.prepare_redeem_transactions(amount, account['address'])
            # Sign the group with our key
            for i, txn in enumerate(transaction_group.transactions):
                if txn.sender == account['address']:
                    transaction_group.signed_transactions[i] = txn.sign(account['private_key'])
            txid = algod.send_transactions(transaction_group.signed_transactions)
            wait_for_confirmation(algod, txid)