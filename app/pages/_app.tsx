import "@/styles/globals.css";
import type { AppProps } from "next/app";

import {
  ThirdwebProvider,
  metamaskWallet,
  coinbaseWallet,
  walletConnect,
  localWallet,
  embeddedWallet,
} from "@thirdweb-dev/react";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <ThirdwebProvider
        activeChain="mumbai"
        clientId={process.env.NEXT_PUBLIC_CLIENT_ID}
        supportedWallets={[
          metamaskWallet(),
          coinbaseWallet({ recommended: true }),
          walletConnect(),
          localWallet(),
          embeddedWallet(),
        ]}
      >
        <Component {...pageProps} />
      </ThirdwebProvider>
    </>
  );
}
