// static/js/character/profile.js

// Показ уведомления.
function showNotification(message, type) {
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Добавление стиля для уведомления. TODO. Подумать над вынесением в общий класс js.
const style = document.createElement("style");
style.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 10px 15px;
        border-radius: 5px;
        color: white;
        font-size: 14px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    }
    .notification.success { background: #27ae60; }
    .notification.error { background: #e74c3c; }
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
`;
document.head.appendChild(style);

// Обновление характеристики.
async function upgradeStat(attr) {
    const button = document.querySelector(`.upgrade[data-stat="${attr}"]`);
    if (button) button.disabled = true;
    try {
        const response = await fetch(`/character/upgrade/${attr}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            // Обновляем значение характеристики
            const valueEl = document.querySelector(`.stat[label='${attr}'] .value`);
            if (valueEl) {
                valueEl.textContent = data.new_value;
            }
            // Обновляем опыт
            updateExperience(data.experience_left);
            showNotification("✅ Характеристика улучшена!", "success");
        } else {
            showNotification("❌ " + (data.detail || "Ошибка"), "error");
        }
    } catch (error) {
        showNotification("⚠️ Ошибка сети", "error");
        console.error("Ошибка сети:", error);
    } finally {
        if (button) button.disabled = false;
    }
}

// Обновить отображение опыта.
function updateExperience(exp) {
    const expEl = document.getElementById("experience-value");
    if (expEl) expEl.textContent = exp;
}