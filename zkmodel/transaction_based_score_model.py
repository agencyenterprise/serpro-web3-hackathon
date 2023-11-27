import json
import pandas as pd
from datetime import timedelta
import math
import numpy as np
from web3 import Web3

# Replace with your Alchemy API key
alchemy_api_key = "YOUR_ALCHEMY_API_KEY"

w3 = Web3(Web3.HTTPProvider(f"https://eth-mainnet.alchemyapi.io/v2/{alchemy_api_key}"))

user_address = "0xUserAddress"  # Replace with the user's Ethereum address
nft_contract_address = (
    "0xNFTContractAddress"  # Replace with the NFT contract address you want to check
)

# Sample data: replace with real transaction data
data = {
    "timestamp": pd.date_range(start="2021-01-01", periods=10, freq="30T"),
    "is_sender": [True, False, True, False, True, False, True, False, True, False],
    "other_address_score": [
        200,
        500,
        300,
        600,
        800,
        100,
        400,
        700,
        900,
        200,
    ],  # Other party's score
}
transactions_df = pd.DataFrame(data)
transactions_df["timestamp"] = pd.to_datetime(transactions_df["timestamp"])


def payment_tx_type(transaction):
    # Determines if the user is sender or receiver
    return "sender" if transaction["is_sender"] else "receiver"


def calculate_num_transactions(transactions, current_index, window=timedelta(hours=1)):
    # Counts transactions within a specified time window
    current_time = transactions.iloc[current_index]["timestamp"]
    return transactions[
        (transactions["timestamp"] >= current_time - window)
        & (transactions["timestamp"] < current_time)
    ].shape[0]


def calculate_influence_factor(S_current, S_other, k=0.1, A=100):
    # Influence factor formula
    return A * (1 - math.exp(-k * abs(S_current - S_other)))


def frequency_modifier(num_transactions, B=50, C=0.5):
    """Calculate the frequency modifier based on the number of transactions"""
    return B / (1 + np.exp(-C * (num_transactions - 1)))


def transaction_score(
    S_current, tx_type, S_other, num_transactions, freq_modifier=0.05
):
    # Transaction scoring formula
    IF = calculate_influence_factor(S_current, S_other)
    FM = frequency_modifier(num_transactions)
    if tx_type == "sender" and S_current < S_other:
        return min(IF * (1 + num_transactions * freq_modifier), 150)
    elif tx_type == "receiver" and S_current > S_other:
        return max(-IF * FM * num_transactions, -150)
    return 0


def compute_transaction_based_score(transactions_df, user_score=400):
    score = 0
    for index, transaction in transactions_df.iterrows():
        tx_type = payment_tx_type(transaction)
        num_transactions = calculate_num_transactions(transactions_df, index)
        other_address_score = transaction["other_address_score"]
        score_change = transaction_score(
            user_score, tx_type, other_address_score, num_transactions
        )
        score += score_change
    return max(min(score, 150), -150)


def calculate_ethereum_balance_score(eth_balance, max_eth_balance=1000000):
    return min(eth_balance / max_eth_balance, 1) * 300


def calculate_ethereum_nfts_score(nfts_held, max_nfts=20):
    return min(nfts_held / max_nfts, 1) * 300


def calculate_ethereum_activity_score(account_age, max_years=10):
    return min(account_age / max_years, 1) * 150


def calculate_erc20_tokens_score(erc20_tokens, max_erc20_tokens=10000):
    return min(erc20_tokens / max_erc20_tokens, 1) * 100


def compute_holdings_based_score(
    eth_balance,
    nfts_held,
    account_age,
    erc20_tokens,
):
    eth_balance_score = calculate_ethereum_balance_score(eth_balance)
    print(f"ETH Balance Score = {eth_balance_score}")
    nfts_score = calculate_ethereum_nfts_score(nfts_held)
    print(f"NFTs Score = {nfts_score}")
    activity_score = calculate_ethereum_activity_score(account_age)
    print(f"Activity Score = {activity_score}")
    erc20_score = calculate_erc20_tokens_score(erc20_tokens)
    print(f"ERC20 Score = {erc20_score}")
    return eth_balance_score + nfts_score + activity_score + erc20_score


def compute_overall_score(
    eth_balance,
    nfts_held,
    account_age,
    erc20_tokens,
    transactions_df,
    holdings_score=0,
):
    holdings_score = compute_holdings_based_score(
        eth_balance,
        nfts_held,
        account_age,
        erc20_tokens,
    )
    # Assuming transaction_score function calculates score up to 150
    transaction_score = compute_transaction_based_score(transactions_df, holdings_score)
    print(f"Transaction Score = {transaction_score}")
    final_score = holdings_score + transaction_score
    return final_score


def count_nfts():
    try:
        # Load the ABI of the NFT contract
        with open("NFTContractABI.json", "r") as abi_file:
            nft_contract_abi = json.load(abi_file)

        # Create a contract instance
        nft_contract = w3.eth.contract(
            address=nft_contract_address, abi=nft_contract_abi
        )

        # Call the balanceOf function to count NFTs owned by the user
        nft_count = nft_contract.functions.balanceOf(user_address).call()

        print(f"Number of NFTs owned by {user_address}: {nft_count}")
    except Exception as e:
        print(f"Error counting NFTs: {e}")


def wei_to_eth(wei):
    return wei / 1e18


def getTransactions(start, end, address):
    columns = [
        "from",
        "to",
        "value",
        "timestamp",
        "is_sender",
        "other_address",
        "block_number",
        "user_balance",
    ]
    transactions = pd.DataFrame([], columns=columns)
    for x in range(start, end):
        block = w3.eth.get_block(x, full_transactions=True)
        for transaction in block.transactions:
            if transaction["to"] == address or transaction["from"] == address:
                other_address = (
                    transaction["to"]
                    if transaction["from"] == address
                    else transaction["from"]
                )
                new_df = pd.DataFrame(
                    [
                        {
                            **transaction,
                            "timestamp": block.timestamp,
                            "is_sender": transaction["from"] == address,
                            "other_address": other_address,
                            "block_number": x,
                            "user_balance": w3.from_wei(
                                w3.eth.get_balance(address, block_identifier=x)
                            ),
                            "other_address_balance": w3.from_wei(
                                w3.eth.get_balance(
                                    other_address,
                                    block_identifier=x,
                                )
                            ),
                        }
                    ],
                    columns=columns,
                )
                transactions = pd.concat(
                    [
                        transactions,
                        new_df,
                    ]
                )
    return transactions


def get_score_in_db(address):
    return None


def extract_payment_data(block_start, block_end, user_address):
    try:
        # Fetch transactions sent to the user's address
        transactions = getTransactions(block_start, block_end, user_address)
        other_address_scores = []
        for _, row in transactions.iterrows():
            block_end = row["block_number"]
            other_address = row["other_address"]
            if other_address_score := get_score_in_db(other_address):
                other_transactions = getTransactions(
                    block_start, block_end, other_address
                )
            else:
                other_address_score = row["other_address_balance"]
            other_address_scores.append(other_address_score)
        transactions["other_address_score"] = other_address_scores
        return transactions
    except Exception as e:
        print(f"Error fetching transactions: {e}")


final_score = compute_overall_score(
    1e6,
    20,
    10,
    10000,
    transactions_df,
    holdings_score=400,
)
print(f"Final Score: {final_score}")
