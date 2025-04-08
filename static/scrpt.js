const toggleThemeBtn = document.getElementById("toggleTheme");
const body = document.body;

if (toggleThemeBtn) {
    toggleThemeBtn.addEventListener("click", () => {
        body.classList.toggle("dark-theme");
    });
}

// Funcionalidade do carrinho
document.addEventListener("DOMContentLoaded", () => {
    const botoesAdicionar = document.querySelectorAll(".btn-adicionar");

    botoesAdicionar.forEach(botao => {
        botao.addEventListener("click", () => {
            const id = botao.dataset.id;
            window.location.href = `/carrinho/${id}`;
        });
    });
});