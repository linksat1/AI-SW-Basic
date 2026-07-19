const API_BASE = "/sql-demo/api";

const authSection = document.getElementById("auth-section");
const appSection = document.getElementById("app");
const userBar = document.getElementById("user-bar");
const userBarName = document.getElementById("user-bar-name");
const authTabs = document.getElementById("auth-tabs");
const authHint = document.getElementById("auth-hint");

const views = {
  login: document.getElementById("login-form"),
  register: document.getElementById("register-form"),
  "register-success": document.getElementById("register-success"),
  forgot: document.getElementById("forgot-form"),
  reset: document.getElementById("reset-form"),
};

let lastRegisteredUsername = null;
let lastAttemptedLoginUsername = null;
let resetToken = null;

async function api(path, options = {}) {
  return fetch(`${API_BASE}${path}`, { credentials: "same-origin", ...options });
}

function showAuthView(name) {
  for (const [key, el] of Object.entries(views)) {
    el.classList.toggle("hidden", key !== name);
  }
  authTabs.classList.toggle("hidden", name === "register-success" || name === "reset" || name === "forgot");
  authHint.classList.toggle("hidden", name === "reset");
  if (name === "login" || name === "register") {
    document.querySelectorAll(".auth-tab").forEach((t) => {
      t.classList.toggle("active", t.dataset.tab === name);
    });
  }
}

async function checkAuthAndStart() {
  const params = new URLSearchParams(window.location.search);
  const tokenFromUrl = params.get("token");
  if (tokenFromUrl) {
    resetToken = tokenFromUrl;
    showAuth();
    showAuthView("reset");
    return;
  }

  try {
    const res = await api("/me");
    if (res.ok) {
      const data = await res.json();
      showApp(data.username);
      return;
    }
  } catch (e) {
    // 네트워크 오류 등 -> 로그인 화면으로 폴백
  }
  showAuth();
  showAuthView("login");
}

function showAuth() {
  authSection.classList.remove("hidden");
  appSection.classList.add("hidden");
  userBar.classList.add("hidden");
}

function showApp(username) {
  authSection.classList.add("hidden");
  appSection.classList.remove("hidden");
  userBar.classList.remove("hidden");
  userBarName.textContent = `${username}님`;
  loadQueries();
}

function setupAuthTabs() {
  const tabs = document.querySelectorAll(".auth-tab");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => showAuthView(tab.dataset.tab));
  });
}

function setupLoginForm() {
  const form = document.getElementById("login-form");
  const errorBox = document.getElementById("login-error");
  const resendBox = document.getElementById("login-resend-box");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.textContent = "";
    resendBox.classList.add("hidden");
    const fd = new FormData(form);
    const username = fd.get("username");
    lastAttemptedLoginUsername = username;
    try {
      const res = await api("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password: fd.get("password") }),
      });
      const data = await res.json();
      if (!res.ok) {
        errorBox.textContent = data.detail || "로그인에 실패했습니다.";
        if (res.status === 403) {
          resendBox.classList.remove("hidden");
        }
        return;
      }
      showApp(data.username);
    } catch (err) {
      errorBox.textContent = `요청 실패: ${err}`;
    }
  });

  document.getElementById("login-resend-btn").addEventListener("click", async () => {
    if (!lastAttemptedLoginUsername) return;
    const res = await api("/resend-verification", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: lastAttemptedLoginUsername }),
    });
    const data = await res.json();
    errorBox.textContent = data.message || "";
  });

  document.getElementById("forgot-password-link").addEventListener("click", () => {
    showAuthView("forgot");
  });
}

function setupRegisterForm() {
  const form = document.getElementById("register-form");
  const errorBox = document.getElementById("register-error");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.textContent = "";
    const fd = new FormData(form);
    const password = fd.get("password");
    const password2 = fd.get("password2");
    if (password !== password2) {
      errorBox.textContent = "비밀번호가 서로 다릅니다.";
      return;
    }
    try {
      const res = await api("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: fd.get("username"),
          email: fd.get("email"),
          password,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        errorBox.textContent = data.detail || "회원가입에 실패했습니다.";
        return;
      }
      lastRegisteredUsername = fd.get("username");
      document.getElementById("register-success-text").textContent = data.message;
      form.reset();
      showAuthView("register-success");
    } catch (err) {
      errorBox.textContent = `요청 실패: ${err}`;
    }
  });
}

function setupRegisterSuccess() {
  document.getElementById("resend-btn").addEventListener("click", async () => {
    const errorBox = document.getElementById("resend-error");
    if (!lastRegisteredUsername) return;
    const res = await api("/resend-verification", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: lastRegisteredUsername }),
    });
    const data = await res.json();
    errorBox.textContent = data.message || "";
  });

  document.getElementById("success-back-to-login").addEventListener("click", () => {
    showAuthView("login");
  });
}

