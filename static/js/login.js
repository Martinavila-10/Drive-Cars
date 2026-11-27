
const formulario = document.getElementById("formLogin");

const password = document.getElementById("password");

const mostrarPassword = document.getElementById("mostrarPassword");

if (mostrarPassword && password) {
    mostrarPassword.addEventListener("click", function () {
        if (password.type === "password") {
            password.type = "text";
            mostrarPassword.textContent = "🙈";
        } else {
            password.type = "password";
            mostrarPassword.textContent = "👁";
        }
    });
}

