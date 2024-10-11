export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-800 text-white">
      <h1 className="text-4xl font-bold mb-6">Bem-vindo ao Jogo da Velha</h1>
      <div className="flex space-x-4">
        <a
          href="/pages/game?mode=2p"
          className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-lg font-semibold"
        >
          Jogar Contra Outro Jogador
        </a>
        <a
          href="/pages/game?mode=IA"
          className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-lg font-semibold"
        >
          Jogar Contra a IA
        </a>
      </div>
    </div>
  );
}
