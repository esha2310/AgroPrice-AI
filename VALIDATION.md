# Validation record — 16 October 2026

## Actually run in the authoring environment

- Downloaded WFP/HDX metadata and original CSV; retained source licence and SHA-256.
- Trained and evaluated persistence, seasonal naive, Random Forest and XGBoost on four commodities, with fixed chronological splits. Stored metrics and 2,784 held-out prediction rows across the four methods (696 unique eligible test commodity-market-months).
- `python manage.py check`: passed, zero reported issues.
- `python manage.py test`: 9 tests passed. Checked CSRF rejection, password hashing, weak/duplicate registration rejection, correct/incorrect sign-in, session/logout, watchlist authentication, per-user isolation, duplicate saves, invalid payloads, GET mutation rejection and basic attempt limiting.
- `python manage.py makemigrations --check --dry-run`: no missing migrations.
- `python check_data.py`: passed input checksum, unique series/prediction keys, chronological splits, recomputed MAE, positive finite forecasts, feature causality and missing-month preservation.
- `node check_frontend.cjs`: JavaScript syntax and simulated-DOM rendering across 361 series and all four model choices; comparison, watchlist save, CSV branch and static sign-in branch exercised. This is not a browser screenshot or actual browser interaction test.
- `python manage.py collectstatic --noinput`: collected Django admin static files for production serving.
- Embedded HTML built successfully without placeholders or external JavaScript/CSS dependencies.

## Important result

Persistence was best on validation and test MAE for all four commodities. ML did not demonstrate improvement. The frontend default and documentation report this result. Only 132 series meet both the latest commodity cutoff and lag requirements for a final one-month snapshot forecast.

## Not verified here

- Actual desktop/mobile browser rendering, visual overlap, touch tooltips, local-file storage restrictions, screen-reader behaviour and browser download handling. Browser-control capability was unavailable in this environment; no visual QA or screenshots are claimed.
- GitHub Pages deployment in the user's GitHub account.
- A public Django account server, production HTTPS/proxy behaviour, database restart persistence, Docker build, rate-limit scaling, backups or load tests.
- Independent source-data audit, real-time freshness, live data ingestion, multi-step forecast reliability, causal price explanations or operational accuracy.

## Manual acceptance checklist

Open the live page on desktop and a phone. Test navigation, each filter, no-forecast cases, chart points, two-market comparison, CSV and source rows. Check that date and unit remain visible. Open/close sign-in with mouse and keyboard; inspect dialog scrolling on a small display. In Django, register two separate users, save different markets, sign out/in and confirm isolation. Confirm static preview never collects passwords and Django error messages do not expose secrets. Refresh the live public URL in a private window.

## Botanical design revision — 17 October 2026, Bangladesh time

Reworked the welcome page, entry screen and workspace navigation; added five original decorative SVGs. Compared the original and revised dashboard JSON, selected prices, raw CSV, metrics and predictions byte for byte: unchanged. JavaScript simulated-DOM checks cover welcome → entry → guest workspace and back navigation in addition to all existing data views. The public site is redeployed through Sites; native deployment status verifies publication, not visual quality. Real desktop/mobile browser QA remains unperformed here.

### Fresh-market visual update

Applied the user’s additional grocery/agriculture references through forest/emerald surfaces, cream typography, warm yellow price accents and four original staple illustrations. No grocery sale, discount, delivery claim or additional commodity was added. Existing data and results remain unchanged. Browser visual QA remains unperformed.

## Separate Login/Create Account pages

Built four HTML pages and real Django page routes. Twelve Django tests passed, including separate routes, stored profile name/email, confirmation mismatch rejection and Remember me session policy. JavaScript simulated-DOM tests passed for separate-page navigation, account-page parsing and disabled public-preview inputs. Source-data and model-result files remain byte-identical to the original release. Actual browser visual QA remains unperformed.
