// static/js/tower_enemies/game.js

class Game {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;

        this.cellSize = 40;
        this.cols = Math.floor(this.width / this.cellSize);
        this.rows = Math.floor(this.height / this.cellSize);

        this.gold = 500;
        this.lives = 100;
        this.wave = 1;

        this.towers = [];
        this.enemies = [];
        this.projectiles = [];

        this.path = this.generatePath();
        this.spawnTimer = 0;
        this.waveTimer = 0;
        this.enemySpawnInterval = 60;

    }

    generatePath() {
        let path = [];
        for (let y = 5; y <= 10; y++) path.push({ x: 5, y });
        for (let x = 5; x <= 15; x++) path.push({ x, y: 10 });
        for (let y = 10; y >= 5; y--) path.push({ x: 15, y });
        return path;
    }

    update() {
        this.spawnEnemies();
        this.updateEnemies();
        this.updateTowers();
        this.updateProjectiles();
        this.checkCollisions();
    }

    spawnEnemies() {
        this.spawnTimer++;
        if (this.spawnTimer >= this.enemySpawnInterval) {
            this.enemies.push(new Enemy(this.path));
            this.spawnTimer = 0;
        }
    }

    updateEnemies() {
        this.enemies = this.enemies.filter(enemy => {
            enemy.move();
            if (enemy.reachedEnd) {
                this.lives--;
                return false;
            }
            return enemy.hp > 0;
        });
    }

    updateTowers() {
        this.towers.forEach(tower => {
            const target = this.enemies.find(e => {
                const dx = tower.x - e.x;
                const dy = tower.y - e.y;
                return Math.sqrt(dx * dx + dy * dy) < tower.range;
            });
            if (target && !tower.cooldown) {
                this.projectiles.push(new Projectile(tower.x, tower.y, target));
                tower.cooldown = 30;
            }
            if (tower.cooldown > 0) tower.cooldown--;
        });
    }

    updateProjectiles() {
        this.projectiles = this.projectiles.filter(proj => {
            proj.move();
            return !proj.hit;
        });
    }

    checkCollisions() {
        this.projectiles.forEach(proj => {
            const dx = proj.x - proj.target.x;
            const dy = proj.y - proj.target.y;
            if (Math.sqrt(dx * dx + dy * dy) < 15) {
                proj.target.hp -= proj.damage;
                proj.hit = true;
                if (proj.target.hp <= 0) {
                    this.gold += 10;
                }
            }
        });
    }

    draw() {
        this.ctx.clearRect(0, 0, this.width, this.height);

        // Рисуем путь
        this.ctx.fillStyle = '#444';
        this.path.forEach(p => {
            this.ctx.fillRect(p.x * this.cellSize, p.y * this.cellSize, this.cellSize, this.cellSize);
        });

        // Рисуем врагов
        this.ctx.fillStyle = 'red';
        this.enemies.forEach(e => {
            this.ctx.beginPath();
            this.ctx.arc(e.x, e.y, 10, 0, Math.PI * 2);
            this.ctx.fill();
        });

        // Рисуем башни
        this.ctx.fillStyle = 'blue';
        this.towers.forEach(t => {
            this.ctx.beginPath();
            this.ctx.arc(t.x, t.y, 15, 0, Math.PI * 2);
            this.ctx.fill();
        });

        // Рисуем снаряды
        this.ctx.fillStyle = 'yellow';
        this.projectiles.forEach(p => {
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
            this.ctx.fill();
        });
    }

    placeTower(x, y) {
        if (this.gold >= 20) {
            this.towers.push(new Tower(x, y));
            this.gold -= 20;
        }
    }

}

class Enemy {
    constructor(path) {
        this.path = path;
        this.index = 0;
        this.x = path[0].x * 40 + 20;
        this.y = path[0].y * 40 + 20;
        this.speed = 1;
        this.hp = 30;
        this.reachedEnd = false;
    }

    move() {
        if (this.index >= this.path.length - 1) {
            this.reachedEnd = true;
            return;
        }

        const target = this.path[this.index + 1];
        const tx = target.x * 40 + 20;
        const ty = target.y * 40 + 20;

        const dx = tx - this.x;
        const dy = ty - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < this.speed) {
            this.x = tx;
            this.y = ty;
            this.index++;
        } else {
            this.x += (dx / dist) * this.speed;
            this.y += (dy / dist) * this.speed;
        }
    }
}

class Tower {
    constructor(x, y) {
        this.x = x * 40 + 20;
        this.y = y * 40 + 20;
        this.range = 100;
        this.damage = 10;
        this.cooldown = 0;
    }
}

class Projectile {
    constructor(x, y, target) {
        this.x = x;
        this.y = y;
        this.target = target;
        this.speed = 5;
        this.damage = 10;
        this.hit = false;
    }

    move() {
        const dx = this.target.x - this.x;
        const dy = this.target.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < this.speed) {
            this.x = this.target.x;
            this.y = this.target.y;
        } else {
            this.x += (dx / dist) * this.speed;
            this.y += (dy / dist) * this.speed;
        }
    }
}