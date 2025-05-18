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
        botao.addEventListener("click", (event) => {
            event.preventDefault(); // Previne o comportamento padrão do formulário
            const id = botao.dataset.id;
            // Adiciona o livro ao carrinho através do formulário
            const form = document.createElement("form");
            form.method = "POST";
            form.action = "/adicionar_carrinho"; 

            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "livro_id";
            input.value = id;

            form.appendChild(input);
            document.body.appendChild(form);
            form.submit();
        });
    });
});