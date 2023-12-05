import { MathJax } from "better-react-mathjax";
export default function WhitePaper() {
  return (
    <div className="container mx-auto p-4 text-left">

<h1 className="text-xl font-bold">Visão Geral</h1>
      <p>
      O Zscore está inovando ao construir um sistema de financiamento descentralizado que utiliza títulos públicos tokenizados como base para o cálculo do score de empréstimos. Empregando zero knowledge proofs, o Zscore desenvolve um modelo de machine learning para calcular o score Web3 de cidadãos e empresas, considerando fatores como transações anteriores, histórico de aquisição de títulos e títulos ativos por receber.
      </p>
      <h1 className="text-xl font-bold pt-2">Diferencial Competitivo</h1>
      <p>
      O Zscore destaca-se ao utilizar zero knowledge proofs e machine learning para calcular o score Web3 do usuário, oferecendo uma abordagem avançada e segura para a concessão de empréstimos descentralizados. Além disso, a tokenização de títulos públicos como informação proporciona uma base sólida de segurança e estabilidade, diferenciando o Zscore como uma opção confiável no mercado DeFi tradicional.  O sistema incorpora dados de plataformas de empréstimos Web3, como a Aave, onde parte do score é determinada pela avaliação da chance de adimplência. Para alcançar isso, removemos as informações das últimas tentativas de empréstimos do usuário e desenvolvemos um modelo que estabelece uma relação entre o health factor, a taxa de inadimplência e a liquidação. Essa abordagem inovadora e analítica proporciona uma visão mais precisa e dinâmica da saúde financeira do usuário, fortalecendo ainda mais a confiabilidade do Zscore no ecossistema financeiro.
      </p>

      




      <h1 className="text-xl font-bold pt-10">
        Sistema de Pontuação de Usuário Web3
      </h1>

      <h2 className="text-lg font-semibold mt-4">Visão Geral</h2>
      <p>
        Este sistema de pontuação calcula uma pontuação abrangente para usuários
        Web3, levando em conta suas posses em Ethereum, NFTs, atividade, tokens
        ERC20 e comportamento de transação. O objetivo é criar uma pontuação
        justa e dinâmica que reflete a confiabilidade e saúde financeira do
        usuário no ecossistema Web3.
      </p>

      <h3 className="font-semibold">Componentes</h3>
      <ol className="list-decimal ml-6">
        <li>
          <strong>Pontuação Baseada em Transação:</strong>
          Calcula uma pontuação com base nas interações do usuário com outros
          endereços. Considera a frequência de transações e a diferença de
          pontuação entre endereços interagentes.
        </li>
        <li>
          <strong>Pontuação Baseada em Posses:</strong>
          Avalia o saldo em Ethereum, posses de NFTs, atividade da conta e
          posses de tokens ERC20 para calcular uma pontuação que reflete a força
          do ativo do usuário.
        </li>
        <li>
          <strong>Pontuação Geral:</strong>
          Combina as pontuações baseadas em transação e em posses para produzir
          uma pontuação final entre 0 e 1000.
        </li>
        <li>
          <strong>Modelo LSTM para Previsão de Risco de Liquidação:</strong>
          Projetado para prever a probabilidade de liquidação de empréstimos em
          plataformas de finanças descentralizadas (DeFi).
        </li>
      </ol>

      <h3 className="font-semibold">
        Fórmulas de Pontuação Baseada em Transação:
      </h3>
      <ul className="list-disc ml-6">
        <li>
          <strong>Fator de Influência (IF):</strong>{" "}
          <MathJax dynamic>
            {
              "`A \\times (1 - e^{-k \\times |S_{\\text{atual}} - S_{\\text{outro}}|})`"
            }
          </MathJax>
        </li>
        <li>
          <strong>Modificador de Frequência (FM):</strong>{" "}
          <MathJax>
            {"`\\frac{B} {(1 + e^{-C \\times (n_{transações} - 1)})}`"}
          </MathJax>
        </li>
        <li>
          <strong>Pontuação de Transação:</strong> Varia com base no tipo de
          transação (envio ou recebimento) e na diferença de pontuação entre
          endereços interagentes.
        </li>
      </ul>

      <h3 className="font-semibold">
        Fórmulas de Pontuação Baseada em Posses:
      </h3>
      <ul className="list-disc ml-6">
        <li>
          <strong>Pontuação de Saldo em Ethereum:</strong>{" "}
          <MathJax>{"`(frac{saldo}{1000000}) \\times 300\\`"}</MathJax>
        </li>
        <li>
          <strong>Pontuação de NFTs Ethereum:</strong>{" "}
          <MathJax>{"`\\(\\frac{nfts}{20}) \\times 300\\`"}</MathJax>`
        </li>
        <li>
          <strong>Pontuação de Atividade Ethereum:</strong>{" "}
          <MathJax>{"`\\(\\frac{\\i\\d\\a\\d\\e}{10}) \\times 150\\`"}</MathJax>
        </li>
        <li>
          <strong>Pontuação de Tokens ERC20:</strong>{" "}
          <MathJax>
            {"`\\(\\frac{saldo_{erc20}}{10000}) \\times 100\\`"}
          </MathJax>
        </li>
      </ul>

      <h3 className="font-semibold">
        Modelo LSTM para Previsão de Risco de Liquidação
      </h3>
      <p>
        Este modelo LSTM (Memória de Longo e Curto Prazo) é especificamente
        projetado para prever a probabilidade de liquidação de empréstimos em
        plataformas de finanças descentralizadas (DeFi), usando dados do
        protocolo de empréstimo Aave.
      </p>

      <h4 className="font-semibold">Processo de Liquidação</h4>
    </div>
  );
}
