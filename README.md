# 🎓 DULMS Auto-Tracker Bot 🚀

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-Web_Scraping-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/Automated_by-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Open Source](https://img.shields.io/badge/Open_Source-100%25-success?style=for-the-badge)

أداة برمجية ذكية ومفتوحة المصدر، مصممة خصيصاً لطلاب **جامعة الدلتا للعلوم والتكنولوجيا (Delta University)**. 
تعمل الأداة كمساعد شخصي آلي (Bot) يقوم بمراقبة حسابك الجامعي على منصة DULMS على مدار الساعة، ويرسل لك إشعارات فورية على Telegram فور حدوث أي تحديث جديد.

---

## ✨ المميزات الأساسية (Features)

* **📝 رادار التكليفات (Assignments):** يكتشف أي واجبات جديدة لم تقم بتسليمها ويرسل لك عددها.
* **⏱️ قناص الاختبارات (Quizzes):** ينبهك فوراً بوجود اختبارات (Quizzes) مفتوحة تحتاج للحل.
* **🧠 المتابعة الذكية للغياب (Smart Absence Tracker):** لا يكتفي بعدّ الغياب فقط، بل يحلل البيانات ليخبرك بـ:
  * اسم المادة التي سجلت غياباً جديداً.
  * نوع الغياب (محاضرة نظري 📚 أم سكشن عملي 🔬).
  * نسبة الغياب الحالية مقارنة بالحد الأقصى.
* **⚡ أتمتة كاملة (100% Automated):** تعمل الأداة في الخلفية (Cloud) كل 4 ساعات عبر خوادم GitHub، ولا تحتاج لتشغيل جهازك أو فتح المتصفح.

---

## 🔒 الأمان والخصوصية (Privacy & Security)

**أمان بياناتك هو الأولوية القصوى.**
تم تصميم هذه الأداة لتعمل بشكل "لامركزي". أنت تقوم بنسخ الكود إلى حسابك الشخصي على GitHub، وتعمل الأداة على خوادمك الخاصة. 
* يتم حفظ الرقم الجامعي وكلمة المرور في **قبو مشفر (GitHub Secrets)**.
* المطور أو أي شخص آخر **لا يملك أي صلاحية** للوصول إلى بياناتك أو رسائلك.

---

## ⚙️ دليل التشغيل (Setup Guide)

لست بحاجة لخبرة برمجية لتشغيل الأداة! فقط اتبع هذه الخطوات التي ستنفذها **لمرة واحدة فقط**:

### 1️⃣ إعداد بوت تليجرام (Telegram Setup)
1. افتح تطبيق Telegram وابحث عن البوت `@BotFather` وأرسل له أمر `/newbot`.
2. اختر اسماً للبوت، وسيرسل لك كود مرور (Token) طويل. **(انسخه واحتفظ به)**.
3. ابحث عن اسم البوت الذي أنشأته للتو، وأرسل له أمر `/start` لتفعيل المحادثة.
4. ابحث في Telegram عن البوت `@userinfobot` وأرسل له أي رسالة، سيعطيك رقم المعرف الخاص بك (ID). **(انسخه واحتفظ به)**.

### 2️⃣ استنساخ المشروع (Forking the Repository)
1. قم بتسجيل الدخول إلى حسابك المجاني في [GitHub](https://github.com).
2. في أعلى يمين هذه الصفحة، اضغط على زر **Fork** ثم **Create fork** لإنشاء نسخة خاصة بك من المشروع.

### 3️⃣ ضبط صلاحيات الذاكرة (Workflow Permissions)
*هذه الخطوة هامة جداً لكي تتذكر الأداة الغياب القديم ولا ترسل لك إشعارات متكررة.*
1. داخل نسختك من المشروع، اذهب إلى الإعدادات **Settings** ⚙️.
2. من القائمة الجانبية، اختر **Actions** ثم **General**.
3. انزل لأسفل إلى قسم **Workflow permissions**، اختر **Read and write permissions** واضغط على زر الحفظ **Save**.

### 4️⃣ إضافة بياناتك للـقبو السري (GitHub Secrets)
1. من نافذة الإعدادات **Settings** ⚙️، اختر **Secrets and variables** ثم **Actions**.
2. اضغط على الزر الأخضر **New repository secret** وقم بإضافة البيانات الأربعة التالية (واحدًا تلو الآخر):
   * `STUDENT_ID` : اكتب رقمك الجامعي.
   * `STUDENT_PASS` : اكتب كلمة المرور الخاصة بمنصة DULMS.
   * `BOT_TOKEN` : اكتب التوكن الخاص ببوت تليجرام (من الخطوة 1).
   * `CHAT_ID` : اكتب معرف تليجرام الخاص بك (من الخطوة 1).

### 5️⃣ إطلاق الأداة (First Run)
1. اذهب إلى تبويب **Actions** في أعلى صفحة المستودع.
2. اضغط على الزر الأخضر **I understand my workflows, go ahead and enable them**.
3. من القائمة الجانبية اليسرى، اختر `DULMS Auto Tracker`.
4. على اليمين، اضغط على **Run workflow** ثم الزر الأخضر الداخلي لتشغيل الأداة لأول مرة.

🎉 **انتهينا!** ستصلك الآن أول رسالة تقرير على Telegram، وستستمر الأداة بمراقبة المنصة تلقائياً من أجلك.

---

### 👨‍💻 التطوير (Developed By)
تم التطوير بواسطة **Zeyad Mohamed Said Elfaramawy** *AI Engineering Student @ Delta University* *📧 للتواصل أو الإبلاغ عن مشكلة، يمكنك فتح `Issue` في المستودع.*
