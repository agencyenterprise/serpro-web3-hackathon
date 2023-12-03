import Image from "next/image";
import {
  useAddress,
  useContract,
  ConnectWallet,
  useContractWrite,
} from "@thirdweb-dev/react";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const address = useAddress();
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
    await mintAsync({
      args: [address, 0, 1],
    });
  }

  return (
    <main
      className={`flex min-h-screen flex-col items-center justify-between p-24 ${inter.className}`}
    >
      <div className="self-end">
        <ConnectWallet
          theme={"dark"}
          modalSize={"wide"}
          dropdownPosition={{
            side: "bottom",
            align: "end",
          }}
        />
      </div>
      {address && contract && (
        <>
          <button
            type="button"
            className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            onClick={createTPFt}
          >
            createTPFt
          </button>
          <button
            type="button"
            className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            onClick={mint}
          >
            mint
          </button>
        </>
      )}
      <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700/10 after:dark:from-sky-900 after:dark:via-[#0141ff]/40 before:lg:h-[360px]">
        <Image
          className="relative dark:drop-shadow-[0_0_0.3rem_#ffffff70] dark:invert"
          src="/next.svg"
          alt="Next.js Logo"
          width={180}
          height={37}
          priority
        />
      </div>
    </main>
  );
}
