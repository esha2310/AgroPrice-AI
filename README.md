# AgroPrice AI — Agricultural Market Intelligence

A Bangladesh-inspired website and reproducible food-price forecasting project by **Nafisa Tasneem Esha**. Forest green, warm ivory, harvest gold, real licensed paddy-field photography and responsive layouts.

## Website design and entry flow

The revised interface opens on an organized welcome page with bold cream-on-forest-green typography, warm yellow accents, real Bangladesh paddy-field photographs and original crop illustrations. Four white staple cards show the original dated sample-median prices, not offers or discounts. **Explore the prices** opens a dedicated entry screen. On the public static site, **Enter your market workspace** continues without collecting passwords. On Django, this screen also provides real registration and sign-in. Dashboard navigation opens the price workspace; **Welcome page** returns to the landing page.

Public website: https://agroprice-ai.mahmudulhasankoci.chatgpt.site

The visual update preserves the original data JSON, selected CSV, source snapshot, metrics and held-out predictions byte for byte. No prices, model results or cutoff dates were changed.

## What works

- Four static pages (`index.html`, `login.html`, `signup.html`, `dashboard.html`) with embedded assets: market and commodity filters, monthly history, chart point tooltips, comparison of two markets, source-row table and CSV export.
- Rice (coarse), masur lentils, wheat flour and palm oil; fixed BDT/KG or BDT/L units.
- Browser-local watchlist in the static website. Optional real Django registration, login/logout and per-user database watchlist in the server version.
- Precomputed, reproducible one-month point forecasts from persistence, seasonal naive, Random Forest and XGBoost. The website displays frozen outputs, not on-demand retraining or an AI chatbot.
- Validation-selected default, held-out errors and visible missing/stale-history states. No invented prices, accuracy percentage, prediction interval or economic-cause explanation.

## Data and scope

