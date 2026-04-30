from __future__ import annotations


def render_login() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PhishGuard AI - Sign In</title>
  <style>
    :root {
      --bg: #0d1117;
      --panel: rgba(22, 27, 34, 0.97);
      --ink: #e6edf3;
      --muted: #8b949e;
      --accent: #58a6ff;
      --accent-2: #79c0ff;
      --danger: #f85149;
      --safe: #3fb950;
      --border: rgba(240, 246, 252, 0.1);
      --glow: rgba(88, 166, 255, 0.15);
      --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    * { box-sizing: border-box; margin: 0; }
    ::selection { background: rgba(88, 166, 255, 0.3); }
    body {
      font-family: "Space Grotesk", -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
      color: var(--ink);
      background: var(--bg);
      min-height: 100vh;
      display: grid;
      place-items: center;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(88,166,255,0.08), transparent),
        radial-gradient(ellipse 60% 40% at 100% 0%, rgba(136,100,255,0.06), transparent);
    }
    .auth-container {
      position: relative;
      z-index: 1;
      width: 100%;
      max-width: 440px;
      padding: 20px;
    }
    .auth-header {
      text-align: center;
      margin-bottom: 32px;
    }
    .auth-header .brand {
      font-size: 1.4rem;
      font-weight: 800;
      color: var(--accent);
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }
    .auth-header .shield {
      font-size: 3rem;
      margin-bottom: 12px;
    }
    .auth-header h1 {
      font-size: 1.8rem;
      font-weight: 800;
      letter-spacing: -0.04em;
      margin-bottom: 6px;
    }
    .auth-header p {
      color: var(--muted);
      font-size: 0.92rem;
    }
    .auth-card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 28px;
    }
    .tabs {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0;
      margin-bottom: 24px;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--border);
    }
    .tab-btn {
      padding: 12px;
      background: transparent;
      border: none;
      color: var(--muted);
      font-weight: 700;
      font-size: 0.9rem;
      cursor: pointer;
      transition: all var(--transition);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    .tab-btn.active {
      background: rgba(88, 166, 255, 0.08);
      color: var(--accent);
    }
    .tab-btn:hover:not(.active) {
      background: rgba(240, 246, 252, 0.04);
      color: var(--ink);
    }
    .form-group {
      margin-bottom: 16px;
    }
    .form-group label {
      display: block;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 6px;
    }
    .form-group input {
      width: 100%;
      padding: 12px 14px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: rgba(13, 17, 23, 0.8);
      color: var(--ink);
      font: inherit;
      font-size: 0.95rem;
      outline: none;
      transition: border-color var(--transition), box-shadow var(--transition);
    }
    .form-group input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--glow);
    }
    .form-group input::placeholder {
      color: #484f58;
    }
    .submit-btn {
      width: 100%;
      padding: 14px;
      border: none;
      border-radius: 8px;
      background: var(--accent);
      color: #ffffff;
      font-weight: 700;
      font-size: 0.95rem;
      cursor: pointer;
      transition: background var(--transition), box-shadow var(--transition), transform 0.15s ease;
      margin-top: 8px;
    }
    .submit-btn:hover {
      background: #79c0ff;
      box-shadow: 0 4px 16px rgba(88, 166, 255, 0.4);
    }
    .submit-btn:active {
      transform: scale(0.97);
    }
    .submit-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .error-msg {
      color: var(--danger);
      font-size: 0.85rem;
      margin-top: 12px;
      text-align: center;
      min-height: 20px;
    }
    .success-msg {
      color: var(--safe);
      font-size: 0.85rem;
      margin-top: 12px;
      text-align: center;
    }
    .auth-form { display: none; }
    .auth-form.active { display: block; }
    .password-hint {
      font-size: 0.78rem;
      color: #484f58;
      margin-top: 4px;
    }
  </style>
