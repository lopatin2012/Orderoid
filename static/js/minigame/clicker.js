let clicks = 0;
let timeLeft = 10;
let gameActive = true;

function clickButton() {
    if (gameActive) {
        clicks++;
        document.getElementById("click-btn").textContent = `Клик! (${clicks})`;
    }
}

function updateTimer() {
    timeLeft--;
    document.getElementById("time").textContent = timeLeft;

    if (timeLeft <= 0) {
        endGame();
    }
}

function endGame() {
    gameActive = false;
    document.getElementById("click-btn").disabled = true;
    document.getElementById("click-btn").style.opacity = 0.6;

    const resultDiv = document.getElementById("result");
    const clicksSpan = document.getElementById("clicks-count");
    const rewardP = document.getElementById("reward");

    clicksSpan.textContent = clicks;

    // Награда
    let rewardExp = 0;
    if (clicks >= 50) {
        rewardExp = 50;
        rewardP.innerHTML = "<strong>Отлично!</strong> +50 опыта!";
    } else if (clicks >= 30) {
        rewardExp = 30;
        rewardP.innerHTML = "Хорошо! +30 опыта!";
    } else if (clicks >= 10) {
        rewardExp = 10;
        rewardP.innerHTML = "Неплохо. +10 опыта.";
    } else {
        rewardP.innerHTML = "Повезёт в следующий раз.";
    }

    // Отправка результата на сервер для получения опыта.
    fetch("/minigame/clicker/submit", { method: "POST", body: JSON.stringify({ clicks }) })

    resultDiv.style.display = "block";
}

// Запуск таймера
setInterval(updateTimer, 1000);