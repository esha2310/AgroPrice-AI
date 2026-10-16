# GitHub ও website চালানোর ধাপ

## ১. ZIP খুলুন

ZIP → right click → **Extract All**। Extract করা folder খুলুন। `index.html`, `manage.py`, `README.md`, `accounts`, `config`, `data`, `assets`, `ml`, `frontend` দেখতে পাবেন। Folder-এর ভেতরের file আলাদা করে এক জায়গায় জড়ো করবেন না।

## ২. Public demo সবার সঙ্গে share করতে

1. GitHub-এ sign in করুন। **New repository** চাপুন।
2. নাম লিখুন: `AgroPrice-AI`। Public বেছে **Create repository** চাপুন।
3. **uploading an existing file** অথবা **Add file → Upload files** চাপুন।
4. শুধু website demo চাইলে **`index.html`, `login.html`, `signup.html`, `dashboard.html`**—চারটি file একসঙ্গে repository root-এ upload করুন। প্রতিটি page-এর প্রয়োজনীয় ছবি embed করা আছে, কিন্তু navigation-এর জন্য চারটি file-ই রাখতে হবে।
5. Commit message: `Add AgroPrice AI website demo` → **Commit changes**।
6. Repository **Settings → Pages** খুলুন।
7. Source: **Deploy from a branch** → Branch: **main** → Folder: **/(root)** → Save।
8. Deployment শেষ হলে Pages-এ দেখানো URL খুলুন। সাধারণ format: `https://YOUR_USERNAME.github.io/AgroPrice-AI/`। নিজের username বসাবেন; এখানে দেওয়া format কোনও নিশ্চিত live link নয়।
9. ফোন ও private/incognito window দিয়ে filter, chart, CSV download এবং watchlist পরীক্ষা করুন।

এই demo-তে account server নেই। Sign in screen এই সীমা জানায়; password সংগ্রহ করে না। Real registration/login চাইলে নিচের full project ও server deployment ব্যবহার করুন।

## ৩. পুরো project GitHub-এ রাখুন

- Extract করা folder-এর **ভেতরের** সব source files ও folders upload করুন, directory structure ঠিক রেখে। ZIP file-টাই code হিসেবে upload করবেন না।
- `accounts/migrations/0001_initial.py` অবশ্যই `accounts/migrations/`-এর ভেতরে থাকবে; root-এ নয়।
- `config/settings.py` থাকবে `config/`-এ। Data ও ছবি তাদের নিজস্ব folder-এ রাখুন।
- `.venv`, `.env`, `db.sqlite3`, `__pycache__` বা নিজের passwords upload করবেন না। Package-এ কোনও account database নেই।
- Browser দিয়ে hidden folders upload কঠিন হলে GitHub Desktop ব্যবহার করুন: repository clone → extracted project files clone folder-এ copy → changes review → Commit → Push origin। `.gitignore` sensitive local files বাদ দেয়।

Description:

> Bangladesh food-price exploration with transparent one-month forecasting, market comparisons and a nature-inspired interface. Includes a static website and optional Django accounts.

Commit message:

> Add AgroPrice AI analytics website and reproducible forecasting project

## ৪. Local full app চালান

VS Code → File → Open Folder → extract করা project folder → Terminal → New Terminal। একবারে একটি command দিন:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Browser-এ `http://127.0.0.1:8000/` খুলুন। Sign in → Create an account দিয়ে নিজের account বানান। অন্য ফোনে Internet দিয়ে ব্যবহার করতে localhost যথেষ্ট নয়; HTTPS server hosting লাগবে।

## ৫. Update করার নিয়ম

- Design বা text বদলাতে `frontend/site.html` edit করুন।
- `python build_demo.py` চালিয়ে চারটি HTML page নতুন করে বানান।
- শুধু HTML edit করলে পরের build-এ সেই পরিবর্তন হারাবে।
- নতুন data আনলে source, licence, cutoff এবং checksum আবার যাচাই করে `ml/train.py` চালান; তারপর build করুন। পুরোনো metrics রেখে নতুন data-এর performance দাবি করবেন না।

## নতুন design update

Welcome page → Explore the prices → entry screen → Continue as a guest—এই ক্রমে demo দেখুন। Public HTML password নেয় না; Django server-এ real signup/login পাওয়া যায়। শুধু website publish করতে চারটি নতুন HTML page root-এ upload করে matching পুরোনো files replace করুন। পুরো project update করলে folders-এর অবস্থান ঠিক রাখুন, `.venv` ও নিজের `db.sqlite3` replace বা upload করবেন না।