</head>
<body>
  <div class="auth-container">
    <div class="auth-header">
      <div class="shield">&#128737;</div>
      <div class="brand">PhishGuard AI</div>
      <h1>Welcome Back</h1>
      <p>Sign in to access threat intelligence dashboard</p>
    </div>
    <div class="auth-card">
      <div class="tabs">
        <button class="tab-btn active" id="tab-signin" type="button">Sign In</button>
        <button class="tab-btn" id="tab-register" type="button">Register</button>
      </div>

      <form class="auth-form active" id="signin-form">
        <div class="form-group">
          <label for="login-user">Username or Email</label>
          <input id="login-user" type="text" placeholder="Enter username or email" required autocomplete="username" />
        </div>
        <div class="form-group">
          <label for="login-pass">Password</label>
          <input id="login-pass" type="password" placeholder="Enter password" required autocomplete="current-password" />
        </div>
        <button class="submit-btn" type="submit">Sign In</button>
        <div class="error-msg" id="signin-error"></div>
      </form>

      <form class="auth-form" id="register-form">
        <div class="form-group">
          <label for="reg-user">Username</label>
          <input id="reg-user" type="text" placeholder="Choose a username" required autocomplete="username" />
        </div>
        <div class="form-group">
          <label for="reg-email">Email</label>
          <input id="reg-email" type="email" placeholder="you@example.com" required autocomplete="email" />
        </div>
        <div class="form-group">
          <label for="reg-pass">Password</label>
          <input id="reg-pass" type="password" placeholder="Create a password" required autocomplete="new-password" />
          <div class="password-hint">Must be at least 6 characters</div>
        </div>
        <div class="form-group">
          <label for="reg-confirm">Confirm Password</label>
          <input id="reg-confirm" type="password" placeholder="Confirm your password" required autocomplete="new-password" />
        </div>
        <button class="submit-btn" type="submit">Create Account</button>
        <div class="error-msg" id="register-error"></div>
        <div class="success-msg" id="register-success"></div>
      </form>
    </div>
  </div>

  <script>
    const signinForm = document.getElementById("signin-form");
    const registerForm = document.getElementById("register-form");
    const tabSignin = document.getElementById("tab-signin");
    const tabRegister = document.getElementById("tab-register");
    const signinError = document.getElementById("signin-error");
    const registerError = document.getElementById("register-error");
    const registerSuccess = document.getElementById("register-success");

    function switchTab(tab) {
      tabSignin.classList.toggle("active", tab === "signin");
      tabRegister.classList.toggle("active", tab === "register");
      signinForm.classList.toggle("active", tab === "signin");
      registerForm.classList.toggle("active", tab === "register");
      signinError.textContent = "";
      registerError.textContent = "";
      registerSuccess.textContent = "";
    }

    tabSignin.addEventListener("click", () => switchTab("signin"));
    tabRegister.addEventListener("click", () => switchTab("register"));

    signinForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      signinError.textContent = "";
      const username = document.getElementById("login-user").value;
      const password = document.getElementById("login-pass").value;
      try {
        const res = await fetch("/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });
        const body = await res.json();
        if (!res.ok) {
          signinError.textContent = body.detail || "Login failed";
          return;
        }
        window.location.href = "/";
      } catch {
        signinError.textContent = "Connection error. Please try again.";
      }
    });

    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      registerError.textContent = "";
      registerSuccess.textContent = "";
      const username = document.getElementById("reg-user").value;
      const email = document.getElementById("reg-email").value;
      const password = document.getElementById("reg-pass").value;
      const confirm = document.getElementById("reg-confirm").value;
      if (password.length < 6) {
        registerError.textContent = "Password must be at least 6 characters.";
        return;
      }
      if (password !== confirm) {
        registerError.textContent = "Passwords do not match.";
        return;
      }
      try {
        const res = await fetch("/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, email, password }),
        });
        const body = await res.json();
        if (!res.ok) {
          registerError.textContent = body.detail || "Registration failed";
          return;
        }
        registerSuccess.textContent = "Account created! Signing you in...";
        const loginRes = await fetch("/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });
        if (loginRes.ok) {
          window.location.href = "/";
        } else {
          switchTab("signin");
        }
      } catch {
        registerError.textContent = "Connection error. Please try again.";
      }
    });
  </script>
</body>
</html>
"""
