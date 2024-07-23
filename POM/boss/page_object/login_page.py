from POM.boss.base_page.base_page import BossBasePage


class LoginPageBoss(BossBasePage):
    def __init__(self):
        super().__init__()

    def enter_account(self, username, password):
        self.get_url('login')
        login_url = self.boss_element['login']['url']

        self.element_locator_sendkeys(page_name='login',
                                      element_name='input_username',
                                      input_data=username)

        self.element_locator_sendkeys(page_name='login',
                                      element_name='input_password',
                                      input_data=password)

        self.element_locator(page_name='login', element_name='login_button').click()
        self.save_boss_cookies_to_json()

        current_url = self.driver.current_url

        return login_url, current_url

    def enter_account_error(self):
        self.get_url('login')
        login_url = self.boss_element['login']['url']

        self.element_locator_sendkeys(page_name='login',
                                      element_name='input_username',
                                      input_data="onelap")

        self.element_locator_sendkeys(page_name='login',
                                      element_name='input_password',
                                      input_data="123")

        self.element_locator(page_name='login', element_name='login_button').click()
        current_url = self.driver.current_url

        return login_url, current_url


if __name__ == '__main__':
    a = LoginPageBoss()
    a.enter_account("onelap", "onelap@123")
    a.driver.quit()
