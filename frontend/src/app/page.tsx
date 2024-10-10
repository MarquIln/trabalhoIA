'use client';

import { useState, useEffect } from "react";
import axios from 'axios';

export default function Home() {
  const [board, setBoard] = useState(Array(9).fill(""));
  const [winner, setWinner] = useState("");
  const [isGameOver, setIsGameOver] = useState(false);
  
  const currentPlayer = () => (board.filter((cell) => cell).length % 2 === 0 ? "X" : "O");

  const checkGameStatus = async (newBoard: string[]) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/check_winner', {
        board: newBoard
      });
      console.log('response:', response.data);

      const { winner, game_status } = response.data;
      
      if (game_status === 'Em andamento') {
        setWinner("");
      } else {
        setWinner(winner);
        setIsGameOver(true);
      }
    } catch (error) {
      console.error('Erro ao verificar o vencedor:', error);
    }
  };

  useEffect(() => {
    if (board.includes("") && !isGameOver) {
      checkGameStatus(board);
    }
  }, [board, isGameOver]);


  const handleClick = (index: number) => {
    if (board[index] !== "" || isGameOver) return;

    const newBoard = [...board];
    newBoard[index] = currentPlayer();
    setBoard(newBoard);
  };

  const resetGame = () => {
    setBoard(Array(9).fill(""));
    setWinner("");
    setIsGameOver(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-800 text-white">
      <h1 className="text-4xl font-bold mb-6">Jogo da Velha</h1>
      <div className="grid grid-cols-3 gap-4">
        {board.map((cell, index) => (
          <button
            key={index}
            onClick={() => handleClick(index)}
            className="w-24 h-24 text-2xl font-bold bg-gray-700 hover:bg-gray-600 rounded-lg"
          >
            {cell}
          </button>
        ))}
      </div>
      {winner ? (
        <h2 className="text-2xl font-semibold mt-6">
          {winner === "Empate" ? "O jogo terminou em empate!" : `Jogador ${winner} venceu!`}
        </h2>
      ) : (
        <h2 className="text-2xl font-semibold mt-6">Jogo em andamento...</h2>
      )}
      <button
        onClick={resetGame}
        className="mt-8 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-lg font-semibold"
      >
        Reiniciar Jogo
      </button>
    </div>
  );
}
