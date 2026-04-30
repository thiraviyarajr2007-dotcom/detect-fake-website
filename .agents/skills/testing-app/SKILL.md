# Testing PhishGuard AI (detect-fake-website)

## Local Setup

1. Install dependencies: `pip install -e .`
2. Start the server: `python run_app.py` (runs on `http://127.0.0.1:8000`)
3. The app uses SQLite — a `scan_history.db` file is created automatically in the working directory.
4. No CI is configured on this repo. Run tests manually: `python -m pytest tests/ -v` (expect 31 tests).

## Architecture

- **FastAPI app** defined in `url_scanner/api.py` via `create_app()` factory
- **Dashboard HTML** is generated in Python via `url_scanner/dashboard.py` — all UI is a single-page app embedded in one large HTML string
- **Login page** is in `url_scanner/login_page.py`
- **Auth system** uses SQLite tables (`users`, `sessions`) managed by `url_scanner/auth.py`
- Session cookies are httponly with 72-hour TTL

## Auth Testing

- Unauthenticated requests to `/` redirect to `/login` (302)
- Register: Click "Register" tab → fill username, email, password (min 6 chars), confirm password → "Create Account"
- On successful registration, user is auto-logged-in and redirected to dashboard
- Login: Fill username + password on Sign In tab → "Sign In"
- Logout: Click "Logout" in the sidebar → redirects to `/login`
- Wrong password shows: "Invalid username or password"
- Short password shows: "Password must be at least 6 characters."
- Mismatched passwords show: "Passwords do not match."

## Dashboard Navigation

- **Sidebar flow-steps**: Home, Live Feed, Threat Intel, Raise Complaint, Support, Logout
- **Top tabs**: Dashboard, Scans, Settings, API
- Each section has a `data-view` attribute that controls which view is active
- The logged-in username appears in the sidebar as `.agent-name` in uppercase

## Button Testing Checklist

| Button | Location | Expected Behavior |
|--------|----------|-------------------|
| Scan Now | Dashboard | Scans entered URL, shows verdict + risk scores |
| Scan URL for Threats | Threat Intel | Switches to Dashboard view, focuses URL input |
| View All Alerts | Threat Intel | Loads phishing/suspicious scans from `/history` |
| Manage Blacklist | Threat Intel | Populates blacklist table from scan history |
| Blacklist Domain | Technical Intel | Adds scanned domain to blacklist table |
| Full Traceroute | Technical Intel | Shows simulated traceroute output |
| Submit Complaint | Raise Complaint | Validates URL, type, description; shows summary alert; clears form |
| API Key Toggle | API tab | Reveals/hides key starting with "pgai_" |
| API Key Copy | API tab | Copies key to clipboard (or shows in alert) |
| Regenerate Key | API tab | Generates new random key |
| Documentation | API tab | Shows API endpoint reference in Scans view |
| Export CSV | Settings | Downloads scan history as CSV via `/history/export.csv` |
| Export PDF | Settings | Generates text audit report as download |
| Settings Switches | Settings | Toggle on/off with visual feedback (class "on") |
| Logout | Sidebar | POST `/auth/logout`, redirect to `/login` |

## API Endpoints (for programmatic testing)

- `POST /scan` — body: `{"url": "https://example.com"}` — scan a URL
- `GET /history` — retrieve all scan history
- `GET /history/export.csv` — export as CSV
- `POST /auth/register` — body: `{"username": "...", "email": "...", "password": "..."}`
- `POST /auth/login` — body: `{"username": "...", "password": "..."}`
- `POST /auth/logout` — clears session
- `GET /auth/me` — returns current user info

## Tips

- The dashboard is a single-page app — all views are in one HTML document, toggled by JS. Navigation doesn't change the URL.
- The scan DB might already have data from previous test runs. "View All Alerts" filters for Phishing/Suspicious verdicts.
- If no scans exist yet, "View All Alerts" shows "No threat alerts yet. Scan some URLs first."
- Complaint form requires all of: URL, complaint type (not default), and description.
- Browser session cookies persist across restarts if using `--user-data-dir`.

## Devin Secrets Needed

No secrets are required. The app runs fully locally with SQLite.
