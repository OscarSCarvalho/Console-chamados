// Console de Chamados — interações do board (drag-and-drop + modal + navegação)

document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card");
  const columnBodies = document.querySelectorAll(".column-body");

  let cardArrastado = null;
  let arrastando = false;

  const podeMover = window.USUARIO_PAPEL !== "solicitante";

  cards.forEach((card) => {
    if (podeMover) {
      card.addEventListener("dragstart", () => {
        cardArrastado = card;
        arrastando = true;
        card.classList.add("dragging");
      });
      card.addEventListener("dragend", () => {
        card.classList.remove("dragging");
        cardArrastado = null;
        setTimeout(() => { arrastando = false; }, 50);
      });
    }
    card.addEventListener("click", () => {
      if (!arrastando) {
        window.location.href = `/chamados/${card.dataset.id}`;
      }
    });
  });

  columnBodies.forEach((body) => {
    const coluna = body.closest(".column");

    if (!podeMover) return;

    body.addEventListener("dragover", (e) => {
      e.preventDefault();
      coluna.classList.add("drag-over");
    });

    body.addEventListener("dragleave", () => {
      coluna.classList.remove("drag-over");
    });

    body.addEventListener("drop", async (e) => {
      e.preventDefault();
      coluna.classList.remove("drag-over");
      if (!cardArrastado) return;

      const novoStatus = body.dataset.status;
      const chamadoId = cardArrastado.dataset.id;
      const colunaOrigemBody = cardArrastado.closest(".column-body");

      if (colunaOrigemBody === body) return;

      body.appendChild(cardArrastado);
      atualizarContadores();

      try {
        const resp = await fetch(`/chamados/${chamadoId}/status`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: novoStatus }),
        });
        if (!resp.ok) throw new Error("Falha ao atualizar status");
        window.location.reload();
      } catch (err) {
        alert("Não foi possível mover o chamado. Tente novamente.");
        window.location.reload();
      }
    });
  });

  function atualizarContadores() {
    document.querySelectorAll(".column").forEach((coluna) => {
      const count = coluna.querySelectorAll(".card").length;
      coluna.querySelector(".col-count").textContent = count;
    });
  }

  // Modal novo chamado
  const modal = document.getElementById("modal-novo");
  const btnAbrir = document.getElementById("btn-novo-chamado");
  const btnCancelar = document.getElementById("btn-cancelar-novo");

  if (btnAbrir) {
    btnAbrir.addEventListener("click", () => modal.classList.add("open"));
  }
  if (btnCancelar) {
    btnCancelar.addEventListener("click", () => modal.classList.remove("open"));
  }
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.classList.remove("open");
    });
  }
});
