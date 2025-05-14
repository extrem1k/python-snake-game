// Konfiguracja zmiennych globalnych
let gameId = null;
let gameState = null;
let gameInterval = null;
let boardSize = [10, 10];
let moveDirection = 'right';
let lastDirection = 'right';
const API_URL = 'http://localhost:5000/api';
const GAME_SPEED = 200; // milisekundy między ruchami (szybkość gry)

// Elementy DOM
const gameSetupSection = document.getElementById('game-setup');
const gameBoardSection = document.getElementById('game-board-section');
const gameBoard = document.getElementById('game-board');
const scoreDisplay = document.getElementById('score-display');
const gameOverScreen = document.getElementById('game-over');
const finalScoreDisplay = document.getElementById('final-score');
const startGameButton = document.getElementById('start-game');
const playAgainButton = document.getElementById('play-again');
const nicknameInput = document.getElementById('nickname');
const boardWidthInput = document.getElementById('board-width');
const boardHeightInput = document.getElementById('board-height');

// Funkcje obsługi API
async function createNewGame() {
    const nickname = nicknameInput.value || 'Anonymous';
    boardSize = [
        parseInt(boardWidthInput.value) || 10,
        parseInt(boardHeightInput.value) || 10
    ];

    // Walidacja rozmiaru planszy
    if (boardSize[0] < 5 || boardSize[0] > 25 || boardSize[1] < 5 || boardSize[1] > 25) {
        alert('Rozmiar planszy musi być pomiędzy 5 a 25!');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/game/new`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nickname: nickname,
                board_size: boardSize
            })
        });

        if (!response.ok) throw new Error('Nie udało się stworzyć nowej gry');

        const data = await response.json();
        gameId = data.game_id;
        gameState = data;

        // Ukryj setup, pokaż planszę gry
        gameSetupSection.classList.add('hidden');
        gameBoardSection.classList.remove('hidden');

        // Renderuj planszę i rozpocznij grę
        renderBoard();
        updateScore();
        startGameLoop();

    } catch (error) {
        console.error('Błąd podczas tworzenia nowej gry:', error);
        alert('Wystąpił błąd podczas łączenia z serwerem gry. Sprawdź czy backend jest uruchomiony.');
    }
}

async function getGameState() {
    try {
        const response = await fetch(`${API_URL}/game/state/${gameId}`);
        if (!response.ok) throw new Error('Nie udało się pobrać stanu gry');

        const data = await response.json();
        gameState = data;
        return data;
    } catch (error) {
        console.error('Błąd podczas pobierania stanu gry:', error);
        return null;
    }
}

async function sendMove(direction) {
    if (!gameId || gameState.game_over) return;

    try {
        const response = await fetch(`${API_URL}/game/move/${gameId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ direction })
        });

        if (!response.ok) throw new Error('Nie udało się wykonać ruchu');

        const data = await response.json();
        gameState = data;

        renderBoard();
        updateScore();

        // Sprawdź, czy gra się zakończyła
        if (gameState.game_over) {
            endGame();
        }

        return data;
    } catch (error) {
        console.error('Błąd podczas wykonywania ruchu:', error);
        return null;
    }
}

// Funkcje gry
function renderBoard() {
    if (!gameState) return;

    const [width, height] = gameState.board_size;

    // Ustaw siatkę CSS dla planszy
    gameBoard.style.gridTemplateColumns = `repeat(${width}, 25px)`;
    gameBoard.innerHTML = '';

    // Stwórz komórki planszy
    for (let y = height - 1; y >= 0; y--) {
        for (let x = 0; x < width; x++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');

            // Sprawdź, czy w tej komórce jest wąż lub jedzenie
            let isSnakeHead = false;
            let isSnakeBody = false;
            let isFood = false;

            // Sprawdź czy na danej pozycji jest głowa węża
            if (gameState.snake[0][0] === x && gameState.snake[0][1] === y) {
                isSnakeHead = true;
            }

            // Sprawdź czy na danej pozycji jest ciało węża
            for (let i = 1; i < gameState.snake.length; i++) {
                if (gameState.snake[i][0] === x && gameState.snake[i][1] === y) {
                    isSnakeBody = true;
                    break;
                }
            }

            // Sprawdź czy na danej pozycji jest jedzenie
            if (gameState.food[0] === x && gameState.food[1] === y) {
                isFood = true;
            }

            // Dodaj odpowiednie klasy
            if (isSnakeHead) {
                cell.classList.add('snake-head');
            } else if (isSnakeBody) {
                cell.classList.add('snake-body');
            } else if (isFood) {
                cell.classList.add('food');
            }

            gameBoard.appendChild(cell);
        }
    }
}

function updateScore() {
    if (!gameState) return;

    const score = gameState.score;
    scoreDisplay.textContent = `Wynik: ${score}`;
}

function startGameLoop() {
    // Zatrzymaj poprzedni interwał, jeśli istnieje
    if (gameInterval) {
        clearInterval(gameInterval);
    }

    // Ustaw nowy interwał
    gameInterval = setInterval(async () => {
        if (gameState && !gameState.game_over) {
            // Wykonaj ruch w bieżącym kierunku
            await sendMove(moveDirection);
            lastDirection = moveDirection;
        }
    }, GAME_SPEED);
}

function endGame() {
    // Zatrzymaj pętlę gry
    if (gameInterval) {
        clearInterval(gameInterval);
        gameInterval = null;
    }

    // Wyświetl ekran końca gry
    finalScoreDisplay.textContent = `Twój wynik: ${gameState.score}`;
    gameOverScreen.classList.remove('hidden');
}

function resetGame() {
    // Ukryj ekran końca gry
    gameOverScreen.classList.add('hidden');

    // Resetuj zmienne stanu
    gameId = null;
    gameState = null;
    moveDirection = 'right';
    lastDirection = 'right';

    // Wróć do ekranu konfiguracji
    gameBoardSection.classList.add('hidden');
    gameSetupSection.classList.remove('hidden');
}

// Obsługa zdarzeń
startGameButton.addEventListener('click', createNewGame);
playAgainButton.addEventListener('click', resetGame);

// Obsługa klawiatury
document.addEventListener('keydown', (event) => {
    // Nie wykonuj akcji, jeśli gra się nie rozpoczęła
    if (!gameState || gameState.game_over) return;

    const key = event.key.toLowerCase();

    // Mapowanie klawiszy
    const oppositeDirections = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left'
    };

    // Określ kierunek na podstawie klawisza
    let newDirection = moveDirection;

    if (key === 'arrowup' || key === 'w') {
        newDirection = 'up';
    } else if (key === 'arrowdown' || key === 's') {
        newDirection = 'down';
    } else if (key === 'arrowleft' || key === 'a') {
        newDirection = 'left';
    } else if (key === 'arrowright' || key === 'd') {
        newDirection = 'right';
    }

    // Zapobiegaj ruchowi w przeciwnym kierunku
    if (newDirection !== oppositeDirections[lastDirection]) {
        moveDirection = newDirection;
    }
});