// Sair rápido: troca a página sem deixar o sistema no "voltar" do navegador.
(() => {
  const btn = document.getElementById("sair-rapido");
  if (!btn) return;
  const sair = () => location.replace(btn.href);
  btn.addEventListener("click", (e) => { e.preventDefault(); sair(); });
  let ultimoEsc = 0;
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (Date.now() - ultimoEsc < 600) sair();
    ultimoEsc = Date.now();
  });
})();

// Botões "copiar" ([data-copiar="texto"] ou [data-copiar-de="#id"]).
document.addEventListener("click", async (e) => {
  const b = e.target.closest("[data-copiar], [data-copiar-de]");
  if (!b) return;
  const texto = b.dataset.copiar ?? document.querySelector(b.dataset.copiarDe).innerText.trim();
  try {
    await navigator.clipboard.writeText(texto);
    const antes = b.innerHTML;
    b.innerHTML = '<i class="bi bi-check2"></i> Copiado';
    setTimeout(() => (b.innerHTML = antes), 1500);
  } catch { /* sem permissão de clipboard: o texto continua visível pra copiar na mão */ }
});
