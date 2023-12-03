import json
import logging
from pdb import run
import time
from typing import Optional
from fastapi.concurrency import run_in_threadpool
import pandas as pd
from datetime import timedelta
import math
import numpy as np
from sqlalchemy import select
from web3 import Web3
from api.application.model.score import ScoreModel
from api.config import settings
import asyncio
from api.application.model.db import session

# Replace with your Alchemy API key
alchemy_api_key = settings.ALCHEMY_API_KEY

w3 = Web3(Web3.HTTPProvider(f"https://eth-mainnet.alchemyapi.io/v2/{alchemy_api_key}"))


def payment_tx_type(transaction):
    # Determines if the user is sender or receiver
    return "sender" if transaction["is_sender"] else "receiver"


def calculate_num_transactions(transactions, current_index, window=timedelta(hours=1)):
    # Counts transactions within a specified time window
    current_time = transactions.iloc[current_index]["timestamp"]
    return transactions[
        (transactions["timestamp"] >= current_time - window)
        & (transactions["timestamp"] <= current_time)
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
    print("No score change")
    return 0


async def compute_transaction_based_score(
    transactions_df: pd.DataFrame, user_score=400
):
    score = 0
    for index, transaction in transactions_df.iterrows():
        tx_type = payment_tx_type(transaction)
        num_transactions = await run_in_threadpool(
            calculate_num_transactions, transactions_df, index
        )
        other_address_score = transaction["other_address_score"]
        score_change = await run_in_threadpool(
            transaction_score,
            user_score,
            tx_type,
            other_address_score,
            num_transactions,
        )
        print(f"Score change for transaction {index}: {score_change}")
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


async def compute_holdings_based_score(
    eth_balance,
    nfts_held,
    account_age,
    erc20_tokens,
):
    eth_balance_score = await run_in_threadpool(
        calculate_ethereum_balance_score, eth_balance
    )
    print(f"ETH Balance Score = {eth_balance_score}")
    nfts_score = await run_in_threadpool(calculate_ethereum_nfts_score, nfts_held)
    print(f"NFTs Score = {nfts_score}")
    activity_score = await run_in_threadpool(
        calculate_ethereum_activity_score, account_age
    )
    print(f"Activity Score = {activity_score}")
    erc20_score = await run_in_threadpool(calculate_erc20_tokens_score, erc20_tokens)
    print(f"ERC20 Score = {erc20_score}")
    return eth_balance_score + nfts_score + activity_score + erc20_score


def compute_overall_score(
    address: str,
    eth_balance: float,
    nfts_held: int,
    account_age: int,
    erc20_tokens: int,
    transactions_df: pd.DataFrame,
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
    asyncio.run(save_score_in_db(address, final_score))
    return final_score


# def count_nfts():
#     try:
#         # Load the ABI of the NFT contract
#         with open("NFTContractABI.json", "r") as abi_file:
#             nft_contract_abi = json.load(abi_file)

#         # Create a contract instance
#         nft_contract = w3.eth.contract(
#             address=settings.NFT_CONTRACT_ADDRESS, abi=nft_contract_abi
#         )

#         # Call the balanceOf function to count NFTs owned by the user
#         nft_count = nft_contract.functions.balanceOf(user_address).call()

#         print(f"Number of NFTs owned by {user_address}: {nft_count}")
#     except Exception as e:
#         print(f"Error counting NFTs: {e}")


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
        "other_address_balance",
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
                            "user_balance": float(
                                w3.from_wei(
                                    w3.eth.get_balance(address, block_identifier=x),
                                    "ether",
                                )
                            ),
                            "other_address_balance": float(
                                w3.from_wei(
                                    w3.eth.get_balance(
                                        other_address,
                                        block_identifier=x,
                                    ),
                                    "ether",
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


async def get_score_in_db(address):
    async with session() as db_session:
        score: Optional[ScoreModel] = await db_session.scalar(
            select(ScoreModel).filter(ScoreModel.address == address).limit(1)
        )

        if score:
            return score.score
        return None


async def save_score_in_db(address, score):
    async with session() as db_session:
        score_model = ScoreModel(address=address, score=score)
        db_session.add(score_model)
        db_session.commit()
        return score_model


async def extract_payment_data(user_address):
    try:
        # Fetch transactions sent to the user's address
        block_end = await run_in_threadpool(w3.eth.get_block, "latest")
        block_end = block_end["number"]
        block_start = block_end - 100
        transactions = await run_in_threadpool(
            getTransactions, block_start, block_end, user_address
        )
        other_address_scores = []
        for _, row in transactions.iterrows():
            block_end = row["block_number"]
            other_address = row["other_address"]
            other_address_score = await get_score_in_db(other_address)

            if other_address_score:
                logging.info(f"Found score for {other_address}: {other_address_score}")
            else:
                other_address_score = (
                    row["other_address_balance"]
                    if row["other_address_balance"] > 0
                    else 100
                )
            other_address_scores.append(other_address_score)
        transactions["other_address_score"] = other_address_scores
        transactions["timestamp"] = pd.to_datetime(transactions["timestamp"])
        return transactions
    except Exception as e:
        print(f"Error fetching transactions: {e}")
