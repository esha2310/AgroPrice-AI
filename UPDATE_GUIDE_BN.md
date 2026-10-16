# নতুন design চালানোর সহজ নিয়ম

1. নতুন ZIP-এ **Extract All** দিন।
2. Extract করা চারটি HTML পাশাপাশি রেখে `index.html` double-click করুন। কোনও installation লাগে না।
3. Welcome page-এ **Explore the prices** চাপুন; entry screen থেকে **Continue as a guest** চাপুন।
4. GitHub Pages update করতে root-এ `index.html`, `login.html`, `signup.html`, `dashboard.html`—চারটি নতুন file upload/replace করে Commit করুন।
5. পুরো Django project update করলে নতুন source files ও folders আগের project folder-এ একই অবস্থানে copy করুন। `.venv`, `.env`, নিজের `db.sqlite3` ও ব্যক্তিগত তথ্য রাখুন; GitHub-এ দেবেন না।
6. VS Code Terminal-এ চলন্ত server **Ctrl+C** দিয়ে বন্ধ করুন। তারপর চালান:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

7. `http://127.0.0.1:8000/` খুলুন। পুরোনো design দেখালে **Ctrl+F5** দিন।

Public static demo-তে password নেওয়া বা account তৈরি করা হয় না। Full Django server-এ registration/login ও account watchlist কাজ করে। আগের data ও model results অপরিবর্তিত। Browser/mobile layout এই environment-এ visually পরীক্ষা করা যায়নি।
