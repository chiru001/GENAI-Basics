// JavaScript Snake Game
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = 400;
canvas.height = 400;

const gridSize = 20; // Size of each grid cell
let snake = [{ x: 200, y: 200 }]; // Initial snake
let food = generateRandomFood();
let dx = gridSize;
let dy = 0;
let score = 0;
let gameInterval;

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawSnake();
    drawFood();
    moveSnake();
    checkCollision();
}

function drawSnake() {
    ctx.fillStyle = 'green';
    snake.forEach(segment => {
        ctx.fillRect(segment.x, segment.y, gridSize, gridSize);
    });
}

function drawFood() {
    ctx.fillStyle = 'red';
    ctx.fillRect(food.x, food.y, gridSize, gridSize);
}

function moveSnake() {
    const head = { x: snake[0].x + dx, y: snake[0].y + dy };
    snake.unshift(head);

    if (head.x === food.x && head.y === food.y) {
        score++;
        document.getElementById('score').textContent = score;
        food = generateRandomFood();
    } else {
        snake.pop();
    }
}

function generateRandomFood() {
    const x = Math.floor(Math.random() * canvas.width / gridSize) * gridSize;
    const y = Math.floor(Math.random() * canvas.height / gridSize) * gridSize;
    return { x, y };
}

function checkCollision() {
    const head = snake[0];
    if (head.x < 0 || head.x >= canvas.width || head.y < 0 || head.y >= canvas.height) {
        gameOver();
    }

    for (let i = 4; i < snake.length; i++) {
        if (head.x === snake[i].x && head.y === snake[i].y) {
            gameOver();
        }
    }
}

function changeDirection(event) {
    const LEFT_KEY = 37;
    const UP_KEY = 38;
    const RIGHT_KEY = 39;
    const DOWN_KEY = 40;

    const keyPressed = event.keyCode;
    const goingUp = dy === -gridSize;
    const goingDown = dy === gridSize;
    const goingRight = dx === gridSize;
    const goingLeft = dx === -gridSize;

    if (keyPressed === LEFT_KEY && !goingRight) {
        dx = -gridSize;
        dy = 0;
    }

    if (keyPressed === UP_KEY && !goingDown) {
        dx = 0;
        dy = -gridSize;
    }

    if (keyPressed === RIGHT_KEY && !goingLeft) {
        dx = gridSize;
        dy = 0;
    }

    if (keyPressed === DOWN_KEY && !goingUp) {
        dx = 0;
        dy = gridSize;
    }
}

function gameOver() {
    clearInterval(gameInterval);
    alert('Game Over! Your Score: ' + score);
}

document.getElementById('startButton').addEventListener('click', function() {
    snake = [{ x: 200, y: 200 }];
    dx = gridSize;
    dy = 0;
    score = 0;
    document.getElementById('score').textContent = score;
    food = generateRandomFood();
    clearInterval(gameInterval);
    gameInterval = setInterval(draw, 100);
});

document.addEventListener('keydown', changeDirection);