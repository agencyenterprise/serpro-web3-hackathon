import axios from "axios";

axios.defaults.baseURL = process.env.NEXT_PUBLIC_API_URL;

export const api = axios.create({
  headers: {
    "Content-Type": "application/json",
  },
});

export interface IScore {
  score: number;
  transaction_score: number;
  loan_score: number;
  holdings_score: number;
}

const round = (value: number, decimals: number = 2) => {
  return Math.round(value * 100) / 100;
};
export const getScore = async (
  address: string,
  eth_balance: number,
  nfts_held: number,
  account_age: number,
  erc20_tokens: number
): Promise<IScore> => {
  const response = await api.post(`/api/v1/complete`, {
    address,
    eth_balance,
    nfts_held,
    account_age,
    erc20_tokens,
  });
  return {
    score: round(response.data.score),
    loan_score: round(response.data.loan_score),
    transaction_score: round(response.data.transaction_score),
    holdings_score: round(response.data.holdings_score),
  };
};
