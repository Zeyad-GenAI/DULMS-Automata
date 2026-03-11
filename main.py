import os
import json
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# جلب البيانات من الخزنة السرية
STUDENT_ID = os.environ.get('STUDENT_ID')
STUDENT_PASS = os.environ.get('STUDENT_PASS')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("خطأ: التوكن أو الـ Chat ID غير متوفرين.")
        return
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}'
    try:
        requests.get(url)
    except Exception as e:
        print(f"مشكلة في إرسال رسالة تليجرام: {e}")

def run_tracker():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    all_alerts = [] # قائمة مجمعة لكل التنبيهات
    
    try:
        # 1. تسجيل الدخول
        print("جاري تسجيل الدخول لمنصة DULMS...")
        driver.get("https://dulms.deltauniv.edu.eg/Login.aspx")
        time.sleep(3)
        driver.find_element(By.ID, "txtname").send_keys(STUDENT_ID)
        driver.find_element(By.ID, "txtPass").send_keys(STUDENT_PASS + Keys.RETURN)
        time.sleep(5)
        
        # 2. فحص الواجبات (Assignments)
        print("جاري فحص الواجبات...")
        driver.get("https://dulms.deltauniv.edu.eg/Assignments/StudentAssignments")
        time.sleep(4)
        unsubmitted_assignments = driver.find_elements(By.CLASS_NAME, "notsubmitted")
        total_assign = sum(int(el.text.strip()) for el in unsubmitted_assignments if el.text.strip().isdigit())
        if total_assign > 0:
            all_alerts.append(f"📝 **الواجبات:** يوجد لديك {total_assign} تكليف لم يتم تسليمه.")

        # 3. فحص الكويزات (Quizzes)
        print("جاري فحص الكويزات...")
        driver.get("https://dulms.deltauniv.edu.eg/Quizzes/StudentQuizzes")
        time.sleep(4)
        unsubmitted_quizzes = driver.find_elements(By.CLASS_NAME, "notsubmitted")
        total_quizzes = sum(int(el.text.strip()) for el in unsubmitted_quizzes if el.text.strip().isdigit())
        if total_quizzes > 0:
            all_alerts.append(f"⏱️ **الكويزات:** يوجد لديك {total_quizzes} اختبار لم يتم حله.")

        # 4. فحص الغياب (Absence)
        print("جاري فحص الغياب...")
        driver.get("https://dulms.deltauniv.edu.eg/SemesterWorks/absence")
        time.sleep(5)
        absence_elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Abs:')]")
        
        file_path = "absence_data.json"
        old_absences = {}
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                old_absences = json.load(f)

        current_absences = {}
        absence_alerts = []

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
                    group_label = "سكشن (عملي)"
                elif clean_text.rfind("Group") > -1:
                    group_label = "محاضرة (نظري)"
                else:
                    group_label = "غير محدد"
                    
                unique_key = f"{course_name} - {group_label}"
            except:
                unique_key = f"عنصر غياب رقم {i+1}"
                course_name = unique_key
                group_label = ""
                
            current_absences[unique_key] = abs_text
            
            try:
                parts = abs_text.split()
                current_count = int(parts[1]) 
                total_count = int(parts[3])   
                old_abs = old_absences.get(unique_key, "Abs: 0 of 5")
                old_count = int(old_abs.split()[1])
                
                if current_count > 0 and current_count > old_count:
                    absence_alerts.append(f"- {course_name} ({group_label}): {current_count} من {total_count}")
            except:
                pass

        if absence_alerts:
            all_alerts.append("🚨 **غياب جديد تم تسجيله:**\n" + "\n".join(absence_alerts))

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(current_absences, f, ensure_ascii=False, indent=4)

        # 5. إرسال التقرير النهائي
        if all_alerts:
            final_message = "🤖 تقرير DULMS Tracker:\n\n" + "\n\n".join(all_alerts)
            print("يوجد تحديثات، جاري إرسال الرسالة...")
            send_telegram_message(final_message)
        else:
            print("لا توجد أي مهام متأخرة أو غياب جديد.")
            
    except Exception as e:
        print(f"حدث خطأ غير متوقع: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tracker()
