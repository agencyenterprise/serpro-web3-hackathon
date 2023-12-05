import { CardTitle, CardHeader, CardContent, Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { useState } from "react";
import {
  useAddress,
  useBalance,
  useContract,
  useContractWrite,
} from "@thirdweb-dev/react";
import { getAddressAge } from "@/utils";
import { NATIVE_TOKEN_ADDRESS } from "@thirdweb-dev/sdk";
import { getScore, IScore } from "@/services/api";
import Loader from "./loader";
import { toast } from "react-toastify";

export default function Score() {
  const [scoreLoadingState, setScoreLoadingState] = useState(false);
  const [score, setScore] = useState<IScore | null>(null);
  const address = useAddress();
  const success = (msg: string) => toast(msg, { type: "success" });
  const error = (msg: string) => toast(msg, { type: "error" });
  const info = (msg: string) => toast(msg, { type: "info" });
  const { data: balance, isLoading: isBalanceLoading } =
    useBalance(NATIVE_TOKEN_ADDRESS);
  const contractAddress = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS || "";
  const { contract } = useContract(contractAddress);
  const { mutateAsync: createTPFtAsync } = useContractWrite(
    contract,
    "createTPFt"
  );
  let counter = 0;
  const { mutateAsync: mintAsync } = useContractWrite(contract, "mint");

  async function createTPFt() {
    await createTPFtAsync({
      args: [["test", "test", new Date().getTime()]],
    });
  }
  async function mint() {
    try {
      setScoreLoadingState(true);
      await mintAsync({
        args: [address, 0, 1],
      });
      success("Compra realizada com sucesso!");
      await computeScore();
    } catch (e) {
      error("Erro ao realizar a compra! Tente novamente mais tarde");
      console.log(e);
    } finally {
      setScoreLoadingState(false);
    }
  }
  async function countNFTs(): Promise<number> {
    if (!contract) return 0;
    const nfts = await contract!.call("getUserTPFtData", [address]);
    if (!Array.isArray(nfts) || !nfts.length) return 0;
    return nfts[0].length;
  }
  async function computeScore() {
    try {
      setScoreLoadingState(true);
      info("Calculando o seu score, isso pode levar alguns segundos...");
      if (!address || !contract || !balance) return;
      const nftCount = await countNFTs();
      const accountAge = await getAddressAge(address!);
      console.log(
        `address: ${address}, balance: ${
          balance!.displayValue
        }, nftCount: ${nftCount}, accountAge: ${accountAge}`
      );

      const completeScore = await getScore(
        address,
        +balance.displayValue,
        nftCount,
        accountAge,
        0
      );
      setScore({ ...completeScore });
      success("Score calculado com sucesso!");
    } catch (e) {
      error("Erro ao calcular o Score! Tentar novamente mais tarde");
      console.log(e);
    } finally {
      setScoreLoadingState(false);
    }
  }
  function Loans() {
    return (
      <section className="w-full py-12">
        <div className="container px-4 md:px-6">
          <h2 className="text-3xl font-bold mb-6 dark:text-gray-900">
            Interessado em aumentar o seu Score de Crédito?
          </h2>
          <p className="text-2xl font-bold mb-6 dark:text-gray-900">
            Adquira já um titulo público tokenizado
          </p>
          <div className="grid gap-6 lg:grid-cols-3">
            <div className="border-2 border-gray-200 rounded-lg p-4 dark:border-gray-800 bg-slate-50">
              <h3 className="text-lg font-bold mb-2 dark:text-gray-900 ">
                TESOURO PREFIXADO 2026
              </h3>
              <p className="text-gray-500 mb-2 dark:text-gray-900">
                Rentabilidade anual: 10.02%
              </p>
              <p className="text-gray-500 mb-2 dark:text-gray-900">
                Vencimento em: 01/01/2026
              </p>
              <div className="pt-5">
                <Button
                  className="inline-flex h-9 items-center justify-center rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-gray-50 shadow transition-colors hover:bg-gray-900/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-gray-950 disabled:pointer-events-none disabled:opacity-50 dark:bg-gray-50 dark:text-gray-900 dark:hover:bg-gray-50/90 dark:focus-visible:ring-gray-300"
                  onClick={mint}
                >
                  Comprar
                </Button>
              </div>
            </div>
            <div className="border-2 border-gray-200 rounded-lg p-4 dark:border-gray-800 bg-slate-50">
              <h3 className="text-lg font-bold mb-2 dark:text-gray-900 ">
                TESOURO PREFIXADO 2029
              </h3>
              <p className="text-gray-500 mb-2 dark:text-gray-900">
                Rentabilidade anual: 10.63%
              </p>
              <p className="text-gray-500 mb-2 dark:text-gray-900">
                Vencimento em: 01/01/2029
              </p>
              <div className="pt-5">
                <Button
                  className="inline-flex h-9 items-center justify-center rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-gray-50 shadow transition-colors hover:bg-gray-900/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-gray-950 disabled:pointer-events-none disabled:opacity-50 dark:bg-gray-50 dark:text-gray-900 dark:hover:bg-gray-50/90 dark:focus-visible:ring-gray-300"
                  onClick={mint}
                >
                  Comprar
                </Button>
              </div>
            </div>
            <div className="border-2 border-gray-200 rounded-lg p-4 dark:border-gray-800 bg-slate-50">
              <h3 className="text-lg font-bold mb-2 dark:text-gray-900 ">
                TESOURO PREFIXADO 2033
              </h3>
              <p className="text-gray-500 mb-2 dark:text-gray-900">
                Rentabilidade anual: 10.90%
              </p>
              <p className="text-gray-500 mb-2 dark:text-gray-900">
                Vencimento em: 01/01/2033
              </p>
              <div className="pt-5">
                <Button
                  className="inline-flex h-9 items-center justify-center rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-gray-50 shadow transition-colors hover:bg-gray-900/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-gray-950 disabled:pointer-events-none disabled:opacity-50 dark:bg-gray-50 dark:text-gray-900 dark:hover:bg-gray-50/90 dark:focus-visible:ring-gray-300"
                  onClick={mint}
                >
                  Comprar
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
  return (
    <>
      {!score && !scoreLoadingState && !!address && (
        <Button className="text-3xl px-10 py-10" onClick={computeScore}>
          Calcular Score
        </Button>
      )}
      {!address && (
        <p className="text-2xl text-slate-800">
          Conecte sua carteira e comece a usar agora mesmo!
        </p>
      )}
      {scoreLoadingState && <Loader />}
      {!!score &&
        !!address &&
        !!contract &&
        !isBalanceLoading &&
        !scoreLoadingState && (
          <Card className="max-w-xl mx-auto">
            <CardHeader>
              <CardTitle className="text-xl font-bold text-center">
                Score de Crédito
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center">
                <p className="text-6xl font-bold">{score.score}</p>
                <div className="h-2 rounded py-3">
                  <Progress
                    value={score.score}
                    max={1000}
                    className="bg-gray-200"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <IconDollarSign className="w-5 h-5 text-green-500 dark:text-green-400" />
                    <p>Atividade Financeira Recente (100 blocos)</p>
                  </div>
                  <p className="text-blue-400">{score.transaction_score}</p>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <IconPlus className="w-5 h-5 text-purple-500 dark:text-purple-400" />
                    <p>Títulos e Investimentos</p>
                  </div>
                  <p className="text-blue-400">{score.holdings_score}</p>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <IconCreditCard className="w-5 h-5 text-blue-500 dark:text-blue-400" />
                    <p>Adimplência</p>
                  </div>
                  <p className="text-blue-400">{score.loan_score * 100}%</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      {!!score && <Loans />}
    </>
  );
}

function IconClock(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <polyline points="12 6 12 12 16 14" />
    </svg>
  );
}

function IconCreditCard(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect width="20" height="14" x="2" y="5" rx="2" />
      <line x1="2" x2="22" y1="10" y2="10" />
    </svg>
  );
}

function IconDollarSign(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <line x1="12" x2="12" y1="2" y2="22" />
      <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
    </svg>
  );
}

function IconPieChart(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
      <path d="M22 12A10 10 0 0 0 12 2v10z" />
    </svg>
  );
}

function IconPlus(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M5 12h14" />
      <path d="M12 5v14" />
    </svg>
  );
}
