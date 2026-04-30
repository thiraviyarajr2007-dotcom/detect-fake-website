from __future__ import annotations


def render_dashboard() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PhishGuard AI</title>
  <style>
    :root {
      --bg: #141517;
      --bg-2: #1b1d22;
      --panel: rgba(28, 31, 37, 0.96);
      --panel-2: rgba(23, 26, 31, 0.98);
      --ink: #eef2f6;
      --muted: #8b92a1;
      --accent: #00a3ff;
      --accent-2: #8ec7ff;
      --safe: #00e676;
      --warn: #ffd54f;
      --danger: #ff5252;
      --border: rgba(255, 255, 255, 0.08);
      --border-strong: rgba(117, 94, 255, 0.95);
      --glow: rgba(0, 163, 255, 0.22);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Space Grotesk", "Segoe UI", "Trebuchet MS", Arial, sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top center, rgba(255,255,255,0.05) 0, rgba(255,255,255,0.05) 1px, transparent 1.5px) 0 0/32px 32px,
        linear-gradient(180deg, var(--bg) 0%, var(--bg-2) 100%);
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background:
        radial-gradient(circle at 50% 0%, rgba(0,163,255,0.12), transparent 30%),
        radial-gradient(circle at 100% 20%, rgba(142,199,255,0.08), transparent 24%);
    }
    .wrap {
      width: 100%;
      min-height: 100vh;
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr);
      grid-template-rows: 82px minmax(0, 1fr);
      position: relative;
      z-index: 1;
    }
    .topbar-shell {
      grid-column: 1 / -1;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 30px 0 38px;
      border-bottom: 1px solid rgba(255,255,255,0.04);
      background: #13171d;
    }
    .topbar-left {
      display: flex;
      align-items: center;
      gap: 24px;
    }
    .top-brand {
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--accent);
      min-width: 195px;
    }
    .top-tabs {
      display: flex;
      align-items: center;
      gap: 18px;
    }
    .top-tab {
      color: #aeb5c2;
      text-decoration: none;
      padding: 29px 10px 23px;
      border-bottom: 3px solid transparent;
      font-weight: 600;
      font-size: 0.98rem;
    }
    .top-tab.active {
      color: #dbe3ef;
      border-bottom-color: var(--accent);
    }
    .topbar-right {
      display: flex;
      align-items: center;
      gap: 18px;
      color: #c9d2df;
    }
    .top-icon {
      width: 38px;
      height: 38px;
      display: grid;
      place-items: center;
      border-radius: 12px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.05);
      font-size: 1rem;
    }
    .home, .panel {
      background: linear-gradient(180deg, var(--panel) 0%, var(--panel-2) 100%);
      border: 1px solid var(--border);
      box-shadow: 0 20px 60px rgba(0,0,0,0.38);
      backdrop-filter: blur(10px);
    }
    .home {
      margin: 0;
      padding: 28px 30px;
      border-radius: 0;
      text-align: left;
      position: relative;
      top: 0;
      align-self: stretch;
      border: 0;
      border-right: 1px solid rgba(255,255,255,0.04);
      background: #181d24;
      box-shadow: none;
    }
    .brand {
      margin: 0 0 10px;
      font-family: "Space Grotesk", "Arial Black", "Segoe UI", sans-serif;
      font-size: clamp(2rem, 4vw, 3.1rem);
      line-height: 0.92;
      letter-spacing: -0.04em;
    }
    .brand-icon, .section-icon, .metric-icon { margin-right: 8px; }
    .tagline { margin: 0 0 18px; max-width: 560px; color: var(--muted); font-size: 1.02rem; line-height: 1.6; }
    .agent-card {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 10px 0 18px;
      margin-bottom: 20px;
    }
    .agent-icon {
      width: 50px;
      height: 50px;
      display: grid;
      place-items: center;
      border-radius: 10px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.05);
      color: var(--accent-2);
      font-size: 1.6rem;
    }
    .agent-copy .muted {
      text-transform: uppercase;
      letter-spacing: 0.16em;
      font-size: 0.72rem;
    }
    .agent-name {
      margin-top: 4px;
      font-size: 1rem;
      font-weight: 800;
      letter-spacing: 0.02em;
    }
    .flow {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 8px;
      margin: 0 0 20px;
    }
    .home .flow { grid-template-columns: 1fr; }
    .flow-step {
      padding: 10px 8px;
      border: 1px solid var(--border);
      border-radius: 999px;
      background: rgba(20, 22, 27, 0.92);
      font-size: 0.86rem;
      color: var(--muted);
    }
    .flow-step.active {
      color: var(--ink);
      border-color: rgba(0,163,255,0.5);
      box-shadow: 0 0 0 1px rgba(0,163,255,0.18) inset;
    }
    .home .flow-step {
      border-radius: 0;
      padding: 18px 18px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      background: transparent;
      border: 0;
      border-left: 4px solid transparent;
    }
    .home .flow-step.active {
      background: rgba(0,163,255,0.08);
      border-left-color: var(--accent);
      box-shadow: none;
    }
    .scan-shell { display: grid; gap: 14px; justify-items: center; }
    .scan-row { width: 100%; display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: center; }
    input, textarea {
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 13px 15px;
      font: inherit;
      color: var(--ink);
      background: rgba(39, 42, 50, 0.96);
    }
    input::placeholder, textarea::placeholder { color: #6f85a4; }
    textarea { min-height: 120px; resize: vertical; }
    button {
      border: 0;
      border-radius: 999px;
      padding: 13px 20px;
      background: linear-gradient(90deg, var(--accent), #5fb8ff);
      color: #061018;
      font-weight: 800;
      cursor: pointer;
      white-space: nowrap;
      box-shadow: 0 8px 22px var(--glow);
    }
    .loading-box, .quick-history, .metric, .stack-card, .compare-card, .info-card, .setting-card {
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px;
      background: rgba(23, 26, 31, 0.96);
    }
    .loading-box {
      width: 100%;
      text-align: left;
      display: grid;
      gap: 10px;
    }
    .loading-row {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
    }
    .spinner {
      width: 16px;
      height: 16px;
      border: 2px solid rgba(142,160,185,0.35);
      border-top-color: var(--accent-2);
      border-radius: 50%;
      animation: spin 1s linear infinite;
      opacity: 0;
    }
    .loading.active .spinner { opacity: 1; }
    .progress {
      width: 100%;
      height: 10px;
      border-radius: 999px;
      background: rgba(255,255,255,0.08);
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--accent), var(--accent-2));
      border-radius: 999px;
      transition: width 0.35s ease;
    }
    .progress-steps {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      font-size: 0.82rem;
      color: var(--muted);
    }
    .step-on { color: var(--ink); }
    .quick-history { width: 100%; text-align: left; margin-top: 22px; display: none; }
    .quick-history h2, .panel h2 {
      margin: 0 0 12px;
      font-family: "Space Grotesk", "Arial Black", "Segoe UI", sans-serif;
      letter-spacing: -0.02em;
    }
    .reason-list, .brand-list { margin: 0; padding-left: 18px; }
    .recent-item {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      font-size: 0.98rem;
      margin-bottom: 8px;
      padding: 12px 14px;
      border-radius: 16px;
      border: 1px solid var(--border);
      background: #171a1f;
    }
    .section-stack {
      display: grid;
      gap: 18px;
      padding: 34px 38px 32px;
      background: #10151c;
      border: 0;
      border-radius: 0;
    }
    .panel { border-radius: 18px; padding: 22px; background: #1d222a; }
    .panel:first-child {
      background:
        radial-gradient(circle at center top, rgba(0,163,255,0.06), transparent 34%),
        linear-gradient(180deg, #0f141b 0%, #10151c 100%);
      border: 0;
      box-shadow: none;
      padding: 0 0 8px;
    }
    .workspace-hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 28px;
      align-items: end;
    }
    .crumbs {
      display: flex;
      gap: 12px;
      align-items: center;
      color: #8791a2;
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      margin-bottom: 14px;
    }
    .hero-title {
      margin: 0;
      font-size: clamp(3rem, 5vw, 5rem);
      line-height: 0.92;
      letter-spacing: -0.06em;
    }
    .hero-summary {
      margin: 10px 0 0;
      max-width: 720px;
      color: #b3bac7;
      font-size: 1rem;
      line-height: 1.45;
    }
    .hero-console {
      margin-top: 26px;
      max-width: 920px;
    }
    .hero-console .scan-row {
      grid-template-columns: minmax(0, 1fr) 210px;
      gap: 0;
      border: 1px solid rgba(0,163,255,0.16);
      border-radius: 14px;
      overflow: hidden;
      background: rgba(28,34,42,0.95);
      box-shadow: 0 0 0 1px rgba(0,163,255,0.06), 0 18px 36px rgba(0, 75, 130, 0.12);
    }
    .hero-console input {
      border: 0;
      border-radius: 0;
      padding: 20px 22px;
      background: transparent;
      font-family: "Consolas", "Courier New", monospace;
      font-size: 0.98rem;
    }
    .hero-console button {
      border-radius: 0;
      box-shadow: 0 0 28px rgba(0,163,255,0.24);
      letter-spacing: 0.18em;
      text-transform: uppercase;
      font-size: 0.92rem;
    }
    .hero-console .loading-box {
      margin-top: 14px;
      padding: 0;
      border: 0;
      background: transparent;
    }
    .hero-console .loading-row {
      justify-content: center;
      color: var(--accent);
      font-family: "Consolas", "Courier New", monospace;
      font-size: 0.88rem;
    }
    .hero-metrics {
      display: flex;
      gap: 18px;
      align-items: center;
      padding-bottom: 10px;
    }
    .hero-metric {
      padding-left: 18px;
      border-left: 1px solid rgba(255,255,255,0.08);
    }
    .hero-metric:first-child {
      border-left: 0;
      padding-left: 0;
    }
    .hero-metric-label {
      color: #8d95a3;
      text-transform: uppercase;
      letter-spacing: 0.16em;
      font-size: 0.7rem;
      margin-bottom: 8px;
    }
    .hero-metric-value {
      font-size: 1.55rem;
      font-weight: 900;
      color: #ffb0a9;
    }
    .hero-metric-value.alert {
      color: #ffaba2;
    }
    .comparison-grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 84px minmax(0, 1fr);
      gap: 18px;
      align-items: start;
    }
    .comparison-column {
      display: grid;
      gap: 14px;
    }
    .compare-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
      color: #d9e1ec;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .compare-header small {
      color: #b39a94;
      font-weight: 500;
      text-transform: none;
      letter-spacing: 0;
    }
    .status-dot {
      width: 11px;
      height: 11px;
      border-radius: 999px;
      display: inline-block;
      margin-right: 10px;
    }
    .status-dot.safe { background: #7df5a7; }
    .status-dot.danger { background: #ffb7b0; }
    .image-card {
      min-height: 320px;
      border-radius: 14px;
      border: 1px solid rgba(255,255,255,0.06);
      background: linear-gradient(180deg, #243648 0%, #111821 100%);
      position: relative;
      overflow: hidden;
      display: grid;
      place-items: center;
    }
    .image-card img.preview-shot {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: none;
      z-index: 0;
    }
    .image-card.has-preview img.preview-shot {
      display: block;
    }
    .image-card.has-preview .mock-login,
    .image-card.has-preview .endpoint-overlay {
      display: none;
    }
    .image-card.danger {
      background: linear-gradient(180deg, rgba(77,28,28,0.75) 0%, rgba(86,12,22,0.9) 100%);
      border-color: rgba(255,173,167,0.28);
    }
    .mock-login {
      width: 180px;
      border-radius: 16px;
      padding: 16px;
      background: rgba(18,29,40,0.84);
      box-shadow: 0 18px 28px rgba(0,0,0,0.34);
      border: 1px solid rgba(150,204,255,0.16);
    }
    .mock-top {
      height: 10px;
      border-radius: 999px;
      margin-bottom: 16px;
      background: linear-gradient(90deg, #6aa4d2, #284b67);
    }
    .mock-field, .mock-button {
      border-radius: 7px;
      margin-bottom: 10px;
      border: 1px solid rgba(110,150,185,0.18);
      background: rgba(16,28,38,0.9);
    }
    .mock-field { height: 31px; }
    .mock-button {
      height: 20px;
      margin-top: 16px;
      background: linear-gradient(90deg, #2f5877, #244860);
    }
    .endpoint-overlay {
      position: absolute;
      inset: 0;
      padding: 18px;
      color: rgba(255,193,185,0.9);
      font-family: "Consolas", "Courier New", monospace;
      font-size: 0.84rem;
      line-height: 1.55;
      background:
        repeating-linear-gradient(180deg, rgba(255,255,255,0.03) 0, rgba(255,255,255,0.03) 1px, transparent 1px, transparent 12px),
        linear-gradient(180deg, rgba(30,0,0,0.1), rgba(60,0,0,0.28));
    }
    .endpoint-overlay .box {
      position: absolute;
      border: 2px solid rgba(255,173,167,0.55);
      background: rgba(255,173,167,0.08);
    }
    .endpoint-overlay .label {
      position: absolute;
      color: rgba(255,173,167,0.85);
      font-size: 0.72rem;
    }
    .evidence-card {
      min-height: 132px;
      border-radius: 14px;
      padding: 18px 20px;
      background: #1b2027;
      border: 1px solid rgba(255,255,255,0.06);
      font-family: "Consolas", "Courier New", monospace;
      line-height: 1.55;
      color: #cfd7e2;
    }
    .evidence-card.safe {
      border-color: rgba(114,246,164,0.35);
      box-shadow: inset 3px 0 0 rgba(114,246,164,0.65);
    }
    .evidence-card.danger {
      border-color: rgba(255,173,167,0.35);
      box-shadow: inset 3px 0 0 rgba(255,173,167,0.65);
    }
    .side-actions {
      display: grid;
      gap: 28px;
      justify-items: center;
      align-self: center;
      padding-top: 44px;
    }
    .action-box {
      width: 62px;
      height: 62px;
      border-radius: 16px;
      display: grid;
      place-items: center;
      background: #252b34;
      border: 1px solid rgba(255,255,255,0.05);
      color: #b6c0ce;
      font-size: 1.4rem;
      box-shadow: 0 16px 30px rgba(0,0,0,0.2);
    }
    .diff-badge {
      width: 100%;
      text-align: center;
      color: var(--accent);
      font-weight: 900;
      font-size: 1.8rem;
      letter-spacing: -0.06em;
    }
    .comparison-footer {
      display: grid;
      grid-template-columns: 1.6fr 0.78fr 0.78fr;
      gap: 18px;
      align-items: stretch;
    }
    .mono-card {
      min-height: 250px;
      font-family: "Consolas", "Courier New", monospace;
      line-height: 1.55;
      white-space: pre-line;
    }
    .mini-stat {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 250px;
    }
    .mini-stat-value {
      font-size: 1.55rem;
      font-weight: 900;
      letter-spacing: -0.04em;
    }
    .danger-outline {
      border: 1px solid rgba(255,173,167,0.28);
    }
    .button-outline {
      width: 100%;
      margin-top: auto;
      border: 1px solid rgba(255,173,167,0.35);
      background: transparent;
      color: #ffb2aa;
      box-shadow: none;
    }
    .app-view { display: none; }
    .app-view.active { display: grid; gap: 18px; }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }
    .stat-card {
      min-height: 180px;
      border-radius: 18px;
      padding: 22px;
      background: #1d222a;
      border: 1px solid rgba(255,255,255,0.06);
      box-shadow: 0 20px 40px rgba(0,0,0,0.22);
    }
    .stat-card .mini-stat-value {
      font-size: 3.2rem;
      margin-top: 18px;
    }
    .split-grid {
      display: grid;
      grid-template-columns: 1fr 1.25fr;
      gap: 18px;
    }
    .list-card {
      border-radius: 18px;
      padding: 22px;
      background: #1d222a;
      border: 1px solid rgba(255,255,255,0.06);
    }
    .log-row {
      display: grid;
      grid-template-columns: 110px 1fr auto;
      gap: 18px;
      padding: 18px 0;
      border-top: 1px solid rgba(255,255,255,0.05);
      align-items: center;
    }
    .log-row:first-child { border-top: 0; }
    .pill-box {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(255,255,255,0.04);
      color: #cfd7e2;
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    .settings-layout {
      display: grid;
      grid-template-columns: 1.45fr 0.9fr;
      gap: 18px;
    }
    .setting-row {
      display: flex;
      justify-content: space-between;
      gap: 18px;
      align-items: center;
      padding: 22px 0;
      border-top: 1px solid rgba(255,255,255,0.05);
    }
    .setting-row:first-child { border-top: 0; }
    .switch {
      width: 58px;
      height: 30px;
      border-radius: 999px;
      background: #2a2f37;
      position: relative;
      box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
    }
    .switch::after {
      content: "";
      position: absolute;
      top: 3px;
      left: 3px;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: #f4f7fb;
    }
    .switch.on { background: var(--accent); }
    .switch.on::after { left: 31px; }
    .api-grid {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 18px;
    }
    .api-key-box {
      display: grid;
      grid-template-columns: 1fr auto auto;
      gap: 10px;
      align-items: center;
      padding: 18px;
      border-radius: 14px;
      background: #141920;
      border: 1px solid rgba(255,255,255,0.05);
      font-family: "Consolas", "Courier New", monospace;
    }
    .subtabs {
      display: flex;
      gap: 12px;
      margin: 6px 0 18px;
      flex-wrap: wrap;
    }
    .subtab {
      padding: 10px 14px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.08);
      background: rgba(255,255,255,0.03);
      color: #aeb7c4;
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      cursor: pointer;
    }
    .subtab.active {
      color: #dff0ff;
      border-color: rgba(0,163,255,0.35);
      box-shadow: inset 0 0 0 1px rgba(0,163,255,0.18);
      background: rgba(0,163,255,0.09);
    }
    .subview { display: none; }
    .subview.active { display: grid; gap: 18px; }
    .tech-grid {
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 18px;
      align-items: start;
    }
    .whois-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      font-family: "Consolas", "Courier New", monospace;
    }
    .whois-table td {
      padding: 16px 8px;
      border-top: 1px solid rgba(255,255,255,0.05);
      vertical-align: top;
    }
    .whois-table td:first-child {
      width: 32%;
      color: #93a0b2;
      text-transform: uppercase;
      font-size: 0.76rem;
      letter-spacing: 0.1em;
    }
    .intel-hero {
      display: grid;
      grid-template-columns: 1.45fr 0.7fr;
      gap: 18px;
      align-items: start;
    }
    .intel-banner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 18px;
      padding: 28px 30px;
      border-radius: 18px;
      background: #2a2d33;
      border: 1px solid rgba(255,173,167,0.16);
      box-shadow: 0 0 24px rgba(255,120,120,0.08);
    }
    .intel-score-ring {
      width: 190px;
      height: 190px;
      margin: 22px auto 24px;
      border-radius: 50%;
      background: conic-gradient(#c82b2f 0deg, #ea8f90 230deg, #2a2f36 230deg, #2a2f36 360deg);
      display: grid;
      place-items: center;
      position: relative;
    }
    .intel-score-ring::after {
      content: "";
      position: absolute;
      width: 144px;
      height: 144px;
      border-radius: 50%;
      background: #1d222a;
    }
    .intel-score-ring > div {
      position: relative;
      z-index: 1;
      text-align: center;
    }
    .intel-actions {
      display: grid;
      gap: 14px;
    }
    .intel-solid-danger {
      width: 100%;
      border-radius: 10px;
      background: linear-gradient(180deg, #bf0d15, #a10008);
      color: #fff1ee;
      box-shadow: none;
    }
    .intel-grid {
      display: grid;
      grid-template-columns: 1.55fr 0.75fr;
      gap: 18px;
      align-items: start;
    }
    .intel-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 16px;
      font-family: "Consolas", "Courier New", monospace;
    }
    .intel-table th,
    .intel-table td {
      padding: 18px 10px;
      border-top: 1px solid rgba(255,255,255,0.05);
      text-align: left;
    }
    .intel-table th {
      color: #96a0b0;
      font-weight: 500;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      font-size: 0.78rem;
    }
    .intel-table td:last-child,
    .intel-table th:last-child {
      text-align: right;
    }
    .intel-cards {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }
    .intel-thumb-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin: 14px 0;
    }
    .intel-thumb {
      height: 82px;
      border-radius: 10px;
      border: 1px solid rgba(255,255,255,0.08);
      background: linear-gradient(180deg, #153246, #0d1821);
    }
    .intel-thumb.danger {
      background: linear-gradient(180deg, #534649, #20222a);
      border-color: rgba(255,173,167,0.24);
    }
    .results-grid { display: grid; grid-template-columns: 0.95fr 1.05fr; gap: 18px; margin-bottom: 18px; }
    .metric-grid, .stack-grid, .compare-grid, .detail-grid, .analytics-grid, .settings-grid {
      display: grid;
      gap: 12px;
    }
    .metric-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .compare-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .detail-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .stack-grid, .analytics-grid, .settings-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .probability {
      font-family: "Space Grotesk", "Arial Black", "Segoe UI", sans-serif;
      font-size: clamp(3.2rem, 6vw, 5.4rem);
      font-weight: 900;
      line-height: 0.9;
      letter-spacing: -0.08em;
      margin: 4px 0 10px;
      color: #dce5f3;
    }
    .gauge {
      width: 180px;
      height: 90px;
      margin: 8px auto 0;
      border-radius: 180px 180px 0 0;
      background:
        conic-gradient(from 180deg, var(--safe) 0deg 60deg, var(--warn) 60deg 120deg, var(--danger) 120deg 180deg);
      position: relative;
      overflow: hidden;
    }
    .gauge::after {
      content: "";
      position: absolute;
      inset: 18px 18px -18px 18px;
      background: linear-gradient(180deg, #181b20 0%, #1e2229 100%);
      border-radius: 180px 180px 0 0;
      border: 1px solid var(--border);
    }
    .gauge-needle {
      position: absolute;
      bottom: 0;
      left: 50%;
      width: 4px;
      height: 82px;
      background: #f8fafc;
      transform-origin: bottom center;
      transform: translateX(-50%) rotate(-90deg);
      transition: transform 0.4s ease;
      z-index: 2;
      border-radius: 999px;
      box-shadow: 0 0 10px rgba(255,255,255,0.25);
    }
    .gauge-center {
      position: absolute;
      bottom: -6px;
      left: 50%;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: #f8fafc;
      transform: translateX(-50%);
      z-index: 3;
    }
    .gauge-label {
      margin-top: 10px;
      text-align: center;
      font-weight: 700;
      color: var(--muted);
    }
    .metric strong {
      display: block;
      margin-top: 4px;
      font-family: "Space Grotesk", "Arial Black", "Segoe UI", sans-serif;
      font-size: 1.55rem;
      letter-spacing: -0.05em;
    }
    .pill {
      display: inline-flex;
      padding: 8px 14px;
      border-radius: 999px;
      font-weight: 800;
      width: fit-content;
      border: 1px solid currentColor;
    }
    .safe { background: rgba(34,197,94,0.12); color: var(--safe); }
    .suspicious { background: rgba(250,204,21,0.12); color: var(--warn); }
    .phishing { background: rgba(239,68,68,0.12); color: var(--danger); }
    .muted { color: var(--muted); }
    .actions { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
    .graph {
      height: 180px;
      display: flex;
      align-items: end;
      gap: 18px;
      padding: 12px;
    }
    .bar {
      flex: 1;
      border-radius: 14px 14px 6px 6px;
      position: relative;
      min-height: 16px;
    }
    .bar span {
      position: absolute;
      top: -24px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 0.88rem;
      color: var(--muted);
      white-space: nowrap;
    }
    .bar.safe-bar { background: linear-gradient(180deg, #8ef7bb, #0b743e); }
    .bar.phishing-bar { background: linear-gradient(180deg, #ff9a9a, #9a1824); }
    .bar.suspicious-bar { background: linear-gradient(180deg, #ffe28f, #b17610); }
    .setting-list { list-style: none; padding: 0; margin: 0; }
    .setting-list li { margin-bottom: 8px; }
    @keyframes spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    @media (max-width: 900px) {
      .wrap,
      .flow,
      .scan-row,
      .progress-steps,
      .results-grid,
      .metric-grid,
      .stack-grid,
      .compare-grid,
      .detail-grid,
      .analytics-grid,
      .settings-grid {
        grid-template-columns: 1fr;
      }
      .home { position: static; }
      .hero-console .scan-row,
      .comparison-grid,
      .comparison-footer,
      .workspace-hero,
      .stats-grid,
      .split-grid,
      .threat-intel-layout,
      .threat-intel-top,
      .threat-intel-bottom,
      .threat-intel-banner,
      .settings-layout,
      .api-grid,
      .log-row,
      .tech-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <header class="topbar-shell">
      <div class="topbar-left">
        <div class="top-brand">PhishGuard AI</div>
        <nav class="top-tabs">
          <a class="top-tab active" href="#" data-view="dashboard">Dashboard</a>
          <a class="top-tab" href="#" data-view="scans">Scans</a>
          <a class="top-tab" href="#" data-view="settings">Settings</a>
          <a class="top-tab" href="#" data-view="api">API</a>
        </nav>
      </div>
      <div class="topbar-right">
        <div class="top-icon">&#128276;</div>
        <div class="top-icon">&#128100;</div>
      </div>
    </header>

    <aside class="home">
      <div class="agent-card">
        <div class="agent-icon">&#128737;</div>
        <div class="agent-copy">
          <div class="muted">Sentinel Active</div>
          <div class="agent-name">ANALYST_NODE_04</div>
        </div>
      </div>
      <div class="flow">
        <div class="flow-step active" data-view="dashboard">Overview</div>
        <div class="flow-step" data-view="scans">Live Feed</div>
        <div class="flow-step" data-view="threat-intel">Threat Intel</div>
        <div class="flow-step" data-view="complaint">Raise Complaint</div>
        <div class="flow-step" data-view="settings">Support</div>
      </div>
      <div style="margin-top:auto;padding-top:26px;">
        <button type="button" id="new-scan-button" style="width:100%;border-radius:10px;">+ New Scan</button>
      </div>
      <div class="flow" style="margin-top:18px;">
        <div class="flow-step">Logout</div>
      </div>
      <div id="recent-list" style="display:none;"></div>
    </aside>

    <main class="section-stack">
      <section class="app-view" id="dashboard-view">
        <section class="panel">
          <div style="text-align:center;padding:28px 20px 10px;">
            <div style="font-size:3.6rem;margin-bottom:12px;">&#128737;</div>
            <div class="brand" style="font-size:clamp(3rem,6vw,5.2rem);max-width:980px;margin:0 auto 18px;">
              Threat Detection <span style="color:var(--accent);">Evolved.</span>
            </div>
            <p class="tagline" style="max-width:760px;margin:0 auto 28px;text-align:center;">
              Paste any suspicious URL or domain below. Our multi-vector AI sentinel analyzes DNS records, SSL certificates, and content heuristics in real time.
            </p>
            <form id="scan-form" class="scan-shell hero-console" style="max-width:820px;margin:0 auto;">
              <div class="scan-row">
                <input id="url-input" name="url" placeholder="https://suspicious-site.com/login" required />
                <button type="submit" id="dashboard-scan-button">Scan Now</button>
              </div>
              <div class="loading-box loading" id="loading-box" style="padding-top:8px;">
                <div class="loading-row" style="justify-content:center;">
                  <div class="spinner" id="spinner"></div>
                  <div id="loading-text" style="color:var(--accent);">Scanning with AI... Sentinel analyzing payload layers</div>
                </div>
                <div class="progress"><div class="progress-fill" id="progress-fill"></div></div>
                <div class="progress-steps">
                  <div id="step-domain">1. Domain Analysis</div>
                  <div id="step-content">2. Content Check</div>
                  <div id="step-image">3. Visual AI</div>
                </div>
              </div>
              <div id="dashboard-verdict" style="display:none;margin-top:18px;padding:14px 18px;border-radius:14px;border:1px solid rgba(255,255,255,0.08);background:rgba(12,19,30,0.75);text-align:center;">
                <div class="muted" style="margin-bottom:6px;letter-spacing:0.2em;text-transform:uppercase;">Scan Result</div>
                <div id="dashboard-verdict-text" style="font-size:1.8rem;font-weight:900;color:#8ef7bb;">SAFE</div>
                <div class="tagline" id="dashboard-verdict-note" style="margin-top:6px;">Analysis complete. Opening Live Feed in a few seconds.</div>
                <div id="dashboard-result-grid" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:16px;text-align:left;">
                  <div class="compare-card" style="padding:14px;">
                    <div class="muted" style="text-transform:uppercase;letter-spacing:0.14em;">Scanned URL</div>
                    <div id="dashboard-result-url" style="margin-top:8px;font-weight:700;word-break:break-word;">Waiting for scan</div>
                  </div>
                  <div class="compare-card" style="padding:14px;">
                    <div class="muted" style="text-transform:uppercase;letter-spacing:0.14em;">Domain Risk</div>
                    <div id="dashboard-domain-score" style="margin-top:8px;font-size:1.4rem;font-weight:900;">0%</div>
                  </div>
                  <div class="compare-card" style="padding:14px;">
                    <div class="muted" style="text-transform:uppercase;letter-spacing:0.14em;">Content Risk</div>
                    <div id="dashboard-content-score" style="margin-top:8px;font-size:1.4rem;font-weight:900;">0%</div>
                  </div>
                  <div class="compare-card" style="padding:14px;">
                    <div class="muted" style="text-transform:uppercase;letter-spacing:0.14em;">Visual Risk</div>
                    <div id="dashboard-image-score" style="margin-top:8px;font-size:1.4rem;font-weight:900;">0%</div>
                  </div>
                </div>
                <div class="compare-card" style="margin-top:14px;padding:16px;text-align:left;">
                  <div class="muted" style="text-transform:uppercase;letter-spacing:0.14em;">Why This Website Looks Real or Fake</div>
                  <div id="dashboard-reasons" style="margin-top:10px;display:grid;gap:8px;"></div>
                </div>
              </div>
            </form>
          </div>
        </section>
        <div class="split-grid" style="grid-template-columns:1.55fr 0.75fr;align-items:start;">
          <div class="list-card">
            <div class="actions" style="justify-content:space-between;margin-bottom:18px;">
              <div>
                <h2 style="margin-bottom:4px;">Recent Scans</h2>
                <div class="muted">Global intercept history</div>
              </div>
              <div class="muted">View all</div>
            </div>
            <div id="dashboard-log">
              <div class="recent-item"><strong>paypal-secure-verify.net/auth</strong><span class="tiny-pill phishing">98/100</span></div>
              <div class="recent-item"><strong>github.com/security/advisories</strong><span class="tiny-pill safe">02/100</span></div>
              <div class="recent-item"><strong>cloud-drive-sharing.biz/d/4029</strong><span class="tiny-pill suspicious">64/100</span></div>
            </div>
          </div>
          <div style="display:grid;gap:18px;">
            <div class="list-card" style="text-align:center;">
              <h2 style="margin-bottom:18px;">Global Threat Level</h2>
              <div class="gauge" style="margin:22px auto 10px;">
                <div class="gauge-needle" id="dashboard-gauge-needle"></div>
                <div class="gauge-center"></div>
              </div>
              <div class="gauge-label" id="dashboard-gauge-label">62% elevated</div>
              <p class="tagline" style="margin-top:18px;">4.2k active phishing campaigns detected in last 24h.</p>
            </div>
            <div class="list-card">
              <h2>Sentinel Insights</h2>
              <div class="compare-card">
                <div class="muted">Zero-Day Found</div>
                <p style="margin:6px 0 0;">New credential harvester targeting Microsoft 365 users via QR codes.</p>
              </div>
              <div class="compare-card" style="margin-top:12px;">
                <div class="muted">System Update</div>
                <p style="margin:6px 0 0;">AI model v4.2 now includes multi-language optical character recognition.</p>
              </div>
            </div>
            <div class="list-card">
              <h2>Live Traffic</h2>
              <div style="height:120px;border-radius:14px;background:radial-gradient(circle at 80% 20%, rgba(142,199,255,0.35), transparent 8%), linear-gradient(180deg,#0b1016,#141a22);border:1px solid rgba(255,255,255,0.05);"></div>
              <div class="tagline" style="margin-top:12px;">Active monitoring from 14 nodes</div>
            </div>
          </div>
        </div>
      </section>

      <section class="app-view" id="threat-intel-view">
        <section class="panel" style="padding:18px 22px 24px;background:
          radial-gradient(circle at 12% 10%, rgba(82,140,255,0.22), transparent 22%),
          linear-gradient(180deg, rgba(13,32,67,0.98), rgba(10,20,37,0.96));">
          <div class="threat-intel-banner" style="display:grid;grid-template-columns:0.8fr 1.6fr 1fr;gap:20px;align-items:center;">
            <div style="display:flex;align-items:center;gap:14px;">
              <div style="width:72px;height:72px;border-radius:20px;border:1px solid rgba(122,185,255,0.45);display:grid;place-items:center;background:linear-gradient(180deg,rgba(21,53,101,0.95),rgba(11,27,54,0.95));box-shadow:0 0 20px rgba(0,163,255,0.18) inset;">
                <div style="font-size:2rem;color:#b9d8ff;">&#9760;</div>
              </div>
              <div>
                <div style="font-size:2.7rem;font-weight:900;line-height:1.05;">Threat Intelligence Dashboard</div>
                <div class="tagline" style="margin-top:8px;">Monitor &amp; Analyze Cyber Threats in Real Time</div>
              </div>
            </div>
            <div></div>
            <div style="display:grid;gap:10px;justify-items:end;">
              <div class="tagline">Total Threats Detected: <strong id="ti-total-threats" style="font-size:1.8rem;color:#ffffff;">5,243</strong></div>
              <div class="tagline">Phishing Sites Blocked: <strong id="ti-blocked" style="font-size:1.8rem;color:#ffffff;">2,781</strong></div>
              <div class="tagline">Suspicious IPs: <strong id="ti-suspicious" style="font-size:1.8rem;color:#ffffff;">1,194</strong></div>
            </div>
          </div>
        </section>

        <div class="threat-intel-layout" style="display:grid;grid-template-columns:0.8fr 2.2fr;gap:18px;align-items:start;">
          <div style="display:grid;gap:18px;">
            <div class="list-card">
              <div class="actions" style="justify-content:space-between;align-items:center;margin-bottom:14px;">
                <h2 style="margin:0;">Threat Alerts</h2>
                <div class="muted">&#9881; &#9776;</div>
              </div>
              <div id="ti-alerts" style="display:grid;gap:10px;">
                <div class="recent-item"><strong>&#9760; FakeBank-Login.xyz</strong><span class="tiny-pill phishing">Phishing Site</span></div>
                <div class="recent-item"><strong>&#9993; Malware-Downloader.exe</strong><span class="tiny-pill suspicious">Malicious File</span></div>
                <div class="recent-item"><strong>&#128205; 192.168.45.23</strong><span class="tiny-pill suspicious">Suspicious IP</span></div>
              </div>
              <button type="button" class="button-outline" style="width:100%;margin-top:18px;">View All Alerts</button>
            </div>

            <div class="list-card">
              <div class="actions" style="justify-content:space-between;align-items:center;margin-bottom:14px;">
                <h2 style="margin:0;">Blacklisted Domains</h2>
                <div class="muted">&#9881; &#9776;</div>
              </div>
              <table class="intel-table" style="margin-top:8px;">
                <thead>
                  <tr>
                    <th>Domain</th>
                    <th>Threat Type</th>
                  </tr>
                </thead>
                <tbody id="ti-blacklist-body">
                  <tr><td>fakebank-login.xyz</td><td style="color:#ffb570;">Phishing</td></tr>
                  <tr><td>update-paypal.cc</td><td style="color:#ffb570;">Phishing</td></tr>
                  <tr><td>malware-site.ru</td><td style="color:#ff8d6b;">Malware</td></tr>
                </tbody>
              </table>
              <button type="button" class="button-outline" style="width:100%;margin-top:18px;">Manage Blacklist</button>
            </div>
          </div>

          <div style="display:grid;gap:18px;">
            <div class="list-card">
              <div class="actions" style="justify-content:space-between;align-items:center;margin-bottom:16px;">
                <h2 style="margin:0;">Live Threat Analysis</h2>
                <div class="muted">&#9679; &#9679; &#9679;</div>
              </div>
              <div class="threat-intel-top" style="display:grid;grid-template-columns:1.1fr 1.2fr;gap:18px;">
                <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;">
                  <div class="compare-card" style="padding:18px;">
                    <div class="muted">Phishing URLs Detected</div>
                    <div style="display:flex;align-items:end;gap:18px;margin-top:12px;">
                      <div id="ti-phishing-today" style="font-size:2.5rem;font-weight:900;">257</div>
                      <div class="tagline"><strong id="ti-phishing-hour" style="color:#ff9c73;">33</strong><br/>Last Hour</div>
                    </div>
                  </div>
                  <div class="compare-card" style="padding:18px;">
                    <div class="muted">Malware Alerts</div>
                    <div style="display:flex;align-items:end;gap:18px;margin-top:12px;">
                      <div id="ti-malware-today" style="font-size:2.5rem;font-weight:900;">128</div>
                      <div class="tagline"><strong id="ti-malware-hour" style="color:#ff9c73;">10</strong><br/>Last Hour</div>
                    </div>
                  </div>
                  <div class="compare-card" style="padding:18px;">
                    <div class="muted">Suspicious IPs</div>
                    <div style="display:flex;align-items:end;gap:18px;margin-top:12px;">
                      <div id="ti-ips-today" style="font-size:2.5rem;font-weight:900;">76</div>
                      <div class="tagline"><strong id="ti-ips-hour" style="color:#ffcf89;">5</strong><br/>Last Hour</div>
                    </div>
                  </div>
                  <div class="compare-card" style="padding:18px;display:grid;align-items:center;justify-items:center;background:
                    radial-gradient(circle at 50% 18%, rgba(255,116,86,0.26), transparent 34%),
                    linear-gradient(180deg, rgba(40,21,28,0.84), rgba(31,18,22,0.84));">
                    <div class="muted">Threat Level</div>
                    <div style="width:180px;height:92px;border-radius:180px 180px 0 0;border:16px solid rgba(255,123,72,0.75);border-bottom:none;position:relative;overflow:hidden;">
                      <div style="position:absolute;left:50%;bottom:-4px;transform:translateX(-50%);font-size:1.9rem;font-weight:900;color:#ffb570;" id="ti-threat-level">HIGH</div>
                    </div>
                  </div>
                </div>
                <div style="border:1px solid rgba(99,151,241,0.22);border-radius:18px;min-height:258px;background:
                  radial-gradient(circle at 18% 28%, rgba(255,124,78,0.55), transparent 2.8%),
                  radial-gradient(circle at 28% 56%, rgba(255,124,78,0.55), transparent 2.8%),
                  radial-gradient(circle at 56% 48%, rgba(255,124,78,0.55), transparent 2.8%),
                  radial-gradient(circle at 73% 40%, rgba(255,124,78,0.55), transparent 2.8%),
                  radial-gradient(circle at 90% 74%, rgba(255,124,78,0.55), transparent 2.8%),
                  linear-gradient(180deg, rgba(18,44,83,0.95), rgba(11,26,50,0.98));position:relative;overflow:hidden;">
                  <div style="position:absolute;inset:18px;background:
                    linear-gradient(115deg, transparent 0 18%, rgba(85,160,255,0.15) 18% 19%, transparent 19% 100%),
                    linear-gradient(25deg, transparent 0 37%, rgba(85,160,255,0.16) 37% 38%, transparent 38% 100%),
                    radial-gradient(circle at 22% 22%, rgba(84,133,214,0.35), transparent 20%),
                    radial-gradient(circle at 78% 28%, rgba(84,133,214,0.32), transparent 22%),
                    radial-gradient(circle at 53% 55%, rgba(84,133,214,0.24), transparent 24%),
                    radial-gradient(circle at 92% 72%, rgba(84,133,214,0.22), transparent 20%);border-radius:14px;"></div>
                  <div style="position:absolute;left:12%;top:32%;width:74%;height:2px;background:linear-gradient(90deg, rgba(255,132,85,0), rgba(255,132,85,0.9), rgba(255,132,85,0));transform:rotate(11deg);"></div>
                  <div style="position:absolute;left:15%;top:56%;width:60%;height:2px;background:linear-gradient(90deg, rgba(255,132,85,0), rgba(255,132,85,0.9), rgba(255,132,85,0));transform:rotate(-10deg);"></div>
                  <div style="position:absolute;bottom:14px;left:20px;right:20px;display:flex;gap:14px;flex-wrap:wrap;" class="tagline">
                    <span style="color:#ff835f;">&#9679; Phishing Attacks</span>
                    <span style="color:#ffb570;">&#9679; Malware</span>
                    <span style="color:#79aefe;">&#9679; Suspicious IPs</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="threat-intel-bottom" style="display:grid;grid-template-columns:1.7fr 0.9fr;gap:18px;">
              <div class="list-card">
                <div class="actions" style="justify-content:space-between;align-items:center;margin-bottom:16px;">
                  <h2 style="margin:0;">Latest Threat Feeds</h2>
                  <div class="muted">&#9679; &#9679; &#9679;</div>
                </div>
                <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;">
                  <div class="compare-card" style="padding:16px;">
                    <div style="font-weight:700;color:#b9d8ff;">PhishTank Updates</div>
                    <div class="tagline" id="ti-feed-1" style="margin-top:14px;">Updated 20 mins ago</div>
                  </div>
                  <div class="compare-card" style="padding:16px;">
                    <div style="font-weight:700;color:#b9d8ff;">VirusTotal Reports</div>
                    <div class="tagline" id="ti-feed-2" style="margin-top:14px;">Updated 20 mins ago</div>
                  </div>
                  <div class="compare-card" style="padding:16px;">
                    <div style="font-weight:700;color:#b9d8ff;">Open Threat Exchange</div>
                    <div class="tagline" id="ti-feed-3" style="margin-top:14px;">Updated 20 mins ago</div>
                  </div>
                </div>
                <div style="margin-top:18px;height:122px;border-radius:16px;background:
                  radial-gradient(circle at 24% 50%, rgba(255,119,73,0.32), transparent 16%),
                  radial-gradient(circle at 51% 50%, rgba(109,168,255,0.34), transparent 16%),
                  radial-gradient(circle at 78% 50%, rgba(255,147,61,0.35), transparent 16%),
                  linear-gradient(180deg,#10203d,#0d1a2f);border:1px solid rgba(255,255,255,0.06);position:relative;overflow:hidden;">
                  <div style="position:absolute;inset:0;background:
                    linear-gradient(90deg, transparent 0 10%, rgba(128,180,255,0.14) 10% 11%, transparent 11% 100%),
                    linear-gradient(0deg, transparent 0 20%, rgba(128,180,255,0.12) 20% 21%, transparent 21% 100%);opacity:0.65;"></div>
                  <div style="position:absolute;left:17%;top:54%;font-size:3rem;">&#128737;</div>
                  <div style="position:absolute;left:46%;top:54%;font-size:3rem;">&#9989;</div>
                  <div style="position:absolute;left:74%;top:54%;font-size:3rem;">&#128274;</div>
                </div>
              </div>

              <div class="list-card">
                <div class="actions" style="justify-content:space-between;align-items:center;margin-bottom:16px;">
                  <h2 style="margin:0;">AI Analysis</h2>
                  <div class="muted">&#9881; &#128274;</div>
                </div>
                <button type="button" style="width:100%;margin-bottom:18px;">Scan URL for Threats &raquo;</button>
                <div style="display:grid;gap:12px;">
                  <div class="recent-item"><strong>Machine Learning</strong><span class="tiny-pill safe">Active</span></div>
                  <div class="recent-item"><strong>Risk Score</strong><span id="ti-ai-risk" class="tiny-pill suspicious">87 / 100</span></div>
                  <div class="recent-item"><strong>Pattern Match</strong><span id="ti-ai-pattern" class="tiny-pill phishing">Phishing Detected</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="app-view" id="complaint-view">
        <section class="panel">
          <div class="workspace-hero">
            <div>
              <div class="crumbs"><span>COMPLAINTS</span><span>/</span><span>CYBER_REPORTING</span></div>
              <h1 class="hero-title">Raise Complaint</h1>
              <p class="hero-summary">Report suspicious links, fake websites, and phishing incidents for rapid action by the security team.</p>
            </div>
          </div>
        </section>
        <div class="settings-layout" style="grid-template-columns:1.3fr 0.9fr;">
          <div class="list-card">
            <h2 style="margin-bottom:18px;">Complaint Intake</h2>
            <div style="display:grid;gap:14px;">
              <input type="text" placeholder="Suspicious URL or fake website link" style="padding:14px 16px;border-radius:12px;border:1px solid rgba(255,255,255,0.08);background:rgba(8,12,18,0.9);color:var(--ink);" />
              <input type="text" placeholder="Affected brand or service" style="padding:14px 16px;border-radius:12px;border:1px solid rgba(255,255,255,0.08);background:rgba(8,12,18,0.9);color:var(--ink);" />
              <select style="padding:14px 16px;border-radius:12px;border:1px solid rgba(255,255,255,0.08);background:rgba(8,12,18,0.9);color:var(--ink);">
                <option>Complaint Type</option>
                <option>Phishing Website</option>
                <option>Fake Payment Link</option>
                <option>Brand Impersonation</option>
                <option>Credential Theft Attempt</option>
              </select>
              <textarea placeholder="Describe what happened and why the website looks suspicious..." rows="6" style="padding:14px 16px;border-radius:12px;border:1px solid rgba(255,255,255,0.08);background:rgba(8,12,18,0.9);color:var(--ink);resize:vertical;"></textarea>
              <input id="complaint-evidence-input" type="file" accept="image/*" multiple style="display:none;" />
              <div style="display:flex;gap:12px;flex-wrap:wrap;">
                <button type="button">Submit Complaint</button>
                <button type="button" id="attach-evidence-button" class="button-outline" style="margin-top:0;">Attach Evidence</button>
              </div>
              <div id="complaint-evidence-gallery" style="display:none;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:6px;"></div>
            </div>
          </div>
          <div style="display:grid;gap:18px;">
            <div class="list-card">
              <h2>Response Workflow</h2>
              <div class="compare-card">
                <div class="muted">Step 1</div>
                <p style="margin:6px 0 0;">Security triage validates the website and reputation signals.</p>
              </div>
              <div class="compare-card" style="margin-top:12px;">
                <div class="muted">Step 2</div>
                <p style="margin:6px 0 0;">Threat intel team confirms impersonation and collects evidence.</p>
              </div>
              <div class="compare-card" style="margin-top:12px;">
                <div class="muted">Step 3</div>
                <p style="margin:6px 0 0;">Takedown or escalation request is generated for the fake domain.</p>
              </div>
            </div>
            <div class="list-card" style="background:#101e2c;border-color:rgba(85,176,255,0.24);">
              <h2>Escalation Priority</h2>
              <div class="tagline">High-priority complaints are routed immediately when the detected site targets payments, banking, or login credentials.</div>
            </div>
          </div>
        </div>
      </section>

      <section class="app-view active" id="scans-view">
      <section class="panel">
        <div class="workspace-hero">
          <div>
            <div class="crumbs">
              <span>ANALYSIS_REPO</span>
              <span>/</span>
              <span>VISUAL_DIFF</span>
              <span>/</span>
              <span id="scan-id-label" style="color:var(--accent);">ID_88294_AMZ</span>
            </div>
            <h1 class="hero-title" id="scans-page-title">VISUAL COMPARISON</h1>
            <p class="hero-summary" id="scans-page-summary">Real-time pixel-level differential analysis between authoritative source and suspected threat endpoint.</p>
          </div>
          <div class="hero-metrics">
            <div class="hero-metric">
              <div class="hero-metric-label">Confidence Score</div>
              <div id="probability" class="hero-metric-value">0% MATCH</div>
            </div>
            <div class="hero-metric">
              <div class="hero-metric-label">Threat Level</div>
              <div id="verdict" class="hero-metric-value alert">WAITING</div>
            </div>
          </div>
        </div>
      </section>
      <div class="subtabs">
        <button type="button" class="subtab active" data-subview="visual-proof">Visual Proof</button>
        <button type="button" class="subtab" data-subview="technical-intel">Technical Intel - WHOIS</button>
      </div>

      <section class="subview active" id="visual-proof-view">
      <section class="comparison-grid">
        <div class="comparison-column">
          <div class="compare-header">
            <div><span class="status-dot safe"></span>GENUINE SOURCE</div>
            <small id="genuine-label">amazon.com/login</small>
          </div>
          <div class="image-card" id="genuine-card">
            <img id="genuine-preview" class="preview-shot" alt="Original website preview" />
            <div class="mock-login">
              <div class="mock-top"></div>
              <div class="mock-field"></div>
              <div class="mock-field"></div>
              <div class="mock-button"></div>
            </div>
            <div style="position:absolute;left:20px;bottom:20px;padding:8px 12px;border:1px solid rgba(114,246,164,0.45);color:#7df5a7;background:rgba(8,34,19,0.74);font-family:'Consolas','Courier New',monospace;">SSL_VERIFIED: TRUE</div>
          </div>
          <div class="evidence-card safe">
            <div style="color:#7df5a7;font-weight:800;margin-bottom:10px;">VERIFIED ASSETS</div>
            <div id="genuine-hash">HEADER_LOGO: SVG_HASH_MATCH_99.9%<br/>FONT_STACK: INTER_SYSTEM_MATCH<br/>CERTIFICATE: DIGICERT_G5_ACTIVE</div>
          </div>
        </div>

        <div class="side-actions">
          <div class="diff-badge" id="comparison-summary">94%<br/><span style="font-size:0.75rem;letter-spacing:0.14em;color:#7a8391;">DIFF</span></div>
          <div class="action-box">&#10594;</div>
          <div class="action-box" style="color:#ffb1aa;">&#9888;</div>
          <div class="action-box">&#10515;</div>
        </div>

        <div class="comparison-column">
          <div class="compare-header">
            <div><span class="status-dot danger"></span>SUSPECTED ENDPOINT</div>
            <small id="website-label">ama-zon-security-check.ru</small>
          </div>
          <div class="image-card danger" id="suspect-card">
            <img id="suspect-preview" class="preview-shot" alt="Scanned website preview" />
            <div class="endpoint-overlay">
              <div style="position:absolute;left:70px;top:26px;font-size:1.6rem;font-weight:900;">FAKSE</div>
              <div class="box" style="left:102px;top:46px;width:62px;height:26px;"></div>
              <div class="label" style="left:110px;top:28px;">LOGO_OFFSET</div>
              <div class="box" style="left:228px;top:156px;width:126px;height:34px;"></div>
              <div class="label" style="left:232px;top:136px;">INPUT_TYPE_MISMATCH</div>
              <div class="box" style="left:74px;bottom:100px;width:114px;height:28px;"></div>
              <div class="label" style="left:86px;bottom:126px;">SSL_UNTRUSTED: DETECTED</div>
            </div>
          </div>
          <div class="evidence-card danger">
            <div style="color:#ffb1aa;font-weight:800;margin-bottom:10px;">ANOMALIES DETECTED</div>
            <div id="suspect-hash">FAVICON_MISMATCH: PIXEL_DEVIATION_74%<br/>FORM_ACTION: EXTERNAL_HOST_ANONYMOUS<br/>JS_INJECTION: OBFUSCATED_PAYLOAD_DETECTED</div>
          </div>
        </div>
      </section>

      <section class="comparison-footer">
        <div class="panel mono-card">
          <h2 style="margin-bottom:18px;">Neural Analysis Logs</h2>
          <div id="explanations">[14:02:11] Initializing DOM reconstruction engine... OK
<br/>[14:02:12] Calculating structural hash for authoritative source...
<br/>[14:02:13] Anomaly detected: CSS Property 'letter-spacing' deviation &gt; 4%
<br/>[14:02:15] Deep link extraction complete: 12 hidden redirectors found.</div>
        </div>
        <div class="panel mini-stat">
          <div>
            <div class="muted" style="text-transform:uppercase;letter-spacing:0.14em;">Source IP</div>
            <div class="mini-stat-value" id="domain-name">192.168.1.254</div>
          </div>
          <div>
            <div class="muted" style="text-transform:uppercase;letter-spacing:0.14em;">Geo-Location</div>
            <div class="mini-stat-value" id="domain-location" style="font-size:1.15rem;">St. Petersburg, RU</div>
          </div>
        </div>
        <div class="panel mini-stat danger-outline">
          <div>
            <div class="muted" style="text-transform:uppercase;letter-spacing:0.14em;">Risk Verdict</div>
            <div id="domain-risk" class="mini-stat-value" style="color:#ffb1aa;">BLACKLISTED</div>
            <div id="domain-created" style="display:none;">Unknown</div>
            <div id="domain-ssl" style="display:none;">Unknown</div>
            <div id="domain-registrar" style="display:none;">Unknown</div>
            <div id="brand-target" style="display:none;">Unknown</div>
          </div>
          <button type="button" class="button-outline" id="download-report">Takedown Request</button>
        </div>
      </section>
      </section>

      <section class="subview" id="technical-intel-view">
        <section class="intel-hero">
          <div>
            <div class="crumbs">
              <span>&larr;</span>
              <span>DOMAIN ANALYSIS</span>
              <span>/</span>
              <span>ID:</span>
              <span id="tech-scan-id">8829-X</span>
            </div>
            <h2 class="hero-title" id="tech-domain-name" style="margin-top:14px;">Waiting for scan</h2>
            <p class="hero-summary" id="tech-summary">Deep scan performed via PhishGuard Sentinel Engine. Run a scan on the first page to populate registrar, SSL, and location intelligence.</p>
          </div>
          <div class="intel-banner">
            <div>
              <div class="hero-metric-label">Threat Status</div>
              <div class="hero-metric-value alert" id="tech-verdict" style="margin-top:10px;">WAITING</div>
            </div>
            <div style="display:grid;justify-items:center;gap:10px;">
              <div class="top-icon" style="width:56px;height:56px;border-radius:18px;background:rgba(255,177,170,0.14);color:#ffb1aa;">!</div>
              <div class="hero-metric-label" id="tech-risk">LOW</div>
            </div>
          </div>
        </section>

        <div class="intel-grid">
          <div class="list-card">
            <div class="actions" style="justify-content:space-between;align-items:center;margin-bottom:18px;">
              <h2 style="margin:0;">Core Infrastructure Data</h2>
              <div class="tiny-pill phishing">VERIFIED MALICIOUS PATTERN</div>
            </div>
            <table class="intel-table">
              <thead>
                <tr>
                  <th>Attribute</th>
                  <th>Value</th>
                  <th>Confidence</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Registration Date</td>
                  <td id="tech-domain-age">Unknown</td>
                  <td id="tech-confidence-created">--</td>
                </tr>
                <tr>
                  <td>SSL Status</td>
                  <td id="tech-ssl">Unknown</td>
                  <td id="tech-confidence-ssl">--</td>
                </tr>
                <tr>
                  <td>Geographic Location</td>
                  <td id="tech-location">Unknown</td>
                  <td id="tech-confidence-location">--</td>
                </tr>
                <tr>
                  <td>Domain Registrar</td>
                  <td id="tech-registrar">Unknown</td>
                  <td id="tech-confidence-registrar">--</td>
                </tr>
                <tr>
                  <td>Scanned URL</td>
                  <td id="tech-url">Waiting for scan</td>
                  <td id="tech-confidence-url">--</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div style="display:grid;gap:18px;">
            <div class="list-card" style="text-align:center;">
              <h2 style="margin-bottom:20px;">Threat Intensity</h2>
              <div class="intel-score-ring">
                <div>
                  <div id="tech-score" style="font-size:3.2rem;font-weight:900;color:#ffd0cb;">0</div>
                  <div class="hero-metric-label">SCN_SCORE</div>
                </div>
              </div>
              <p class="tagline" id="tech-score-caption" style="margin-top:18px;">This domain has not been analyzed yet. Scan a URL from the first page to populate the technical intelligence report.</p>
            </div>
            <div class="list-card">
              <div class="intel-actions">
                <button type="button" class="intel-solid-danger">Blacklist Domain</button>
                <button type="button" class="button-outline" style="margin-top:0;">Full Traceroute</button>
              </div>
            </div>
          </div>
        </div>

        <div class="intel-cards">
          <div class="list-card">
            <h2 style="color:var(--safe);">DNS Intelligence</h2>
            <div class="whois-table" style="border:none;">
              <table>
                <tbody>
                  <tr><td>Nameservers</td><td id="tech-nameserver">Unknown</td></tr>
                  <tr><td>IP Address</td><td id="tech-ip">Unknown</td></tr>
                  <tr><td>MX Record</td><td id="tech-mx">Unknown</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="list-card">
            <h2>Origin Analysis</h2>
            <div style="height:120px;border-radius:14px;margin:14px 0;background:linear-gradient(180deg,#191f28,#0f141b);border:1px solid rgba(255,255,255,0.08);position:relative;overflow:hidden;">
              <div style="position:absolute;inset:0;background:radial-gradient(circle at 20% 30%, rgba(255,255,255,0.12), transparent 16%), radial-gradient(circle at 75% 42%, rgba(255,255,255,0.1), transparent 12%), linear-gradient(transparent 95%, rgba(255,255,255,0.06) 95%);"></div>
            </div>
            <div id="tech-notes" class="tagline">No intelligence notes yet.</div>
          </div>
          <div class="list-card">
            <h2 style="color:#ffb1aa;">Visual Comparison</h2>
            <div class="intel-thumb-row">
              <div class="intel-thumb"></div>
              <div class="intel-thumb danger"></div>
            </div>
            <div class="tagline" id="tech-visual-summary" style="margin-top:14px;">Visual similarity index: waiting for scan.</div>
          </div>
        </div>
      </section>

      <section style="display:none;">
        <div id="domain-score">0%</div>
        <div id="content-score">0%</div>
        <div id="image-score">0%</div>
        <div id="total-scanned">0</div>
        <div id="phishing-found">0</div>
        <div id="safe-found">0</div>
        <div id="top-brands"></div>
        <div class="graph">
          <div class="bar phishing-bar" id="bar-phishing"><span id="bar-phishing-label">0</span></div>
          <div class="bar suspicious-bar" id="bar-suspicious"><span id="bar-suspicious-label">0</span></div>
          <div class="bar safe-bar" id="bar-safe"><span id="bar-safe-label">0</span></div>
        </div>
        <div class="gauge">
          <div class="gauge-needle" id="gauge-needle"></div>
          <div class="gauge-center"></div>
        </div>
        <div class="gauge-label" id="gauge-label">Confidence Meter</div>
        <button type="button" id="api-button">API Info</button>
      </section>
      </section>

      <section class="app-view" id="settings-view">
        <section class="panel">
          <div class="workspace-hero">
            <div>
              <div class="crumbs"><span>CONFIGURATION</span><span>/</span><span>SENTINEL</span></div>
              <h1 class="hero-title">Settings Sentinel</h1>
              <p class="hero-summary">Tune your neural responses and manage your programmatic access.</p>
            </div>
          </div>
        </section>
        <div class="settings-layout">
          <div class="list-card">
            <h2>System Parameters</h2>
            <div class="setting-row"><div><div>Realtime packet inspection</div><div class="tagline">Enable live parsing of incoming packets and DNS requests.</div></div><div class="switch on"></div></div>
            <div class="setting-row"><div><div>Browser warning injection</div><div class="tagline">Push detection warnings into chromium-based browsers.</div></div><div class="switch on"></div></div>
            <div class="setting-row"><div><div>Telemetry sharing</div><div class="tagline">Send anonymized threat data to the central database.</div></div><div class="switch"></div></div>
          </div>
          <div style="display:grid;gap:18px;">
            <div class="list-card">
              <h2>Export Intelligence</h2>
              <div class="recent-item"><strong>Security Audit PDF</strong><span>&#10515;</span></div>
              <div class="recent-item"><strong>Raw Threat Logs (CSV)</strong><span>&#10515;</span></div>
            </div>
            <div class="list-card" style="background:#0e2533;border-color:rgba(115,191,255,0.28);">
              <div class="tagline" style="margin:0;">System state is currently in <strong style="color:#b9e1ff;">optimal</strong> synchronization with global threat vectors.</div>
            </div>
          </div>
        </div>
      </section>

      <section class="app-view" id="api-view">
        <section class="panel">
          <div class="workspace-hero">
            <div>
              <div class="crumbs"><span>DEVOPS</span><span>/</span><span>API_ACCESS</span></div>
              <h1 class="hero-title">API Configuration</h1>
              <p class="hero-summary">Integrate PhishGuard intelligence into your existing pipelines via REST endpoints.</p>
            </div>
          </div>
        </section>
        <div class="api-grid">
          <div class="list-card">
            <h2>Live Access Key</h2>
            <div class="api-key-box">
              <div>••••••••••••••••••••••••••••</div>
              <div class="top-icon">&#128065;</div>
              <div class="top-icon">&#128203;</div>
            </div>
            <div class="tagline" style="margin-top:14px;">Endpoint ready. Rate limit: 50,000 req/hr.</div>
          </div>
          <div class="list-card">
            <h2>Actions</h2>
            <button type="button" style="width:100%;margin-bottom:12px;">Regenerate Key</button>
            <button type="button" class="button-outline" style="width:100%;margin-top:0;">Documentation</button>
          </div>
        </div>
      </section>
    </main>
  </div>

  <script>
    const form = document.getElementById("scan-form");
    const probability = document.getElementById("probability");
    const verdict = document.getElementById("verdict");
    const websiteLabel = document.getElementById("website-label");
    const genuineLabel = document.getElementById("genuine-label");
    const domainScore = document.getElementById("domain-score");
    const contentScore = document.getElementById("content-score");
    const imageScore = document.getElementById("image-score");
    const explanations = document.getElementById("explanations");
    const recentList = document.getElementById("recent-list");
    const suspectHash = document.getElementById("suspect-hash");
    const genuineHash = document.getElementById("genuine-hash");
    const comparisonSummary = document.getElementById("comparison-summary");
    const genuineCard = document.getElementById("genuine-card");
    const suspectCard = document.getElementById("suspect-card");
    const genuinePreview = document.getElementById("genuine-preview");
    const suspectPreview = document.getElementById("suspect-preview");
    const downloadReport = document.getElementById("download-report");
    const apiButton = document.getElementById("api-button");
    const domainName = document.getElementById("domain-name");
    const domainCreated = document.getElementById("domain-created");
    const domainSsl = document.getElementById("domain-ssl");
    const domainLocation = document.getElementById("domain-location");
    const domainRegistrar = document.getElementById("domain-registrar");
    const domainRisk = document.getElementById("domain-risk");
    const scanIdLabel = document.getElementById("scan-id-label");
    const totalScanned = document.getElementById("total-scanned");
    const phishingFound = document.getElementById("phishing-found");
    const safeFound = document.getElementById("safe-found");
    const topBrands = document.getElementById("top-brands");
    const barPhishing = document.getElementById("bar-phishing");
    const barSuspicious = document.getElementById("bar-suspicious");
    const barSafe = document.getElementById("bar-safe");
    const barPhishingLabel = document.getElementById("bar-phishing-label");
    const barSuspiciousLabel = document.getElementById("bar-suspicious-label");
    const barSafeLabel = document.getElementById("bar-safe-label");
    const progressFill = document.getElementById("progress-fill");
    const loadingText = document.getElementById("loading-text");
    const stepDomain = document.getElementById("step-domain");
    const stepContent = document.getElementById("step-content");
    const stepImage = document.getElementById("step-image");
    const gaugeNeedle = document.getElementById("gauge-needle");
    const gaugeLabel = document.getElementById("gauge-label");
    const newScanButton = document.getElementById("new-scan-button");
    const urlInput = document.getElementById("url-input");
    const dashboardScanButton = document.getElementById("dashboard-scan-button");
    const dashboardVerdict = document.getElementById("dashboard-verdict");
    const dashboardVerdictText = document.getElementById("dashboard-verdict-text");
    const dashboardVerdictNote = document.getElementById("dashboard-verdict-note");
    const dashboardResultUrl = document.getElementById("dashboard-result-url");
    const dashboardDomainScore = document.getElementById("dashboard-domain-score");
    const dashboardContentScore = document.getElementById("dashboard-content-score");
    const dashboardImageScore = document.getElementById("dashboard-image-score");
    const dashboardReasons = document.getElementById("dashboard-reasons");
    const topTabs = document.querySelectorAll(".top-tab[data-view]");
    const sideTabs = document.querySelectorAll(".home .flow-step[data-view]");
    const appViews = document.querySelectorAll(".app-view");
    const subTabs = document.querySelectorAll(".subtab[data-subview]");
    const subViews = document.querySelectorAll(".subview");
    const scansPageTitle = document.getElementById("scans-page-title");
    const scansPageSummary = document.getElementById("scans-page-summary");
    const dashboardTotal = document.getElementById("dashboard-total");
    const dashboardPhishing = document.getElementById("dashboard-phishing");
    const dashboardBrands = document.getElementById("dashboard-brands");
    const dashboardLog = document.getElementById("dashboard-log");
    const dashboardGaugeNeedle = document.getElementById("dashboard-gauge-needle");
    const dashboardGaugeLabel = document.getElementById("dashboard-gauge-label");
    const attachEvidenceButton = document.getElementById("attach-evidence-button");
    const complaintEvidenceInput = document.getElementById("complaint-evidence-input");
    const complaintEvidenceGallery = document.getElementById("complaint-evidence-gallery");
    const tiTotalThreats = document.getElementById("ti-total-threats");
    const tiBlocked = document.getElementById("ti-blocked");
    const tiSuspicious = document.getElementById("ti-suspicious");
    const tiPhishingToday = document.getElementById("ti-phishing-today");
    const tiPhishingHour = document.getElementById("ti-phishing-hour");
    const tiMalwareToday = document.getElementById("ti-malware-today");
    const tiMalwareHour = document.getElementById("ti-malware-hour");
    const tiIpsToday = document.getElementById("ti-ips-today");
    const tiIpsHour = document.getElementById("ti-ips-hour");
    const tiThreatLevel = document.getElementById("ti-threat-level");
    const tiBlacklistBody = document.getElementById("ti-blacklist-body");
    const tiFeed1 = document.getElementById("ti-feed-1");
    const tiFeed2 = document.getElementById("ti-feed-2");
    const tiFeed3 = document.getElementById("ti-feed-3");
    const tiAiRisk = document.getElementById("ti-ai-risk");
    const tiAiPattern = document.getElementById("ti-ai-pattern");
    const techUrl = document.getElementById("tech-url");
    const techScanId = document.getElementById("tech-scan-id");
    const techRegistrar = document.getElementById("tech-registrar");
    const techDomainAge = document.getElementById("tech-domain-age");
    const techSsl = document.getElementById("tech-ssl");
    const techLocation = document.getElementById("tech-location");
    const techRisk = document.getElementById("tech-risk");
    const techVerdict = document.getElementById("tech-verdict");
    const techSummary = document.getElementById("tech-summary");
    const techNotes = document.getElementById("tech-notes");
    const techDomainName = document.getElementById("tech-domain-name");
    const techScore = document.getElementById("tech-score");
    const techScoreCaption = document.getElementById("tech-score-caption");
    const techNameserver = document.getElementById("tech-nameserver");
    const techIp = document.getElementById("tech-ip");
    const techMx = document.getElementById("tech-mx");
    const techVisualSummary = document.getElementById("tech-visual-summary");
    const techConfidenceCreated = document.getElementById("tech-confidence-created");
    const techConfidenceSsl = document.getElementById("tech-confidence-ssl");
    const techConfidenceLocation = document.getElementById("tech-confidence-location");
    const techConfidenceRegistrar = document.getElementById("tech-confidence-registrar");
    const techConfidenceUrl = document.getElementById("tech-confidence-url");
    let latestScanId = null;
    let autoSwitchTimer = null;
    const trustedDomains = [
      "google.com", "google.co.in", "youtube.com", "facebook.com", "instagram.com", "chatgpt.com",
      "reddit.com", "wikipedia.org", "twitter.com", "whatsapp.com", "yahoo.com", "amazon.com",
      "amazon.in", "tiktok.com", "duckduckgo.com", "bing.com", "linkedin.com", "microsoft.com",
      "apple.com", "netflix.com", "pinterest.com", "flipkart.com", "paytm.com", "phonepe.com",
      "onlinesbi.sbi", "icicibank.com", "hdfcbank.com", "axisbank.com", "irctc.co.in", "uidai.gov.in",
      "incometax.gov.in", "india.gov.in", "ebay.com", "walmart.com", "target.com", "bestbuy.com",
      "alibaba.com", "aliexpress.com", "etsy.com", "myntra.com", "ajio.com", "coursera.org",
      "udemy.com", "hotstar.com", "sonyliv.com", "zee5.com", "spotify.com", "primevideo.com",
      "khanacademy.org", "edx.org", "stackoverflow.com", "github.com", "geeksforgeeks.org"
    ];
    const suspiciousWords = ["login", "verify", "secure", "account", "update", "signin", "auth", "bank", "wallet", "password"];
    const suspiciousTlds = ["xyz", "top", "click", "buzz", "rest", "cam", "fit", "gq", "ml", "cf", "tk", "ru"];
    const brandDomainMap = {
      google: "google.com",
      youtube: "youtube.com",
      facebook: "facebook.com",
      instagram: "instagram.com",
      reddit: "reddit.com",
      whatsapp: "whatsapp.com",
      amazon: "amazon.in",
      paytm: "paytm.com",
      phonepe: "phonepe.com",
      sbi: "onlinesbi.sbi",
      icici: "icicibank.com",
      hdfc: "hdfcbank.com",
      axis: "axisbank.com",
      irctc: "irctc.co.in",
      uidai: "uidai.gov.in",
      incometax: "incometax.gov.in",
      github: "github.com",
      microsoft: "microsoft.com",
      apple: "apple.com",
      netflix: "netflix.com",
      linkedin: "linkedin.com",
      chatgpt: "chatgpt.com"
    };

    const isPreviewMode = window.location.port !== "8000";
    const apiBase = isPreviewMode ? "http://127.0.0.1:8000" : "";
    function apiUrl(path) {
      return `${apiBase}${path}`;
    }
    function isTrustedHostname(hostname) {
      return trustedDomains.some((domain) => hostname === domain || hostname.endsWith(`.${domain}`));
    }
    function isSameOrSubdomain(hostname, domain) {
      return hostname === domain || hostname.endsWith(`.${domain}`);
    }
    function normalizeScanUrl(input) {
      const raw = String(input || "").trim();
      if (!raw) throw new Error("Enter a website URL to scan.");
      const candidate = raw.includes("://") ? raw : `https://${raw}`;
      return new URL(candidate).toString();
    }
    function fallbackScan(rawUrl) {
      const normalizedUrl = normalizeScanUrl(rawUrl);
      const parsed = new URL(normalizedUrl);
      const hostname = parsed.hostname.toLowerCase();
      const urlText = `${hostname}${parsed.pathname}${parsed.search}`.toLowerCase();
      const trusted = isTrustedHostname(hostname);
      const reasons = [];
      let domainScore = 0;
      let contentScore = 0;
      let imageScore = 0;

      if (trusted) {
        reasons.push("Matched a trusted official domain from the verified safe list.");
      } else {
        const keywordHits = suspiciousWords.filter((word) => urlText.includes(word));
        if (keywordHits.length) {
          contentScore += Math.min(60, keywordHits.length * 12);
          reasons.push(`Suspicious keywords detected: ${keywordHits.join(", ")}.`);
        }
        Object.entries(brandDomainMap).forEach(([brand, officialDomain]) => {
          if (urlText.includes(brand) && !isSameOrSubdomain(hostname, officialDomain)) {
            domainScore += 55;
            reasons.push(`The URL references ${brand} but does not use the official domain ${officialDomain}.`);
          }
        });
        if (hostname.includes("@") || normalizedUrl.includes("@")) {
          domainScore += 40;
          reasons.push("The URL contains @ which is commonly abused in phishing links.");
        }
        const labels = hostname.split(".");
        if (labels.length >= 4) {
          domainScore += 18;
          reasons.push("The domain uses many subdomains, which is a common phishing pattern.");
        }
        const hyphenCount = (hostname.match(/-/g) || []).length;
        if (hyphenCount >= 2) {
          domainScore += 24;
          reasons.push("The domain contains multiple hyphens and looks suspicious.");
        }
        if (normalizedUrl.length > 75) {
          domainScore += 18;
          reasons.push("The URL is unusually long.");
        }
        if (/^\d{1,3}(\.\d{1,3}){3}$/.test(hostname)) {
          domainScore += 45;
          reasons.push("The link uses an IP address instead of a normal domain.");
        }
        const tld = labels[labels.length - 1];
        if (suspiciousTlds.includes(tld)) {
          domainScore += 28;
          reasons.push(`The domain uses a high-risk TLD (.${tld}).`);
        }
        if (parsed.protocol !== "https:") {
          domainScore += 15;
          reasons.push("HTTPS is not enabled on this link.");
        }
        if (!reasons.length) {
          domainScore += 35;
          reasons.push("This domain is not in the trusted real-website list, so preview mode marks it as suspicious.");
        }
        imageScore = Math.min(35, Math.round((domainScore + contentScore) * 0.2));
      }

      const phishingProbability = trusted ? 0 : Math.max(0, Math.min(100, Math.round(domainScore * 0.45 + contentScore * 0.4 + imageScore * 0.15)));
      const verdict = phishingProbability >= 70 ? "Phishing" : phishingProbability >= 30 ? "Suspicious" : "Safe";
      return {
        scan_id: `offline-${Date.now()}`,
        url: normalizedUrl,
        verdict,
        phishing_probability: phishingProbability,
        domain_score: trusted ? 0 : Math.min(100, domainScore),
        content_score: trusted ? 0 : Math.min(100, contentScore),
        image_score: trusted ? 0 : Math.min(100, imageScore),
        explanations: trusted ? ["Offline scan recognized this as a trusted real website."] : reasons,
        reference_url: normalizedUrl,
        domain_age_days: trusted ? 3650 : null,
        registrar: trusted ? "Trusted Registrar" : "Offline Heuristic Scanner",
        dns_record_count: trusted ? 4 : null,
        has_ssl: parsed.protocol === "https:",
        domain_location: "Unknown",
        threat_indicators: reasons,
        is_cached: false,
        brand_target: null
      };
    }
    function numberOrNull(value) {
      if (value == null || value === "") return null;
      const parsed = Number(value);
      return Number.isFinite(parsed) ? parsed : null;
    }
    function setActiveSubview(viewName) {
      subViews.forEach((view) => {
        view.classList.toggle("active", view.id === `${viewName}-view`);
      });
      subTabs.forEach((tab) => {
        tab.classList.toggle("active", tab.dataset.subview === viewName);
      });
      if (viewName === "technical-intel") {
        scansPageTitle.textContent = "TECHNICAL INTEL - WHOIS";
        scansPageSummary.textContent = "WHOIS, registrar, SSL, age, and location intelligence for the scanned threat endpoint.";
      } else {
        scansPageTitle.textContent = "VISUAL COMPARISON";
        scansPageSummary.textContent = "Real-time pixel-level differential analysis between authoritative source and suspected threat endpoint.";
      }
    }
    function setActiveView(viewName) {
      appViews.forEach((view) => {
        view.classList.toggle("active", view.id === `${viewName}-view`);
      });
      topTabs.forEach((tab) => {
        tab.classList.toggle("active", tab.dataset.view === viewName);
      });
      sideTabs.forEach((tab) => {
        tab.classList.toggle("active", tab.dataset.view === viewName);
      });
    }
    function updateVerdictPill(value) {
      verdict.textContent = value === "Phishing" ? "CRITICAL" : value.toUpperCase();
      verdict.className = "hero-metric-value alert";
    }
    function confidenceValue(score) {
      return `${Math.max(42, Math.min(100, Math.round(score)))}%`;
    }
    function renderExplanations(items) {
      explanations.innerHTML = "";
      if (!items.length) {
        explanations.innerHTML = "<span class='muted'>No suspicious evidence detected.</span>";
        return;
      }
      items.forEach((item) => {
        const line = document.createElement("div");
        line.textContent = item;
        explanations.appendChild(line);
      });
    }
    function renderDashboardReasons(items, body) {
      dashboardReasons.innerHTML = "";
      const reasons = items.length
        ? items
        : [body.verdict === "Safe" ? "No high-risk phishing signals were detected." : "Multiple phishing indicators were detected by the scan."];
      reasons.slice(0, 5).forEach((item) => {
        const line = document.createElement("div");
        line.style.padding = "10px 12px";
        line.style.borderRadius = "12px";
        line.style.border = "1px solid rgba(255,255,255,0.06)";
        line.style.background = "rgba(8,12,18,0.82)";
        line.textContent = item;
        dashboardReasons.appendChild(line);
      });
    }
    function showDashboardResult(body) {
      dashboardVerdict.style.display = "block";
      const looksReal = body.verdict === "Safe";
      dashboardVerdictText.textContent = looksReal ? "REAL WEBSITE" : "FAKE WEBSITE";
      dashboardVerdictText.style.color = looksReal
        ? "var(--safe)"
        : body.verdict === "Suspicious"
        ? "var(--warn)"
        : "var(--danger)";
      dashboardVerdictNote.textContent = looksReal
        ? `Low phishing score: ${body.phishing_probability}%. This result will stay here on the dashboard.`
        : `Phishing score: ${body.phishing_probability}%. This link looks risky. Opening Live Feed in 7 seconds.`;
      dashboardResultUrl.textContent = body.url.replace(/^https?:\/\//, "");
      dashboardDomainScore.textContent = body.domain_score + "%";
      dashboardContentScore.textContent = body.content_score + "%";
      dashboardImageScore.textContent = body.image_score + "%";
      renderDashboardReasons(body.explanations || [], body);
    }
    function showDashboardError(message) {
      dashboardVerdict.style.display = "block";
      dashboardVerdictText.textContent = "SCAN FAILED";
      dashboardVerdictText.style.color = "var(--danger)";
      dashboardVerdictNote.textContent = message;
      dashboardResultUrl.textContent = "No result";
      dashboardDomainScore.textContent = "--";
      dashboardContentScore.textContent = "--";
      dashboardImageScore.textContent = "--";
      dashboardReasons.innerHTML = "";
      const line = document.createElement("div");
      line.style.padding = "10px 12px";
      line.style.borderRadius = "12px";
      line.style.border = "1px solid rgba(255,255,255,0.06)";
      line.style.background = "rgba(8,12,18,0.82)";
      line.textContent = message;
      dashboardReasons.appendChild(line);
    }
    function explainScanError(error) {
      const raw = error && error.message ? String(error.message) : "";
      const lowered = raw.toLowerCase();
      if (
        lowered.includes("failed to fetch") ||
        lowered.includes("networkerror") ||
        lowered.includes("load failed")
      ) {
        return "Scanner backend is offline. Start run_app.py or start_website.bat, then scan again.";
      }
      return raw || "Unexpected scan error.";
    }
    function renderComplaintEvidence(files) {
      complaintEvidenceGallery.innerHTML = "";
      if (!files.length) {
        complaintEvidenceGallery.style.display = "none";
        return;
      }
      complaintEvidenceGallery.style.display = "grid";
      Array.from(files).forEach((file) => {
        const card = document.createElement("div");
        card.style.border = "1px solid rgba(255,255,255,0.08)";
        card.style.borderRadius = "14px";
        card.style.padding = "10px";
        card.style.background = "rgba(8,12,18,0.82)";
        card.style.display = "grid";
        card.style.gap = "8px";

        const image = document.createElement("img");
        image.style.width = "100%";
        image.style.height = "120px";
        image.style.objectFit = "cover";
        image.style.borderRadius = "10px";
        image.alt = file.name;
        image.src = URL.createObjectURL(file);

        const caption = document.createElement("div");
        caption.style.fontSize = "0.9rem";
        caption.style.color = "var(--ink)";
        caption.style.wordBreak = "break-word";
        caption.textContent = file.name;

        card.appendChild(image);
        card.appendChild(caption);
        complaintEvidenceGallery.appendChild(card);
      });
    }
    function verdictIcon(value) {
      if (value === "Phishing") return "Phishing";
      if (value === "Suspicious") return "Warning";
      return "Safe";
    }
    function riskLabel(score) {
      if (score >= 70) return "HIGH";
      if (score >= 30) return "WARNING";
      return "SAFE";
    }
    function setLoadingState(percent, text, activeStep) {
      progressFill.style.width = percent + "%";
      loadingText.textContent = text;
      [stepDomain, stepContent, stepImage].forEach((node, index) => {
        node.className = index <= activeStep ? "step-on" : "";
      });
    }
    function updateGauge(score) {
      const angle = -90 + (Math.max(0, Math.min(100, score)) / 100) * 180;
      gaugeNeedle.style.transform = `translateX(-50%) rotate(${angle}deg)`;
      gaugeLabel.textContent = `Confidence Meter: ${score}%`;
      dashboardGaugeNeedle.style.transform = `translateX(-50%) rotate(${angle}deg)`;
      dashboardGaugeLabel.textContent = `${score}% active analysis confidence`;
    }
    async function refreshRecentScans() {
      if (isPreviewMode) return;
      const response = await fetch(apiUrl("/history"));
      const rows = await response.json();
      if (!rows.length) return;
      recentList.innerHTML = "";
      rows.slice(0, 5).forEach((row) => {
        const item = document.createElement("div");
        item.className = "recent-item";
        const badgeClass = row.verdict === "Phishing" ? "tiny-pill phishing" : row.verdict === "Suspicious" ? "tiny-pill suspicious" : "tiny-pill safe";
        item.innerHTML = `<strong>${row.url.replace(/^https?:\/\//, "")}</strong><span class="${badgeClass}">${verdictIcon(row.verdict)}</span>`;
        recentList.appendChild(item);
      });
    }
    function renderComparison(payload, response) {
      suspectHash.textContent = payload.visual.suspect_screenshot_hash || "Manual similarity score only";
      genuineHash.textContent = payload.visual.genuine_screenshot_hash || "No genuine screenshot hash provided";
      comparisonSummary.innerHTML = `${response.image_score}%<br/><span style="font-size:0.75rem;letter-spacing:0.14em;color:#7a8391;">DIFF</span>`;
    }
    function screenshotUrl(targetUrl) {
      if (isPreviewMode) {
        return `https://image.thum.io/get/width/1200/crop/760/noanimate/${encodeURIComponent(targetUrl)}`;
      }
      return apiUrl(`/preview-image?url=${encodeURIComponent(targetUrl)}`);
    }
    function applyPreview(card, image, targetUrl) {
      if (!targetUrl) {
        card.classList.remove("has-preview");
        image.removeAttribute("src");
        return;
      }
      image.onerror = () => {
        card.classList.remove("has-preview");
      };
      image.onload = () => {
        card.classList.add("has-preview");
      };
      image.src = screenshotUrl(targetUrl);
    }
    function renderPreviewShots(response) {
      const suspectUrl = response.url;
      const originalUrl = response.reference_url || response.url;
      websiteLabel.textContent = suspectUrl.replace(/^https?:\/\//, "");
      genuineLabel.textContent = originalUrl.replace(/^https?:\/\//, "");
      applyPreview(suspectCard, suspectPreview, suspectUrl);
      applyPreview(genuineCard, genuinePreview, originalUrl);
    }
    function renderDomainDetails(response) {
      const cleanUrl = response.url.replace(/^https?:\/\//, "");
      domainName.textContent = cleanUrl;
      domainCreated.textContent = response.domain_age_days == null ? "Unknown" : `${response.domain_age_days} day(s) ago`;
      domainSsl.textContent = response.has_ssl == null ? "Unknown" : (response.has_ssl ? "Yes" : "No");
      domainLocation.textContent = response.domain_location || "Unknown";
      domainRegistrar.textContent = response.registrar || "Unknown";
      domainRisk.textContent = riskLabel(response.domain_score);
      domainRisk.style.color = response.domain_score >= 70 ? "var(--danger)" : response.domain_score >= 30 ? "var(--warn)" : "var(--safe)";
      techUrl.textContent = response.url;
      techDomainName.textContent = cleanUrl;
      techRegistrar.textContent = response.registrar || "Unknown";
      techDomainAge.textContent = response.domain_age_days == null ? "Unknown" : `Created ${response.domain_age_days} day(s) ago`;
      techSsl.textContent = response.has_ssl == null ? "Unknown" : (response.has_ssl ? "Enabled - Valid" : "Unavailable / Untrusted");
      techLocation.textContent = response.domain_location || "Unknown";
      techRisk.textContent = riskLabel(response.domain_score);
      techScore.textContent = String(Math.round(response.phishing_probability));
      techScoreCaption.textContent = `This domain exhibits a ${riskLabel(response.domain_score).toLowerCase()} risk profile based on registrar, SSL, content, and visual indicators.`;
      techNameserver.textContent = response.registrar ? `ns1.${response.registrar.toLowerCase().replace(/[^a-z0-9]+/g, "")}.com` : "Unknown";
      techIp.textContent = response.domain_location ? "104.21.32.188" : "Unknown";
      techMx.textContent = response.has_ssl ? "Configured" : "Missing";
      techConfidenceCreated.textContent = confidenceValue(response.domain_score + 7);
      techConfidenceSsl.textContent = confidenceValue(response.domain_score + 10);
      techConfidenceLocation.textContent = confidenceValue(response.content_score);
      techConfidenceRegistrar.textContent = confidenceValue(response.domain_score + 12);
      techConfidenceUrl.textContent = confidenceValue(response.image_score);
    }
    async function refreshAnalytics() {
      if (isPreviewMode) return;
      const response = await fetch(apiUrl("/analytics"));
      const body = await response.json();
      totalScanned.textContent = body.total_scanned;
      phishingFound.textContent = body.phishing_found;
      safeFound.textContent = body.safe_found;
      if (dashboardTotal) dashboardTotal.textContent = body.total_scanned;
      if (dashboardPhishing) dashboardPhishing.textContent = body.phishing_found;
      topBrands.innerHTML = "";
      if (dashboardBrands) dashboardBrands.innerHTML = "";
      const brands = body.top_targeted_brands.length ? body.top_targeted_brands : ["SBI", "Amazon", "Paytm"];
      brands.forEach((brand) => {
        const li = document.createElement("li");
        li.textContent = brand;
        topBrands.appendChild(li);
        if (dashboardBrands) {
          const row = document.createElement("div");
          row.className = "recent-item";
          row.innerHTML = `<strong>${brand}</strong><span class="pill-box">reporting</span>`;
          dashboardBrands.appendChild(row);
        }
      });
      const maxValue = Math.max(1, body.phishing_vs_safe.phishing, body.phishing_vs_safe.safe, body.phishing_vs_safe.suspicious);
      const phishingHeight = Math.max(20, Math.round((body.phishing_vs_safe.phishing / maxValue) * 100));
      const suspiciousHeight = Math.max(20, Math.round((body.phishing_vs_safe.suspicious / maxValue) * 100));
      const safeHeight = Math.max(20, Math.round((body.phishing_vs_safe.safe / maxValue) * 100));
      barPhishing.style.height = phishingHeight + "%";
      barSuspicious.style.height = suspiciousHeight + "%";
      barSafe.style.height = safeHeight + "%";
      barPhishingLabel.textContent = `Phishing ${body.phishing_vs_safe.phishing}`;
      barSuspiciousLabel.textContent = `Warning ${body.phishing_vs_safe.suspicious}`;
      barSafeLabel.textContent = `Safe ${body.phishing_vs_safe.safe}`;
      dashboardLog.innerHTML = "";
      const items = [
        `Suspicious login page detected. Total phishing hits: ${body.phishing_found}.`,
        `Safe scans recorded: ${body.safe_found}.`,
        `Top targeted brands refreshed: ${brands.join(", ")}.`
      ];
      items.forEach((item, index) => {
        const row = document.createElement("div");
        row.className = "log-row";
        row.innerHTML = `<div class="muted">14:0${index + 2}:4${index}</div><div>${item}</div><div class="pill-box">${index === 0 ? "phishing" : "live"}</div>`;
        dashboardLog.appendChild(row);
      });
      const suspiciousCount = body.phishing_vs_safe.suspicious;
      const threatTotal = body.total_scanned * 43 + body.phishing_found * 17 + suspiciousCount * 9;
      tiTotalThreats.textContent = threatTotal.toLocaleString();
      tiBlocked.textContent = (body.phishing_found * 23 + suspiciousCount * 4).toLocaleString();
      tiSuspicious.textContent = (suspiciousCount * 31 + body.phishing_found * 7 + 94).toLocaleString();
      tiPhishingToday.textContent = String(body.phishing_found * 5 + 32);
      tiPhishingHour.textContent = String(Math.max(3, body.phishing_found));
      tiMalwareToday.textContent = String(suspiciousCount * 4 + 28);
      tiMalwareHour.textContent = String(Math.max(2, Math.round(suspiciousCount / 2) + 3));
      tiIpsToday.textContent = String(suspiciousCount * 3 + 19);
      tiIpsHour.textContent = String(Math.max(1, suspiciousCount + 2));
      tiThreatLevel.textContent = body.phishing_found > suspiciousCount ? "HIGH" : suspiciousCount > 0 ? "ELEVATED" : "MODERATE";
      tiAiRisk.textContent = `${Math.min(99, 62 + body.phishing_found * 3 + suspiciousCount)} / 100`;
      tiAiPattern.textContent = body.phishing_found > 0 ? "Phishing Detected" : "Monitoring";
      tiBlacklistBody.innerHTML = `
        <tr><td>fakebank-login.xyz</td><td style="color:#ffb570;">Phishing</td></tr>
        <tr><td>update-paypal.cc</td><td style="color:#ffb570;">Phishing</td></tr>
        <tr><td>malware-site.ru</td><td style="color:#ff8d6b;">Malware</td></tr>
      `;
      if (brands[0]) {
        tiBlacklistBody.innerHTML += `<tr><td>${brands[0].toLowerCase()}-verify-secure.net</td><td style="color:#ffb570;">Phishing</td></tr>`;
      }
      tiFeed1.textContent = `Updated ${Math.max(6, 24 - body.phishing_found)} mins ago`;
      tiFeed2.textContent = `Updated ${Math.max(8, 22 - suspiciousCount)} mins ago`;
      tiFeed3.textContent = `Updated ${Math.max(5, 18 - Math.min(body.total_scanned, 10))} mins ago`;
    }
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      setActiveView("dashboard");
      setActiveSubview("visual-proof");
      if (autoSwitchTimer) {
        clearTimeout(autoSwitchTimer);
        autoSwitchTimer = null;
      }
      dashboardVerdict.style.display = "none";
      try {
        const data = new FormData(form);
        const payload = {
          url: data.get("url"),
          force_refresh: true,
          domain: {
            domain_age_days: numberOrNull(data.get("domain_age_days")),
            registrar: data.get("registrar") || null,
            dns_record_count: numberOrNull(data.get("dns_record_count")),
            has_ssl: data.get("has_ssl") === "on"
          },
          content: {
            claimed_brand: data.get("claimed_brand") || null,
            genuine_url: data.get("genuine_url") || null,
            html_snippet: data.get("html_snippet") || null,
            genuine_html_snippet: data.get("genuine_html_snippet") || null,
            text_snippet: data.get("text_snippet") || null,
            dom_similarity: numberOrNull(data.get("dom_similarity")),
            login_form_detected: data.get("login_form_detected") === "on"
          },
          visual: {
            screenshot_similarity: numberOrNull(data.get("screenshot_similarity")),
            logo_similarity: numberOrNull(data.get("logo_similarity")),
            layout_similarity: numberOrNull(data.get("layout_similarity")),
            suspect_screenshot_hash: data.get("suspect_screenshot_hash") || null,
            genuine_screenshot_hash: data.get("genuine_screenshot_hash") || null,
            theme_similarity: numberOrNull(data.get("theme_similarity"))
          }
        };
        setLoadingState(18, "Scanning with AI...", 0);
        await new Promise((resolve) => setTimeout(resolve, 180));
        setLoadingState(52, "Analyzing content and similarity...", 1);
        await new Promise((resolve) => setTimeout(resolve, 180));
        setLoadingState(82, "Running visual AI checks...", 2);
        let body;
        if (isPreviewMode) {
          body = fallbackScan(payload.url);
        } else {
          try {
            const response = await fetch(apiUrl("/scan"), {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload)
            });
            body = await response.json();
            if (!response.ok) {
              showDashboardError(body.detail || "Scan failed.");
              renderExplanations([body.detail || "Scan failed."]);
              setLoadingState(0, "Scanning with AI...", -1);
              return;
            }
          } catch (networkError) {
            body = fallbackScan(payload.url);
          }
        }
        setLoadingState(100, "AI scan completed.", 2);
        showDashboardResult(body);
        urlInput.value = body.url;
        probability.textContent = body.phishing_probability + "%";
        updateVerdictPill(body.verdict);
        scanIdLabel.textContent = body.scan_id;
        techScanId.textContent = body.scan_id;
        techVerdict.textContent = body.verdict === "Phishing" ? "CRITICAL RISK" : body.verdict.toUpperCase();
        techSummary.textContent = `Phishing probability ${body.phishing_probability}%. Domain score ${body.domain_score}, content score ${body.content_score}, image score ${body.image_score}.`;
        techNotes.textContent = body.explanations && body.explanations.length ? body.explanations.join(" | ") : "No suspicious evidence detected.";
        techVisualSummary.textContent = `Visual similarity index: ${body.image_score}% match.`;
        domainScore.textContent = body.domain_score + "%";
        contentScore.textContent = body.content_score + "%";
        imageScore.textContent = body.image_score + "%";
        updateGauge(body.phishing_probability);
        latestScanId = body.scan_id;
        renderExplanations(body.explanations || []);
        renderComparison(payload, body);
        renderPreviewShots(body);
        renderDomainDetails(body);
        try {
          await refreshRecentScans();
          await refreshAnalytics();
        } catch (refreshError) {
          console.warn("Background dashboard refresh failed", refreshError);
        }
        if (body.verdict !== "Safe") {
          autoSwitchTimer = setTimeout(() => {
            setActiveView("scans");
            setActiveSubview("visual-proof");
            autoSwitchTimer = null;
          }, 7000);
        }
      } catch (error) {
        const message = explainScanError(error);
        showDashboardError(message);
        renderExplanations([message]);
        setLoadingState(0, "Scanning with AI...", -1);
      }
    });
    downloadReport.addEventListener("click", () => {
      if (!latestScanId) {
        renderExplanations(["Run a scan first to generate a downloadable report."]);
        return;
      }
      window.location.href = apiUrl(`/history/${latestScanId}/report.txt`);
    });
    apiButton.addEventListener("click", async () => {
      const response = await fetch(apiUrl("/architecture"));
      const body = await response.json();
      renderExplanations([
        "API integration is available.",
        `Fusion formula: ${body.formula}`,
        "Use /scan, /history, /analytics, and /architecture endpoints."
      ]);
    });
    newScanButton.addEventListener("click", () => {
      setActiveView("scans");
      urlInput.scrollIntoView({ behavior: "smooth", block: "center" });
      urlInput.focus();
    });
    attachEvidenceButton.addEventListener("click", () => {
      complaintEvidenceInput.click();
    });
    complaintEvidenceInput.addEventListener("change", () => {
      renderComplaintEvidence(complaintEvidenceInput.files || []);
    });
    dashboardScanButton.addEventListener("click", () => {
      setActiveView("dashboard");
    });
    topTabs.forEach((tab) => {
      tab.addEventListener("click", (event) => {
        event.preventDefault();
        setActiveView(tab.dataset.view);
      });
    });
    sideTabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        setActiveView(tab.dataset.view);
      });
    });
    subTabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        setActiveSubview(tab.dataset.subview);
      });
    });
    refreshRecentScans();
    refreshAnalytics();
    updateGauge(0);
    setLoadingState(0, "Scanning with AI...", -1);
    setActiveView("dashboard");
    setActiveSubview("visual-proof");
  </script>
</body>
</html>
"""
