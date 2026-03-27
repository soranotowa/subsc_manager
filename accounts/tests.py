from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 以下は現在の書き方に修正(今はwebdriverの個別のダウンロードは不要)
        cls.selenium = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # ユーザ作成
        User = get_user_model()
        username = 'testuser'
        email = 'test@example.com'
        password = 'testpass123'

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ログインページを開く
        # self.selenium.get('http://localhost:8000' + str(reverse_lazy('account_login')))
        self.selenium.get(self.live_server_url + str(reverse_lazy('account_login')))

        # ログイン
        # 以下は現在の書き方に修正(find_element_by_nameは現在は廃止されている)
        username_input = self.selenium.find_element(By.NAME, "login")
        # username_input.send_keys('<ユーザ登録済みのメールアドレス>')
        username_input.send_keys(email)

        password_input = self.selenium.find_element(By.NAME, "password")
        # password_input.send_keys('<ログインパスワード>')
        password_input.send_keys(password)

        # self.selenium.find_element(By.CLASS_NAME, 'btn').click()
        self.selenium.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # ページタイトルの検証
        # self.assertEqual('日記一覧 | Private Diary', self.selenium.title)
        # 👇 修正後
        WebDriverWait(self.selenium, 10).until(
            EC.title_is('日記一覧 | Private Diary')
        )