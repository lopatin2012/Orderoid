function upgradeStat(attr) {
    fetch(`/character/upgrade/${attr}`, {
        method: "POST"
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === "success") {
            alert(`Характеристика улучшена! Осталось опыта: ${data.experience_left}`);
            location.reload();
        } else {
            alert("Ошибка: " + data.detail);
        }
    });
}