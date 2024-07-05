from POM.boss.base.base_page import BossBasePage
from common.logger import log_decorator


class ReportResult(BossBasePage):
    def __init__(self):
        super().__init__()
        self.b = 5

    @log_decorator
    def create_record_forbid_speak(self):
        a = self.b + 5
        self.driver.quit()
        return a


if __name__ == '__main__':
    x = ReportResult()
