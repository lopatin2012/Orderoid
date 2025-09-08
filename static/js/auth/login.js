// static/js/auth/login.js

document.getElementById("login-form").submit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    const response = await fetch("/users/token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        const { access_token } = await response.json();
        // Сохраняем токен.
        localStorage.setItem("access_token", access_token);
        // Перенаправляем.
        window.location.href = "/";
    } else {
        alert("Ошибка входа");
    }
};