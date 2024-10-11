// minimax.ts

export type Player = 'X' | 'O';
export type Board = (Player | "")[];

const EMPTY: Player | "" = ""; // Representação do espaço vazio

const checkWinner = (board: Board): Player | "Empate" | null => {
  const winningCombinations = [
    // Linhas
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    // Colunas
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    // Diagonais
    [0, 4, 8],
    [2, 4, 6],
  ];

  for (const combination of winningCombinations) {
    const [a, b, c] = combination;
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      return board[a];
    }
  }

  return board.includes(EMPTY) ? null : 'Empate';
};

export const minimax = (board: Board, depth: number, isMaximizing: boolean): number => {
  const winner = checkWinner(board);
  if (winner === 'X') return -10 + depth; // 'X' é o jogador minimizador
  if (winner === 'O') return 10 - depth; // 'O' é o jogador maximizador
  if (winner === 'Empate') return 0;

  if (isMaximizing) {
    let bestScore = -Infinity;
    for (let i = 0; i < 9; i++) {
      if (board[i] === EMPTY) {
        board[i] = 'O'; // 'O' é o jogador maximizador
        const score = minimax(board, depth + 1, false);
        board[i] = EMPTY; // Reverter movimento
        bestScore = Math.max(score, bestScore);
      }
    }
    return bestScore;
  } else {
    let bestScore = Infinity;
    for (let i = 0; i < 9; i++) {
      if (board[i] === EMPTY) {
        board[i] = 'X'; // 'X' é o jogador minimizador
        const score = minimax(board, depth + 1, true);
        board[i] = EMPTY; // Reverter movimento
        bestScore = Math.min(score, bestScore);
      }
    }
    return bestScore;
  }
};

export const bestMove = (board: Board): number => {
  let bestScore = -Infinity;
  let move = -1;

  for (let i = 0; i < 9; i++) {
    if (board[i] === EMPTY) {
      board[i] = 'O'; // 'O' é o jogador maximizador
      const score = minimax(board, 0, false);
      board[i] = EMPTY; // Reverter movimento

      if (score > bestScore) {
        bestScore = score;
        move = i;
      }
    }
  }

  return move;
};
