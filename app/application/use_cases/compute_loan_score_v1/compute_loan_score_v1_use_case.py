from fastapi.concurrency import run_in_threadpool
from app.application.use_cases.controllers.loan_transactions_controller import (
    LoanTransactionController,
)
from app.domain.entities.score import Score
from app.domain.shared_ports.loan_transaction_ports import LoanTransactionPorts
from tensorflow import keras
from keras.models import load_model, Model
import numpy as np

model: Model = load_model(
    "./app/application/use_cases/compute_loan_score_v1/zscore_complete.h5"
)


class ComputeLoanScoreV1UseCase(LoanTransactionPorts):
    async def compute_loan_score(self, address: str, k: int = 5, **kwargs) -> Score:
        loan_transaction_controller = LoanTransactionController()
        transactions = await loan_transaction_controller.list_transactions(address, k)
        input_features = np.array(
            [
                [
                    transaction.total_collateral_eth,
                    transaction.current_liquidation_threshold,
                    transaction.available_borrows_eth,
                    transaction.total_debt_eth,
                ]
                for transaction in transactions
            ]
        )
        result = await run_in_threadpool(model.predict, input_features[np.newaxis, :])
        return result[0].tolist()
