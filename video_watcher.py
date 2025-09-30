from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# --- 配置部分 ---
LOGIN_URL = "https://kunpeng.askpcb.com/login.html"  # 替换为你的实际登录页URL
VIDEO_URL = "https://kunpeng.askpcb.com/kng/#/course/play?kngId=0040e5d6-5f0e-405d-8fb3-d2233eceb3d0&projectId=&btid=&gwnlUrl=&locateshare=94d6a796-d46a-4c28-a12d-3287c5c2d283" # 替换为你想看的视频页面URL
CHROMEDRIVER_PATH = "E:\chromedriver-win64\chromedriver.exe" # 如果没加到PATH，需要指定驱动路径
WATCH_TIME_SECONDS = 300  # 计划观看时长（秒）
# ---------------

# ---------------
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

try:
    # 1️⃣ 打开登录页
    driver.get(LOGIN_URL)
    print("\n" + "="*50)
    print("   🛑 请在打开的浏览器中手动登录")
    print("   ⏳ 正在自动检测登录状态...")
    print("="*50 + "\n")

    # 自动检测登录状态，出现首页按钮即认为已登录
    login_success = False
    for i in range(60):  # 最多等待60秒
        try:
            # 检查页面是否出现“首页”按钮
            driver.find_element(By.XPATH, '//a[@href="/main/#/index" and contains(text(), "首页")]')
            login_success = True
            print("🚀 检测到首页按钮，已登录，脚本继续执行...")
            break
        except:
            time.sleep(1)
    if not login_success:
        print("❌ 未检测到登录成功（未找到首页按钮），请检查账号或网络！")
        driver.quit()
        exit(1)

    # 2️⃣ 登录成功后，跳转到视频页面
    driver.get(VIDEO_URL)
    print("🎬 视频页面已加载")
    time.sleep(5)

    # 3️⃣ 尝试播放视频（原有逻辑）
    # ✅ 确保视频在播放
    try:
            # 方法1：通过内部 span 文字定位
            try:
                play_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="开始学习"]]'))
                )
                play_button.click()
                print("▶️ 已点击‘开始学习’按钮")
            except:
                # 如果找不到"开始学习"按钮，尝试找"继续学习"按钮
                continue_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="继续学习"]]'))
                )
                continue_button.click()
                print("▶️ 已点击‘继续学习’按钮")
    except Exception as e:
            print(f"⚠️ 未找到或无法点击播放按钮: {e}")

        # 4️⃣ 保持观看...（无限时长，持续保持页面活动）
    print("⏳ 已进入视频页面，自动保持活动，无时间限制。按 Ctrl+C 退出。")
    while True:
        driver.execute_script("window.scrollBy(0, 1);")
        time.sleep(random.randint(10, 30))

except Exception as e:
        print(f"❌ 发生错误: {e}")

finally:
        driver.quit()
        print("👋 浏览器已关闭")

    # # ⚠️ 备选方案：直接点击隐藏的 checkbox input（不推荐，可能被遮挡）
    # try:
    #     agree_element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//label[@class="yxt-checkbox core-custom-checkbox"]//span[contains(text(), "已阅读并同意")]'))
    #     )
    #     # 使用 JavaScript 点击（绕过 Selenium 原生点击限制）
    #     driver.execute_script("arguments[0].click();", agree_element)
    #     print("✅ 已通过 JS 点击同意隐私政策")
    # except Exception as e:
    #     print(f"⚠️ JS点击同意条款失败: {e}")
    #     driver.save_screenshot("js_click_error.png")  # 截图留证

    # # 2️⃣ 定位用户名输入框 —— 使用 placeholder 或 class 定位（因为 name="username" 有歧义）
    # username_field = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//input[@placeholder="请输入员工邮箱/账号"]'))
    # )
    # username_field.clear()
    # username_field.send_keys(USERNAME)
    # print("✅ 已输入用户名")

    # # 3️⃣ 定位密码输入框 —— 使用 type="password" + class 定位
    # password_field = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//input[@type="password" and @class="yxtf-input__inner yxtf-input__inner--border"]'))
    # )
    # password_field.clear()
    # password_field.send_keys(PASSWORD)
    # print("✅ 已输入密码")
    
    # # ✅ 终极方案：手动派发 mousedown -> mouseup -> click 事件
    # try:
    #     login_button = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//button[span/span[text()="登 录"]]'))
    #     )

    #     # 滚动到按钮
    #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_button)
    #     time.sleep(1)

    #     # 手动派发三个事件（模拟真实点击）
    #     driver.execute_script("""
    #         var btn = arguments[0];
    #         // 模拟鼠标按下的事件
    #         var evt1 = new MouseEvent('mousedown', {
    #             bubbles: true,
    #             cancelable: true,
    #             view: window,
    #             clientX: btn.getBoundingClientRect().left + btn.offsetWidth / 2,
    #             clientY: btn.getBoundingClientRect().top + btn.offsetHeight / 2
    #         });
    #         btn.dispatchEvent(evt1);

    #         // 模拟鼠标抬起的事件
    #         var evt2 = new MouseEvent('mouseup', {
    #             bubbles: true,
    #             cancelable: true,
    #             view: window,
    #             clientX: btn.getBoundingClientRect().left + btn.offsetWidth / 2,
    #             clientY: btn.getBoundingClientRect().top + btn.offsetHeight / 2
    #         });
    #         btn.dispatchEvent(evt2);

    #         // 模拟点击事件（通常由 mousedown+mouseup 触发）
    #         var evt3 = new MouseEvent('click', {
    #             bubbles: true,
    #             cancelable: true,
    #             view: window,
    #             clientX: btn.getBoundingClientRect().left + btn.offsetWidth / 2,
    #             clientY: btn.getBoundingClientRect().top + btn.offsetHeight / 2
    #         });
    #         btn.dispatchEvent(evt3);
    #     """, login_button)

    #     print("✅ 已模拟完整鼠标事件点击登录按钮")
    # except Exception as e:
    #     print(f"❌ 模拟鼠标事件失败: {e}")
    #     driver.save_screenshot("mouse_events_fail.png")
    #     raise

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
