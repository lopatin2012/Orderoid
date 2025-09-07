// static/js/tower_enemies/main.js

const canvas = document.getElementById('gameCanvas');
const game = new Game(canvas);

function gameLoop() {
    game.update();
    game.draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();

document.getElementById('spawnBtn').addEventListener('click', () => {
    // FIXME Придумать выбор башни, с ограничением построек.
    game.placeTower(7, 7);
});

// Обновление UI
function updateUI() {
    document.getElementById('gold').textContent = game.gold;
    document.getElementById('lives').textContent = game.lives;
    document.getElementById('wave').textContent = game.wave;
    requestAnimationFrame(updateUI);
}
updateUI();