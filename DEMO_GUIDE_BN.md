# পাঁচ মিনিটের demo

শুরুতে **Explore the prices** চাপুন। Entry screen-এ public preview-এর সীমা পড়ে **Continue as a guest** চাপুন। Server version-এ চাইলে আগে account তৈরি ও sign in করতে পারবেন।

1. Homepage-এ Bangladesh-এর ধানক্ষেত, four staples এবং snapshot-এর শেষ মাস দেখান। বলুন: “এগুলো আজকের live দোকানের দাম নয়; source-এর মাস অনুযায়ী দেখা যাচ্ছে।”
2. **Price explorer** খুলুন। Commodity, Division ও Market বদলান। Chart-এর point-এ mouse রাখুন; ফোনে tap করুন। **View source rows**-এ exact values ও flag দেখান।
3. একই পণ্যের অন্য market compare করুন। Unit একই থাকার সুবিধা বোঝান। ভিন্ন market-এর সব দাম একই মাসে নেই—gap লুকানো হয় না।
4. Forecast method থেকে Persistence, Random Forest ও XGBoost বদলান। Evidence table দেখিয়ে বলুন: “এই পরীক্ষায় আগের মাসের দাম ধরে রাখা baseline-ই কম ভুল করেছে।”
5. **Save to watchlist**, তারপর **Download history CSV** চাপুন। Static version-এ browser-local saves; server version-এ sign-in করা থাকলে account-specific saves।
6. Sign in screen দেখান। Static preview account তৈরি করে না। Full Django server-এ **Create an account**, sign out এবং sign in দেখাতে পারবেন। নিজের password share করবেন না।

## যা দাবি করবেন না

- “সব বাজারের বর্তমান দাম আছে।”
- “AI সঠিক দাম নিশ্চিত করে / 99% accurate।”
- “ML baseline-এর চেয়ে ভালো”—এই snapshot-এ ফল উল্টো।
- “Forecast interval validated”—এখানে interval নেই।
- “কৃষককে কখন কিনতে/বিক্রি করতে হবে বলে দেয়।”

## পেশাদারভাবে বলতে পারেন

“AgroPrice AI একটি Bangladesh-focused food-price exploration ও forecasting project। WFP-এর dated data ব্যবহার করে বাজারভেদে history ও reproducible one-month model comparisons দেখায়। বাস্তব forecast skill মাপার জন্য temporal validation/test রাখা হয়েছে; বর্তমান পরীক্ষায় persistence baseline সেরা হওয়ায় সেটিই default।”
