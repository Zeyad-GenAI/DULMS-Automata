import os
import json
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def send_telegram_message(message):
    bot_token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("مشكلة في إرسال رسالة تليجرام:", e)

def run_master_tracker():
    student_id = os.environ.get('STUDENT_ID')
    student_pass = os.environ.get('STUDENT_PASS')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    report_sections = [] 
    
    try:
        print("جاري الدخول للمنصة بحسابك...")
        driver.get("https://dulms.deltauniv.edu.eg/Login.aspx")
        time.sleep(3)
        driver.find_element(By.ID, "txtname").send_keys(student_id)
        driver.find_element(By.ID, "txtPass").send_keys(student_pass + Keys.RETURN)
        time.sleep(5)
        
        # 1. فحص الإعلانات
        print("1. جاري فحص الإعلانات...")
        driver.get("https://dulms.deltauniv.edu.eg/Announcement/AllAnnouncement")
        time.sleep(4)
        
        announcement_elements = driver.find_elements(By.CLASS_NAME, "announce-item")
        ann_file = "announcements_data.json"
        is_first_run_ann = not os.path.exists(ann_file)
        old_announcements = []
        if not is_first_run_ann:
            with open(ann_file, "r", encoding="utf-8") as f:
                old_announcements = json.load(f)

        new_ann_alerts = []
        for element in announcement_elements[:5]: 
            text_content = element.text.strip()
            if not text_content: continue
            lines = text_content.split('\n')
            if len(lines) >= 3:
                sender = lines[0].strip()
                date_time = lines[1].strip()
                content = "\n".join(lines[2:]).strip()
                unique_key = f"{sender} | {date_time}"
                
                if unique_key not in old_announcements:
                    old_announcements.append(unique_key)
                    if not is_first_run_ann:
                        new_ann_alerts.append(f"👤 من: {sender}\n🕒 الوقت: {date_time}\n📝 التفاصيل: {content}")

        if is_first_run_ann:
            report_sections.append("📢 الإعلانات: تم تشغيل البوت لأول مرة وحفظ الإعلانات القديمة.")
        elif new_ann_alerts:
            report_sections.append("📢 إعلانات جديدة:\n\n" + "\n---\n".join(new_ann_alerts))
        else:
            report_sections.append("📢 الإعلانات: مفيش أي إعلانات جديدة.")

        with open(ann_file, "w", encoding="utf-8") as f:
            json.dump(old_announcements[-20:], f, ensure_ascii=False, indent=4)

        # 2. فحص الواجبات
        print("2. جاري فحص الواجبات...")
        driver.get("https://dulms.deltauniv.edu.eg/Assignment/AssignmentStudentList")
        time.sleep(4)
        unsubmitted_assign = driver.find_elements(By.CLASS_NAME, "notsubmitted")
        assign_alerts = []
        for element in unsubmitted_assign:
            if element.text.strip().isdigit() and int(element.text.strip()) > 0:
                try:
                    course = driver.execute_script("return arguments[0].closest('.panel').innerText;", element).split('\n')[0].strip()
                except: course = "مادة غير معروفة"
                assign_alerts.append(f"📌 {course}: {element.text.strip()} متأخر")
                
        if assign_alerts:
            report_sections.append("📝 الواجبات المتأخرة:\n" + "\n".join(assign_alerts))
        else:
            report_sections.append("📝 الواجبات: كله متسلم يا بطل.")

        # 3. فحص الكويزات
        print("3. جاري فحص الكويزات...")
        driver.get("https://dulms.deltauniv.edu.eg/Quizzes/StudentQuizzes")
        time.sleep(4)
        unsubmitted_quiz = driver.find_elements(By.CLASS_NAME, "notsubmitted")
        quiz_alerts = []
        for element in unsubmitted_quiz:
            if element.text.strip().isdigit() and int(element.text.strip()) > 0:
                try:
                    course = driver.execute_script("return arguments[0].closest('.panel').innerText;", element).split('\n')[0].strip()
                except: course = "مادة غير معروفة"
                quiz_alerts.append(f"📌 {course}: {element.text.strip()} متأخر")
                
        if quiz_alerts:
            report_sections.append("⏱️ الكويزات المتأخرة:\n" + "\n".join(quiz_alerts))
        else:
            report_sections.append("⏱️ الكويزات: كله محلول.")

        # 4. فحص الغياب
        print("4. جاري فحص الغياب...")
        driver.get("https://dulms.deltauniv.edu.eg/SemesterWorks/absence")
        time.sleep(5)
        absence_elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Abs:')]")
        
        abs_file = "absence_data.json"
        old_absences = {}
        if os.path.exists(abs_file):
            with open(abs_file, "r", encoding="utf-8") as f:
                old_absences = json.load(f)

        current_absences, abs_reminders, abs_new = {}, [], []
        
        for i, element in enumerate(absence_elements):
            abs_text = element.text.strip()
            try:
                parent_text = element.find_element(By.XPATH, "./../../../../..").text
                course_name = parent_text.split('\n')[0].strip()
                
                preceding_text = driver.execute_script("""
                    var el = arguments[0];
                    var parent = el.parentElement;
                    while(parent && !parent.innerText.includes('Group')) {
                        parent = parent.parentElement;
                    }
                    if(!parent) return "";
                    var html = parent.innerHTML;
                    var parts = html.split(arguments[0].outerHTML);
                    return parts[0];
                """, element)
                
                clean_text = preceding_text.replace("SubGroup", "SUB_G")
                if clean_text.rfind("SUB_G") > clean_text.rfind("Group"):
                    group_label = "سكشن🔬"
                elif clean_text.rfind("Group") > -1:
                    group_label = "محاضرة📚"
                else:
                    group_label = "غير محدد❓"
                    
                unique_key = f"{course_name} - {group_label}"
            except:
                unique_key = f"عنصر غياب رقم {i+1}"
                
            current_absences[unique_key] = abs_text
            
            try:
                parts = abs_text.split()
                current_count = int(parts[1]) 
                total_count = int(parts[3])   
                
                old_abs = old_absences.get(unique_key, "Abs: 0 of 5")
                old_count = int(old_abs.split()[1])
                
                if current_count > 0:
                    abs_reminders.append(f"📌 {unique_key}: {current_count} من {total_count}")
                    if current_count > old_count:
                        abs_new.append(f"⚠️ غياب جديد! {unique_key} بقى {current_count}")
            except: pass

        abs_report = []
        if abs_new: abs_report.append("🚨 إنذار غياب جديد:\n" + "\n".join(abs_new))
        if abs_reminders: abs_report.append("📋 تذكير بإجمالي الغياب:\n" + "\n".join(abs_reminders))
        
        if abs_report:
            report_sections.append("\n".join(abs_report))
        else:
            report_sections.append("🚨 الغياب: ممتاز، مفيش غياب متسجل عليك.")

        with open(abs_file, "w", encoding="utf-8") as f:
            json.dump(current_absences, f, ensure_ascii=False, indent=4)

        # 5. إرسال التقرير المجمع
        print("جاري تجميع وإرسال التقرير النهائي...")
        final_message = "🤖 تقرير DULMS الشامل 🤖\n\n" + "\n\n\n".join(report_sections)
        print(final_message)
        send_telegram_message(final_message)
            
    except Exception as e:
        error_msg = f"⚠️ حصل خطأ غير متوقع أثناء الفحص:\n{e}"
        print(error_msg)
        send_telegram_message(error_msg)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_master_tracker()
