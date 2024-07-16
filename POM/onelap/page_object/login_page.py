from POM.onelap.base.base_page import OnelapBasePage


class OnelapLogin(OnelapBasePage):
    def __init__(self):
        super().__init__()
        self.driver = self.connect_device_first()

    def open_onelap_app(self, username, password):
        self.element_locator(self.driver, 'login', 'tv_agree_privacy_dialog').click()
        self.element_locator(self.driver, 'login', 'btn_login_index').click()
        self.element_locator(self.driver, 'login', 'et_username_login').send_keys(username)
        self.element_locator(self.driver, 'login', 'et_password_login').send_keys(password)
        self.element_locator(self.driver, 'login', 'btn_check_out_login').click()
        self.element_locator(self.driver, 'login', 'btn_login_login').click()

    def get_app_name(self):
        self.element_locator(self.driver, 'login', 'tv_agree_privacy_dialog').click()
        home_title = self.element_locator(self.driver, 'login',
                                          'com.onelap.bls.dear:id/tv_app_name_main_fragment').text
        return home_title


if __name__ == '__main__':
    OnelapLogin().open_onelap_app("13001723386", "zhang107.")
    OnelapLogin().get_app_name()
