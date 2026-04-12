const API = "/products";

// --- API helpers ---

async function apiFetch(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  // 204 No Content — тела нет
  if (res.status === 204) return null;
  return res.json().then((data) => ({ ok: res.ok, status: res.status, data }));
}

async function getProducts() {
  const { data } = await apiFetch(API);
  return data;
}

async function createProduct(product) {
  return apiFetch(API, { method: "POST", body: JSON.stringify(product) });
}

async function updateProduct(id, update) {
  return apiFetch(`${API}/${id}`, { method: "PUT", body: JSON.stringify(update) });
}

async function deleteProduct(id) {
  const res = await fetch(`${API}/${id}`, { method: "DELETE" });
  return { ok: res.ok, status: res.status };
}

// --- Render ---

function renderProducts(products) {
  const tbody = document.getElementById("products-body");
  const emptyMsg = document.getElementById("empty-msg");

  tbody.innerHTML = "";

  if (products.length === 0) {
    emptyMsg.style.display = "block";
    return;
  }
  emptyMsg.style.display = "none";

  for (const p of products) {
    const tr = document.createElement("tr");
    tr.dataset.id = p.id;
    tr.dataset.testid = `product-row-${p.id}`;
    tr.innerHTML = `
      <td data-testid="cell-id-${p.id}">${p.id}</td>
      <td data-testid="cell-name-${p.id}">${escapeHtml(p.name)}</td>
      <td data-testid="cell-price-${p.id}">${p.price.toFixed(2)}</td>
      <td class="actions">
        <button class="btn-edit"   data-testid="btn-edit-${p.id}"   data-id="${p.id}">Edit</button>
        <button class="btn-delete" data-testid="btn-delete-${p.id}" data-id="${p.id}">Delete</button>
      </td>
    `;
    tbody.appendChild(tr);
  }
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// --- Load & refresh ---

async function loadProducts() {
  const products = await getProducts();
  renderProducts(products);
}

// --- Add form ---

document.getElementById("add-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorEl = document.getElementById("add-error");
  errorEl.textContent = "";

  const product = {
    id:    parseInt(document.getElementById("input-id").value, 10),
    name:  document.getElementById("input-name").value.trim(),
    price: parseFloat(document.getElementById("input-price").value),
  };

  const result = await createProduct(product);
  if (result.ok) {
    e.target.reset();
    await loadProducts();
  } else {
    errorEl.textContent = result.data?.detail ?? "Error creating product";
  }
});

// --- Delete (делегирование) ---

document.getElementById("products-body").addEventListener("click", async (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;

  const id = parseInt(btn.dataset.id, 10);

  if (btn.classList.contains("btn-delete")) {
    const result = await deleteProduct(id);
    if (result.ok) {
      await loadProducts();
    }
  }

  if (btn.classList.contains("btn-edit")) {
    openEditModal(id);
  }
});

// --- Edit modal ---

function openEditModal(id) {
  const row = document.querySelector(`tr[data-id="${id}"]`);
  const name  = row.querySelector(`[data-testid="cell-name-${id}"]`).textContent;
  const price = row.querySelector(`[data-testid="cell-price-${id}"]`).textContent;

  document.getElementById("edit-id").value    = id;
  document.getElementById("edit-name").value  = name;
  document.getElementById("edit-price").value = price;
  document.getElementById("edit-error").textContent = "";

  document.getElementById("modal-overlay").style.display = "flex";
}

function closeModal() {
  document.getElementById("modal-overlay").style.display = "none";
}

document.getElementById("btn-cancel").addEventListener("click", closeModal);

document.getElementById("modal-overlay").addEventListener("click", (e) => {
  if (e.target === e.currentTarget) closeModal();
});

document.getElementById("edit-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorEl = document.getElementById("edit-error");
  errorEl.textContent = "";

  const id = parseInt(document.getElementById("edit-id").value, 10);
  const update = {
    name:  document.getElementById("edit-name").value.trim(),
    price: parseFloat(document.getElementById("edit-price").value),
  };

  const result = await updateProduct(id, update);
  if (result.ok) {
    closeModal();
    await loadProducts();
  } else {
    errorEl.textContent = result.data?.detail ?? "Error updating product";
  }
});

// --- Init ---
loadProducts();
