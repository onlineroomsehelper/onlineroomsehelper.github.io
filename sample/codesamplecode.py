from datetime import datetime, timezone, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 设置初始的 course sub id 值
course_id = 106261 # 这里更改成你想试的课号
sub_id = 27908413 # 随便设一个初始值
# 计算timestamp
# 获取当前系统时间并设置为UTC时区
current_time = datetime.now(timezone.utc)
target_time = datetime(2024, 4, 21, 0, 3, 30, tzinfo=timezone(timedelta(hours=8))).astimezone(timezone.utc)
# 计算时间差
time_diff = current_time - target_time
# 将时间差转换为秒数
t = 1713629012 + time_diff.total_seconds()


# 初始化 Chrome 浏览器
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 最大化窗口
driver = webdriver.Chrome()

# 待访问的初始 URL 注意！！！！！这里更换成你在教学网获取到的url！！！！！！！！！
base_url = "https://yjapise.pku.edu.cn/casapi/index.php?r=auth/login-with-sign&role_type=student&tenant_code=1&app_id=XXXXXXXXXXXXXXXXXXXXX&account=2X000XXXXX&sign=XXXXXXXXXXXXXXXXXXX&nonce=XXXXXXXXXXXXXXXXXXXXXXXXXX&forward=https://onlineroomse.pku.edu.cn/livingroom?course_id%3D"

# 循环访问
while True:
    # 构建完整的 URL
    url = base_url + str(course_id) + "%26sub_id%3D" + str(sub_id) + "&timestamp=" + str(t)

    # 访问 URL
    driver.get(url)

    # 等待元素加载
    try:
        tagoferror = 1
        alert_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.el-message.el-message--warning')))
    except:
        tagoferror = 0
    if(tagoferror):
        print(f"课程id或者 sub_id 被篡改，当前 URL: {url}")
        # 如果弹出元素，则 x 值加1，继续下一次循环
        sub_id += 1
        # 计算timestamp
        # 获取当前系统时间并设置为UTC时区
        current_time = datetime.now(timezone.utc)
        target_time = datetime(2024, 4, 21, 0, 3, 30, tzinfo=timezone(timedelta(hours=8))).astimezone(timezone.utc)
        # 计算时间差
        time_diff = current_time - target_time
        # 将时间差转换为秒数
        t = 1713629012 + time_diff.total_seconds()

        time.sleep(4)
        continue
    else:
        # 如果未弹出元素，则将 URL 写入到 txt 文件中，并结束循环
        # EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-v-2a2a4971][title]'))

        title = driver.find_element(By.CSS_SELECTOR, 'span[data-v-2a2a4971][title]').get_attribute("title")
        teacher_name = driver.find_element(By.CSS_SELECTOR, 'span.course-info__header-teachInfo ').text.split()[0]
        location = driver.find_element(By.CSS_SELECTOR, 'span.course-info__header-teachInfo ').text.split()[1]

        with open("output.txt", "a") as file:
            file.write(title + " " + teacher_name + " " + location + ":\n" + "course_id:"+str(course_id) + " " +"sub_id:" + str(sub_id)+"\n" + str(current_time) +"\n")
        print(f"试验成功，当前 URL 已写入 output.txt 文件: {url}")
        break


# 关闭浏览器
driver.quit()