function setupForgotForm() {
  const form = document.getElementById("forgot-form");
  const errorBox = document.getElementById("forgot-error");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.textContent = "";
    const fd = new FormData(form);
    try {
      const res = await api("/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: fd.get("email") }),
      });
      const data = await res.json();
      errorBox.textContent = data.message || "";
      errorBox.classList.add("message");
    } catch (err) {
      errorBox.textContent = `요청 실패: ${err}`;
    }
  });

  document.getElementById("forgot-back-to-login").addEventListener("click", () => {
    errorBox.textContent = "";
    errorBox.classList.remove("message");
    showAuthView("login");
  });
}

function setupResetForm() {
  const form = document.getElementById("reset-form");
  const errorBox = document.getElementById("reset-error");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.textContent = "";
    const fd = new FormData(form);
    const password = fd.get("password");
    const password2 = fd.get("password2");
    if (password !== password2) {
      errorBox.textContent = "비밀번호가 서로 다릅니다.";
      return;
    }
    try {
      const res = await api("/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: resetToken, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        errorBox.textContent = data.detail || "비밀번호 재설정에 실패했습니다.";
        return;
      }
      window.history.replaceState({}, "", "/sql-demo/");
      form.reset();
      showAuthView("login");
      document.getElementById("login-error").textContent = "비밀번호가 변경되었습니다. 새 비밀번호로 로그인해주세요.";
    } catch (err) {
      errorBox.textContent = `요청 실패: ${err}`;
    }
  });
}

function setupLogout() {
  document.getElementById("logout-btn").addEventListener("click", async () => {
    await api("/logout", { method: "POST" });
    appSection.innerHTML = '<p id="loading">쿼리 목록을 불러오는 중...</p>';
    showAuth();
    showAuthView("login");
  });
}

async function loadQueries() {
  let queries;
  try {
    const res = await api("/queries");
    if (res.status === 401) {
      showAuth();
      showAuthView("login");
      return;
    }
    queries = await res.json();
  } catch (e) {
    appSection.innerHTML = `<p class="error">쿼리 목록을 불러오지 못했습니다: ${e}</p>`;
    return;
  }

  const categories = [];
  const byCategory = new Map();
  for (const q of queries) {
    if (!byCategory.has(q.category)) {
      byCategory.set(q.category, []);
      categories.push(q.category);
    }
    byCategory.get(q.category).push(q);
  }

  appSection.innerHTML = "";
  for (const category of categories) {
    const section = document.createElement("section");
    section.className = "category";

    const h2 = document.createElement("h2");
    h2.textContent = category;
    section.appendChild(h2);

    for (const q of byCategory.get(category)) {
      section.appendChild(renderQueryCard(q));
    }

    appSection.appendChild(section);
  }
}

function renderQueryCard(q) {
  const card = document.createElement("div");
  card.className = "query-card";

  const desc = document.createElement("p");
  desc.className = "desc";
  desc.textContent = q.description;
  card.appendChild(desc);

  if (q.sql) {
    const pre = document.createElement("pre");
    pre.className = "sql";
    pre.textContent = q.sql;
    card.appendChild(pre);
  }

  const button = document.createElement("button");
  button.className = "run";
  button.textContent = "실행하기";
  card.appendChild(button);

  const resultBox = document.createElement("div");
  resultBox.className = "result";
  card.appendChild(resultBox);

  button.addEventListener("click", async () => {
    button.disabled = true;
    button.textContent = "실행 중...";
    resultBox.innerHTML = "";
    try {
      const res = await api(`/run/${encodeURIComponent(q.id)}`, { method: "POST" });
      if (res.status === 401) {
        showAuth();
        showAuthView("login");
        return;
      }
      const data = await res.json();
      renderResult(resultBox, data);
    } catch (e) {
      resultBox.innerHTML = `<p class="error">요청 실패: ${e}</p>`;
    } finally {
      button.disabled = false;
      button.textContent = "다시 실행";
    }
  });

  return card;
}

function renderResult(box, data) {
  if (data.error) {
    box.innerHTML = `<p class="error">Error: ${escapeHtml(data.error)}</p>`;
    return;
  }
  if (data.message) {
    box.innerHTML = `<p class="message">${escapeHtml(data.message)}</p>`;
    return;
  }
  if (data.columns) {
    if (data.rows.length === 0) {
      box.innerHTML = `<p class="message">결과 0건</p>`;
      return;
    }
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const headRow = document.createElement("tr");
    for (const col of data.columns) {
      const th = document.createElement("th");
      th.textContent = col;
      headRow.appendChild(th);
    }
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    for (const row of data.rows) {
      const tr = document.createElement("tr");
      for (const cell of row) {
        const td = document.createElement("td");
        td.textContent = cell === null ? "NULL" : cell;
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    }
    table.appendChild(tbody);

    box.innerHTML = "";
    box.appendChild(table);
    return;
  }
  box.innerHTML = `<p class="message">완료</p>`;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

setupAuthTabs();
setupLoginForm();
setupRegisterForm();
setupRegisterSuccess();
setupForgotForm();
setupResetForm();
setupLogout();
checkAuthAndStart();
