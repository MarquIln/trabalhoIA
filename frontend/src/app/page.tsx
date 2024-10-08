'use client'

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [board, setBoard] = useState(Array(9).fill(""));
  const [winner, setWinner] = useState("");
  const [isGameOver, setIsGameOver] = useState(false);

  const handleClick = (index: number) => {
    if (board[index] !== "" || isGameOver) return;

    const newBoard = [...board];
    newBoard[index] = currentPlayer();
    setBoard(newBoard);

    if (newBoard.every((cell) => cell !== "")) {
      checkWinner(newBoard);
    }
  };

  const currentPlayer = () => {
    const xCount = board.filter((cell) => cell === "X").length;
    const oCount = board.filter((cell) => cell === "O").length;
    return xCount <= oCount ? "X" : "O";
  };

  const checkWinner = async (boardState: string[]) => {
    try {
      const response = await axios.post("http://localhost:5000/check_winner", {
        board: boardState,
      });
      setWinner(response.data.winner);
      setIsGameOver(true);
    } catch (error) {
      console.error("Error checking winner", error);
    }
  };

  const resetGame = () => {
    setBoard(Array(9).fill(""));
    setWinner("");
    setIsGameOver(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-8">Jogo da Velha</h1>

      <div className="grid grid-cols-3 gap-4">
        {board.map((cell, index) => (
          <button
            key={index}
            className="w-20 h-20 text-2xl font-bold border"
            onClick={() => handleClick(index)}
          >
            {cell}
          </button>
        ))}
      </div>

      {winner && (
        <div className="mt-8">
          <h2 className="text-xl font-bold">
            {winner === "Em andamento" ? "Jogo em andamento..." : `Resultado: ${winner}`}
          </h2>
          <button
            onClick={resetGame}
            className="mt-4 p-2 bg-blue-500 text-white rounded"
          >
            Jogar Novamente
          </button>
        </div>
      )}
    </div>
  );
}
