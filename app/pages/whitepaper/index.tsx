import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import ctaStyle from "@/components/cta.module.css";

import {
  useAddress,
  useContract,
  ConnectWallet,
  useContractWrite,
} from "@thirdweb-dev/react";
import { Inter } from "next/font/google";
import Score from "@/components/score";
import WhitePaper from "@/components/whitepaper";

function IconBank(props: any) {
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
      <rect width="20" height="12" x="2" y="6" rx="2" />
      <circle cx="12" cy="12" r="2" />
      <path d="M6 12h.01M18 12h.01" />
    </svg>
  );
}

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  function WalletBtn() {
    return (
      <>
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
      </>
    );
  }

  return (
    <>
      <main
        className={`container mx-auto flex min-h-screen flex-col items-center justify-between ${inter.className} ${ctaStyle.cta}`}
      >
        <section className="w-full py-12">
          <header className="flex h-20 w-full items-center px-4 md:px-6">
            <Link href="/">
              <IconBank className="h-6 w-6" />
              <span className="sr-only">Score de Crédito e Empréstimo</span>
            </Link>
            <Link
              href="/whitepaper"
              className="pl-3 text-xl hover:text-slate-500 font-bold"
            >
              <p>Como funciona?</p>
            </Link>
            <Link
              href={`${process.env.NEXT_PUBLIC_API_URL}/docs`}
              target="_blank"
              className="pl-3 text-xl hover:text-slate-500"
            >
              <p>Conheça nossa API</p>
            </Link>
            <nav className="ml-auto flex gap-4 sm:gap-6">
              <WalletBtn />
            </nav>
          </header>
        </section>
        <WhitePaper />
      </main>

      <footer className="w-full py-4 px-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-600">
        <div className="container mx-auto flex justify-between items-center">
          <span className="text-gray-600 dark:text-gray-300 text-sm">
            © CreditLoans. All rights reserved.
          </span>
          <nav className="space-x-4">
            <Link
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-50 text-sm"
              href="#"
            >
              Terms & Conditions
            </Link>
            <Link
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-50 text-sm"
              href="#"
            >
              Privacy Policy
            </Link>
          </nav>
        </div>
      </footer>
    </>
  );
}
