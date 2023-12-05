import {
  Network,
  Alchemy,
  AssetTransfersCategory,
  AssetTransfersResult,
} from "alchemy-sdk";

// Optional config object, but defaults to demo api-key and eth-mainnet.
const settings = {
  apiKey: process.env.NEXT_PUBLIC_ALCHEMY_KEY, // Replace with your Alchemy API Key.
  network: Network.MATIC_MUMBAI, // Replace with your network.
};
const alchemy = new Alchemy(settings);

export const getAddressAge = async (address: string) => {
  const data = await alchemy.core.getAssetTransfers({
    fromAddress: address,
    category: [AssetTransfersCategory.ERC20],
  });
  if (!data.transfers.length) return 0.5;
  const transactions = data.transfers
    .map((transfer: AssetTransfersResult) => ({
      ...transfer,
      id: +transfer.blockNum,
    }))
    .sort((a: any, b: any) => a.id - b.id);
  const firstTransaction = transactions[0];
  const initialBlock = await alchemy.core.getBlock(firstTransaction.blockNum);
  const initialTimestamp = initialBlock.timestamp;
  // get number of years since initialTimestamp
  const now = Date.now();
  const age = now - initialTimestamp;
  return age / 1000 / 60 / 60 / 24 / 365;
};
