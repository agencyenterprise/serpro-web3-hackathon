import "@/styles/globals.css";
import type { AppProps } from "next/app";

import { ThirdwebProvider, metamaskWallet } from "@thirdweb-dev/react";
import { MathJaxContext } from "better-react-mathjax";
const config = {
  loader: { load: ["input/asciimath", "output/chtml"] },
  asciimath2jax: {
    delimiters: [["$$", "$$"]],
    preview: "none",
  },
};
export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <MathJaxContext config={config}>
        <ThirdwebProvider
          activeChain="mumbai"
          clientId={process.env.NEXT_PUBLIC_CLIENT_ID}
          supportedWallets={[metamaskWallet()]}
        >
          <Component {...pageProps} />
        </ThirdwebProvider>
      </MathJaxContext>
    </>
  );
}