Source: [WFP food prices for Bangladesh via HDX](https://data.humdata.org/dataset/wfp-food-prices-for-bangladesh), [CC BY-IGO 3.0](https://creativecommons.org/licenses/by/3.0/igo/legalcode). Snapshot retrieved **16 October 2026**. Included source metadata and SHA-256 make the frozen input identifiable.

Original input: 34,468 rows. Selected: **13,450 monthly records, 361 commodity-market series, 103 distinct market IDs**. Latest selected month: **August 2026**; rice, lentils and palm oil stop in July 2026. Some markets stop much earlier. This is not a live-price service and does not cover every Bangladesh market. Wheat **flour** is not wheat grain. Palm oil is not soybean oil.

Rows are Retail/BDT with exact commodity and unit filters; `Division` pseudo-markets are excluded. WFP flags are retained: 4,285 `actual`, 9,162 `aggregate`, 3 `actual,aggregate` rows. Aggregate does not mean an individually observed shop quote. Missing monthly observations are not filled. Data can contain source errors or unusual prices; no unexplained manual outlier correction is made. Card medians use only markets reporting the commodity's latest month; changing coverage can change those medians. They are not representative national price estimates.

### Actual model results

MAE = mean absolute error in BDT per unit; lower is better. Chronological six-calendar-month validation and twelve-calendar-month test windows per commodity, with only rows having all exact lags eligible. Some test-window months have no eligible rows. Metrics below were run on this snapshot, not promised performance.

| Commodity | Unit | Persistence MAE | Random Forest MAE | XGBoost MAE |
|---|---|---:|---:|---:|
| Rice, coarse | KG | 0.7396 | 0.9555 | 0.9367 |
| Lentils, masur | KG | 1.9153 | 3.3610 | 3.1686 |
| Wheat flour | KG | 2.5039 | 2.9857 | 2.7925 |
| Palm oil | L | 3.0909 | 3.8577 | 4.5097 |

**Persistence won validation and test MAE for all four commodities.** The default therefore keeps last month's price unchanged. RF and XGBoost are implemented, trained and compared; they are not presented as superior. See `evidence/model_metrics.csv`, `evidence/holdout_predictions.csv` and `evidence/MODEL_CARD.md`.

## Open the website immediately

Extract the entire website ZIP, keeping **`index.html`, `login.html`, `signup.html` and `dashboard.html` together**. Double-click `index.html`. Page assets are embedded, but all four files are needed for page navigation. No CDN or installation is needed. Login in this static preview explains that an account server is required and does not collect a password. Watchlists are browser-local, may be cleared by the browser, and do not send alerts. Local-file browser storage behaviour can vary; GitHub Pages is the recommended shareable static version.

## Run the complete server version on Windows

Extract the ZIP. Open the extracted folder in VS Code and choose **Terminal → New Terminal**. The current folder must contain `manage.py`.

Run each command separately, without copying terminal prompts:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Keep the terminal running. Choose **Sign in → Create an account**. No default username or password is bundled. Account passwords are hashed by Django; CSRF-protected POST endpoints create accounts, sign in/out and modify watchlists. Anonymous saves remain local; signing in shows account saves and does not automatically import anonymous saves.

Optional administration:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Open `/admin/`. On macOS/Linux use `python3 -m venv .venv` and `.venv/bin/python` instead.

## Reproduce the data and models

The raw WFP CSV is bundled under its own source licence. There are no paid APIs or API keys.

```powershell
.\.venv\Scripts\python.exe ml\train.py
.\.venv\Scripts\python.exe build_demo.py
.\.venv\Scripts\python.exe check_data.py
.\.venv\Scripts\python.exe ml\forecast.py --commodity rice --market Barisal
```

Training recreates selected rows, metrics, all held-out predictions, eight fitted model files and the dashboard JSON. It may take several minutes. `build_demo.py` builds all four HTML files with embedded assets. The dashboard JSON is unchanged. Source templates are `frontend/site.html`, `frontend/login.html` and `frontend/signup.html`.

Pinned build versions are recorded in `evidence/environment.txt`; `requirements.txt` uses compatible ranges for installation. Exact ranks or values may vary on different library versions. Serialized joblib models must only be loaded from a trusted local build; the website does not deserialize them at request time.

## Verification

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe check_data.py
node check_frontend.cjs
```

Node is optional and only used for the JavaScript check. `VALIDATION.md` distinguishes tests actually run from browser checks still needed.

## Share and deploy

See **`GITHUB_UPLOAD_BN.md`** for folder-safe upload and GitHub Pages. Pages hosts the static website only. It cannot run Django or account authentication. See **`DEPLOYMENT.md`** for the server version and persistent storage requirements. A Pages or server URL only works after that service successfully deploys it. This package itself does not create a repository in your GitHub account.

## Boundaries

This is an educational analytics project, not an official government service, buying/selling recommendation or guarantee of future prices. Source revisions, changing market coverage and sudden price shocks limit the evidence. Existing forecasts are dated to the dataset cutoff; the app never changes that cutoff to today's date. Forecasts are issued only for markets reaching the commodity cutoff with all required lags (132 series in this snapshot). Older or incomplete market series have no forecast. There are no automatic updates, price alerts, payments or SMS features.

Server registration has basic single-process attempt throttling, not a production-grade shared limiter. Before broad use add durable backups, monitoring, a shared atomic rate limiter and account recovery/deletion flows. No recovery emails or password-reset service is implemented. Admins can delete accounts and their associated watchlists through Django admin. Hosting costs and persistence depend on your provider.

Code licence: MIT. Data and photographs retain their separate licences; see **`DATA_AND_IMAGE_CREDITS.md`**.

## Separate account pages

The botanical Login and Create Account designs are separate URLs, not tabs of one modal. Server routes are `/login/`, `/signup/` and `/dashboard/`; static counterparts use `.html`. Registration stores the submitted full name and email on Django’s user record, uses a distinct username for sign-in, and checks confirmation when supplied. Remember me chooses a seven-day session; otherwise a browser-session cookie is used. Closing a browser may not end its restored session in every browser. No Google/Facebook authentication or email recovery service is configured. Public preview fields are disabled and guest entry remains available.
