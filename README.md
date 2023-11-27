# Web3 User Scoring System

## Overview

This scoring system calculates a comprehensive score for Web3 users, taking into account their Ethereum holdings, NFTs, activity, ERC20 tokens, and transaction behavior. The aim is to create a fair and dynamic score that reflects a user's trustworthiness and financial health in the Web3 ecosystem.

### Components

1. Transaction-based Scoring
   Calculates a score based on the user's interactions with other addresses. It considers the frequency of transactions and the score difference between interacting addresses.

2. Holdings-based Scoring
   Evaluates Ethereum balance, NFT holdings, account activity, and ERC20 token holdings to compute a score that reflects the user's asset strength.

3. Overall Scoring
   Combines transaction-based and holdings-based scores to produce a final score between 0 and 1000.

4. LSTM Model for Liquidation Risk Prediction:
   designed to predict the likelihood of loan liquidation in decentralized finance (DeFi) platforms

### Transaction-based Scoring Formulae:

- Influence Factor (IF): $A \times (1 - e^{-k \times |S_{\text{current}} - S_{\text{other}}|})$
- Frequency Modifier (FM): $\dfrac{B} {(1 + e^{-C \times (n_{transactions} - 1)})}$
- Transaction Score: Varies based on the transaction type (sending or receiving) and the score difference between interacting addresses.

#### Holdings-based Scoring Formulae:

- Ethereum Balance Score: $(\dfrac{balance} {1000000}) \times 300$

- Ethereum NFTs Held Score: $(\dfrac{nfts}{20}) \times 300$

- Ethereum Activity Score: $(\dfrac{age} {10}) \times 150$

- ERC20 Tokens Score: $(\dfrac{balance_{erc20}}{10000}) \times 100$

### LSTM Model for Liquidation Risk Prediction

This LSTM (Long Short-Term Memory) model is specifically designed to predict the likelihood of loan liquidation in decentralized finance (DeFi) platforms, using data from the Aave lending protocol.

#### Liquidation Process in DeFi

- Liquidation occurs when a borrower's collateral value falls below a certain threshold, making the loan risky for lenders.
- The model predicts this risk by analyzing patterns in loan transactions and borrower behaviors.

#### Model Architecture

- Multiple LSTM layers capture temporal dependencies in transaction data, crucial for understanding borrower's financial behavior over time.
- Dropout layers follow each LSTM layer, reducing overfitting and enhancing model generalization.
- The output layer predicts the probability of liquidation, helping platforms and users to proactively manage risk.

#### Application

- The model aids in assessing the liquidation risk of loans on DeFi platforms.
- It provides insights for both lenders and borrowers, enabling informed decision-making and risk management in the dynamic DeFi ecosystem.
