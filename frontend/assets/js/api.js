/**
 * api.js — Financiando Sueños
 * Capa de comunicación con el backend FastAPI.
 
 */

const API = "http://localhost:8000";

// ── SESIÓN ────────────────────────────────────────────────────────────────────
const Session = {
  guardar(token, rol, nombre, correo) {
    localStorage.setItem("fs_token",  token);
    localStorage.setItem("fs_rol",    rol);
    localStorage.setItem("fs_nombre", nombre);
    localStorage.setItem("fs_correo", correo);
  },
  token()  { return localStorage.getItem("fs_token");  },
  rol()    { return localStorage.getItem("fs_rol");    },
  nombre() { return localStorage.getItem("fs_nombre"); },
  correo() { return localStorage.getItem("fs_correo"); },
  cerrar() { ["fs_token","fs_rol","fs_nombre","fs_correo"].forEach(k => localStorage.removeItem(k)); },
  activa() { return !!localStorage.getItem("fs_token"); },
  /** Redirige al login si no hay sesión activa */
  requerir() {
    if (!this.activa()) { window.location.href = "login.html"; }
  }
};

// ── REQUEST BASE ──────────────────────────────────────────────────────────────
async function request(method, path, body = null, auth = true) {
  const headers = { "Content-Type": "application/json" };
  if (auth && Session.token()) {
    headers["Authorization"] = "Bearer " + Session.token();
  }
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(API + path, opts);

  // Token expirado → redirigir al login
  if (res.status === 401) {
    Session.cerrar();
    window.location.href = "login.html";
    return;
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Error del servidor" }));
    throw new Error(err.detail || "Error desconocido");
  }

  // Respuestas 204 No Content
  if (res.status === 204) return null;
  return res.json();
}

const get  = (path, auth = true)        => request("GET",    path, null, auth);
const post = (path, body, auth = true)  => request("POST",   path, body, auth);
const put  = (path, body, auth = true)  => request("PUT",    path, body, auth);
const del  = (path, auth = true)        => request("DELETE", path, null, auth);


// ── AUTH ──────────────────────────────────────────────────────────────────────
const Auth = {
  async login(correo, password, rol) {
    const data = await post("/auth/login", { correo, password, rol }, false);
    Session.guardar(data.access_token, data.rol, data.nombre, data.correo);
    return data;
  },
  async recovery(correo) {
    return post("/auth/recovery", { correo }, false);
  },
  logout() {
    Session.cerrar();
    window.location.href = "login.html";
  }
};


// ── ADULTOS MAYORES ───────────────────────────────────────────────────────────
const Adultos = {
  listar(filtros = {}) {
    const params = new URLSearchParams(filtros).toString();
    return get("/adultos/" + (params ? "?" + params : ""));
  },
  obtener(id)     { return get(`/adultos/${id}`); },
  crear(datos)    { return post("/adultos/", datos); },
  actualizar(id, datos) { return put(`/adultos/${id}`, datos); },
  eliminar(id)    { return del(`/adultos/${id}`); },
};


// ── EMPRESAS ──────────────────────────────────────────────────────────────────
const Empresas = {
  listar()        { return get("/empresas/"); },
  obtener(id)     { return get(`/empresas/${id}`); },
  registrar(datos){ return post("/empresas/", datos, false); },  // público
  actualizar(id, datos) { return put(`/empresas/${id}`, datos); },
};


// ── DONACIONES ────────────────────────────────────────────────────────────────
const Donaciones = {
  listar(filtros = {}) {
    const params = new URLSearchParams(filtros).toString();
    return get("/donaciones/" + (params ? "?" + params : ""));
  },
  obtener(id)     { return get(`/donaciones/${id}`); },
  crear(datos)    { return post("/donaciones/", datos); },
  actualizar(id, datos) { return put(`/donaciones/${id}`, datos); },
  eliminar(id)    { return del(`/donaciones/${id}`); },
};


// ── REPORTES ──────────────────────────────────────────────────────────────────
const Reportes = {
  resumen()       { return get("/reportes/resumen"); },
  porMes(anio)    { return get(`/reportes/por-mes?anio=${anio || new Date().getFullYear()}`); },
  porCategoria()  { return get("/reportes/por-categoria"); },
  topEmpresas(n)  { return get(`/reportes/top-empresas?limit=${n || 5}`); },
  porCiudad()     { return get("/reportes/por-ciudad"); },
  urgencia()      { return get("/reportes/urgencia-beneficiarios"); },
};


// ── CERTIFICADOS ──────────────────────────────────────────────────────────────
const Certificados = {
  /** Abre el certificado en una nueva pestaña listo para imprimir/descargar. */
  abrir(donacionId) {
    const url = `${API}/certificados/${donacionId}?token=${Session.token()}`;
    window.open(url, "_blank");
  },
  /** URL del certificado (para iframe o descarga directa). */
  url(donacionId) {
    return `${API}/certificados/${donacionId}`;
  }
};


// ── UTILIDADES UI ─────────────────────────────────────────────────────────────
const UI = {
  _toastTimer: null,

  toast(icon, msg, duracion = 3000) {
    const t   = document.getElementById("toast");
    const ti  = document.getElementById("toastIcon");
    const tm  = document.getElementById("toastMsg");
    if (!t) return;
    if (ti) ti.textContent = icon;
    if (tm) tm.textContent = msg;
    t.classList.add("show");
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => t.classList.remove("show"), duracion);
  },

  toastOk(msg)  { this.toast("✅", msg); },
  toastErr(msg) { this.toast("❌", msg); },
  toastInfo(msg){ this.toast("ℹ️", msg); },

  fmtCOP(v) {
    return "$" + Number(v).toLocaleString("es-CO");
  },

  /** Muestra spinner en un botón mientras espera una promesa. */
  async withLoading(btn, promesa, textoOk = null) {
    const original = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span style="opacity:.6">Cargando…</span>`;
    try {
      const result = await promesa;
      if (textoOk) { btn.innerHTML = textoOk; setTimeout(() => { btn.innerHTML = original; btn.disabled = false; }, 1200); }
      else { btn.innerHTML = original; btn.disabled = false; }
      return result;
    } catch (err) {
      btn.innerHTML = original;
      btn.disabled = false;
      this.toastErr(err.message || "Ocurrió un error");
      throw err;
    }
  },

  /** Llena un <select> con opciones desde un array de objetos. */
  llenarSelect(selectId, items, valKey, labelKey, placeholder = "— Seleccionar —") {
    const sel = document.getElementById(selectId);
    if (!sel) return;
    sel.innerHTML = `<option value="">${placeholder}</option>` +
      items.map(it => `<option value="${it[valKey]}">${it[labelKey]}</option>`).join("");
  },

  /** Iniciales de un nombre completo. */
  initials(nombre = "") {
    return nombre.split(" ").slice(0, 2).map(n => n[0]).join("").toUpperCase();
  }
};
