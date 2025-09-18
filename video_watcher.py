from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# --- 配置部分 ---
LOGIN_URL = "https://kunpeng.askpcb.com/login.html"  # 替换为你的实际登录页URL
VIDEO_URL = "https://kunpeng.askpcb.com/kng/#/course/play?kngId=8f98a028-49f0-49d8-8062-7e2cbfad0ce2&projectId=&btid=&gwnlUrl=&locateshare=dd8bbb9f-fcab-4b3e-b287-8af038056833" # 替换为你想看的视频页面URL
CHROMEDRIVER_PATH = "E:\chromedriver-win64\chromedriver.exe" # 如果没加到PATH，需要指定驱动路径
WATCH_TIME_SECONDS = 300  # 计划观看时长（秒）
# ---------------

# 👇 替换为你的真实账号密码
USERNAME = "2401002"
PASSWORD = "028736"


# ---------------
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

try:
    # 1️⃣ 打开登录页
    driver.get(LOGIN_URL)
    print("✅ 登录页面已加载")
    time.sleep(2)

    # ⚠️ 备选方案：直接点击隐藏的 checkbox input（不推荐，可能被遮挡）
    try:
        agree_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//label[@class="yxt-checkbox core-custom-checkbox"]//span[contains(text(), "已阅读并同意")]'))
        )
        # 使用 JavaScript 点击（绕过 Selenium 原生点击限制）
        driver.execute_script("arguments[0].click();", agree_element)
        print("✅ 已通过 JS 点击同意隐私政策")
    except Exception as e:
        print(f"⚠️ JS点击同意条款失败: {e}")
        driver.save_screenshot("js_click_error.png")  # 截图留证

    # 2️⃣ 定位用户名输入框 —— 使用 placeholder 或 class 定位（因为 name="username" 有歧义）
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="请输入员工邮箱/账号"]'))
    )
    username_field.clear()
    username_field.send_keys(USERNAME)
    print("✅ 已输入用户名")

    # 3️⃣ 定位密码输入框 —— 使用 type="password" + class 定位
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="password" and @class="yxtf-input__inner yxtf-input__inner--border"]'))
    )
    password_field.clear()
    password_field.send_keys(PASSWORD)
    print("✅ 已输入密码")
    
    # ✅ 终极方案：手动派发 mousedown -> mouseup -> click 事件
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[span/span[text()="登 录"]]'))
        )

        # 滚动到按钮
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_button)
        time.sleep(1)

        # 手动派发三个事件（模拟真实点击）
        driver.execute_script("""
            var btn = arguments[0];
            // 模拟鼠标按下的事件
            var evt1 = new MouseEvent('mousedown', {
                bubbles: true,
                cancelable: true,
                view: window,
                clientX: btn.getBoundingClientRect().left + btn.offsetWidth / 2,
                clientY: btn.getBoundingClientRect().top + btn.offsetHeight / 2
            });
            btn.dispatchEvent(evt1);

            // 模拟鼠标抬起的事件
            var evt2 = new MouseEvent('mouseup', {
                bubbles: true,
                cancelable: true,
                view: window,
                clientX: btn.getBoundingClientRect().left + btn.offsetWidth / 2,
                clientY: btn.getBoundingClientRect().top + btn.offsetHeight / 2
            });
            btn.dispatchEvent(evt2);

            // 模拟点击事件（通常由 mousedown+mouseup 触发）
            var evt3 = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window,
                clientX: btn.getBoundingClientRect().left + btn.offsetWidth / 2,
                clientY: btn.getBoundingClientRect().top + btn.offsetHeight / 2
            });
            btn.dispatchEvent(evt3);
        """, login_button)

        print("✅ 已模拟完整鼠标事件点击登录按钮")
    except Exception as e:
        print(f"❌ 模拟鼠标事件失败: {e}")
        driver.save_screenshot("mouse_events_fail.png")
        raise

#     # 5️⃣ 等待登录跳转完成（比如URL变化或出现某个元素）
#     try:
#         home_link = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, '//a[@href="/main/#/index" and contains(text(), "首页")]'))
#         )
#         print("✅ 登录成功！检测到‘首页’链接")
#     except Exception as e:
#         print(f"❌ 登录失败：未检测到‘首页’元素，可能账号密码错误或网络问题")
#         driver.save_screenshot("login_failed_no_home.png")
#         raise  # 停止脚本，方便调试

#     # 6️⃣ 跳转到视频页面
#     driver.get(VIDEO_URL)
#     print("🎬 视频页面已加载")
#     time.sleep(5)

#     # 7️⃣ 尝试播放视频（原有逻辑，根据你视频页元素修改）
#     try:
#         play_button = driver.find_element(By.XPATH, '//button[contains(text(), "播放")]')  # 示例，需根据实际修改
#         play_button.click()
#         print("▶️ 播放按钮已点击")
#     except Exception as e:
#         print(f"⚠️ 未找到播放按钮: {e}")

#     # 8️⃣ 保持观看...
#     WATCH_TIME_SECONDS = 300
#     print(f"⏳ 开始观看视频，计划时长 {WATCH_TIME_SECONDS} 秒...")
#     start_time = time.time()
#     while time.time() - start_time < WATCH_TIME_SECONDS:
#         driver.execute_script("window.scrollBy(0, 1);")
#         time.sleep(random.randint(10, 30))
#         print(f"⏱️ 已观看 {int(time.time() - start_time)} 秒")

except Exception as e:
    print(f"❌ 发生错误: {e}")
    # 可选：截图保存错误现场
    driver.save_screenshot("error_login.png")

finally:
    driver.quit()
    print("👋 浏览器已关闭")
