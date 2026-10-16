# Deployment options

## Static public website

GitHub Pages serves `index.html`, `login.html`, `signup.html` and `dashboard.html` together from the repository root. It has the complete price exploration UI, frozen predictions and browser-local saves. No Python process, API secret, model server or database is needed. This version does **not** register users or authenticate passwords. Its separate Login and Create Account pages show disabled fields and explain that an account server is required.

Public static hosting does not make the dataset live. The displayed date remains the source cutoff. Hosting availability and quotas are controlled by the provider.

## Full Django website with actual accounts

Use a Python/Docker host with HTTPS and a persistent volume. The included Dockerfile runs Gunicorn, not Django's development server. A host account or paid service is not created by this package. We do not promise permanently free backend hosting or durable storage on free tiers.

Required environment variables:

- `DEBUG=0`
- `SECRET_KEY`: unique random secret, at least 40 characters; generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"` and store in host secrets, never Git.
- `ALLOWED_HOSTS`: comma-separated exact hostnames, without scheme, such as `agroprice.example.org`.
- `CSRF_TRUSTED_ORIGINS`: exact HTTPS origins, such as `https://agroprice.example.org`.
- `DATA_DIR=/var/lib/agroprice`; mount persistent storage there for SQLite.
- `TRUST_PROXY=1` only when a controlled HTTPS reverse proxy strips client-supplied forwarded headers and sets `X-Forwarded-Proto` itself. Otherwise leave 0 and configure HTTPS correctly at the application boundary.

`.env.example` is documentation, not an automatically loaded environment file. Do not deploy with its placeholder values.

Typical Docker process:

```bash
docker build -t agroprice-ai .
```

Configure the environment using your platform's secret manager, mount a volume at `/var/lib/agroprice`, route HTTPS to container port 8000, then start it. Startup applies migrations and runs Gunicorn. WhiteNoise serves bundled Django admin static assets collected at build time. The product page has embedded images/styles/data.

For an initial deployment, create a superuser with the platform's shell:

```bash
python manage.py createsuperuser
```

Do not expose DEBUG=1, use a hardcoded secret, or share a superuser account. Validate registration/login/logout, CSRF, cross-user watchlist separation, cookies, restart persistence and database backups on the actual host. Basic in-memory attempt throttling is per process; before a broad public account rollout add a shared atomic limiter at the reverse proxy or application layer. SQLite is intended for a small single-host deployment; move to a properly configured persistent PostgreSQL service before multi-instance or heavier usage. Database failover, email recovery and monitoring are not supplied.

## Release checks

1. Run `python manage.py check`, `python manage.py test`, `python check_data.py`, `node check_frontend.cjs`.
2. Set production environment securely and run `python manage.py check --deploy`.
3. Test at phone and desktop widths, keyboard navigation, chart readability and sign-in dialog scroll.
4. Open the actual HTTPS URL in an incognito browser and on a phone.
5. Do not call it a live-market feed. Do not call the ML models more accurate than persistence; the supplied results show otherwise.

The backend tests ran locally in the authoring environment. A public account server has not been provisioned or load-tested by this package.
