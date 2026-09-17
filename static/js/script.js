const menuBtn = document.querySelector(".menu-btn");
const menu = document.querySelector(".menu");

if (menuBtn && menu) {
    menuBtn.addEventListener("click", () => {
        menu.classList.toggle("aberto");
    });

    menu.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => menu.classList.remove("aberto"));
    });
}

document.querySelectorAll("[data-copy]").forEach(botao => {
    botao.addEventListener("click", async () => {
        const texto = botao.dataset.copy;
        try {
            await navigator.clipboard.writeText(texto);
            const original = botao.textContent;
            botao.textContent = "Copiado!";
            setTimeout(() => botao.textContent = original, 1600);
        } catch {
            alert("Protocolo: " + texto);
        }
    });
});
