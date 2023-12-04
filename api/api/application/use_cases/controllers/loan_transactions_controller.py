from typing import Union, List
from api.application.controllers import DBController
import requests
from httpx import AsyncClient
from api.domain.entities.loan_transactions import LoanTransaction


class LoanTransactionController(DBController):
    def __init__(self):
        super().__init__()
        self.url = "https://api.thegraph.com/subgraphs/name/aave/protocol-v2"

    async def list_transactions(
        self, address: str, k: int = 5, **kwargs
    ) -> List[LoanTransaction]:
        # GraphQL query
        query = (
            """
        {
        borrows(where: { user: \""""
            + address
            + """\" }, first: """
            + str(k)
            + """, orderBy: timestamp, orderDirection: desc) {
                userReserve {
                currentTotalDebt
                currentATokenBalance
                currentStableDebt
                liquidityRate
                reserve {
                        baseLTVasCollateral
                        totalPrincipalStableDebt
                        totalLiquidity
                        totalDeposits
                        totalCurrentVariableDebt
                        totalLiquidityAsCollateral
                        reserveLiquidationThreshold
                    }
                }
            }
        }
        """
        )
        async with AsyncClient() as client:
            # Make the HTTP POST request
            response = await client.post(self.url, json={"query": query})
            if response.status_code == 200:
                data = response.json()

                # Process and structure the response data
                borrows_data = data["data"]["borrows"]
                borrows_features_list = []

                for borrow in borrows_data:
                    user_reserve = borrow["userReserve"]

                    # Calculations (these are simplistic and might need more complex logic based on Aave's specific calculation methods)
                    total_collateral_eth = (
                        float(user_reserve["reserve"]["totalLiquidityAsCollateral"])
                        / 1e18
                    )
                    total_debt_eth = float(user_reserve["currentTotalDebt"]) / 1e18
                    current_liquidation_threshold = (
                        float(user_reserve["reserve"]["reserveLiquidationThreshold"])
                        / 10000
                    )
                    ltv = float(user_reserve["reserve"]["baseLTVasCollateral"])
                    available_borrows_eth = (
                        total_collateral_eth * ltv / 10000 - total_debt_eth
                    )

                    borrow_features = {
                        "total_collateral_eth": total_collateral_eth,
                        "current_liquidation_threshold": current_liquidation_threshold,
                        "available_borrows_eth": available_borrows_eth,
                        "total_debt_eth": total_debt_eth,
                    }
                    borrows_features_list.append(borrow_features)

                return [LoanTransaction(**x) for x in borrows_features_list]
            else:
                raise Exception(
                    "Query failed with status code {}. {}".format(
                        response.status_code, query
                    )
                )
