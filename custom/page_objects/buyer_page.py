import os.path
import json
from base_page import BasePage


class BuyerPage(BasePage):

    def __init__(self):
        super(BuyerPage, self).__init__()
        config_file = open(os.path.dirname(__file__) +
                           '/../config/admin_fields.json', 'r').read()
        self.config = json.loads(config_file)

    def fill_credit_card_number(self, cc_num):
        I = self
        I.fill_field(self.config['custom']['credit_card']).with_value(cc_num)
        return self

    def fill_expiration_month(self, expiration_month):
        I = self
        I.fill_field(self.config['custom'][
                     'expiration_month']).with_value(expiration_month)
        self._browser.fill(self.config['custom'][
                           'expiration_month'], expiration_month)
        return self

    def fill_expiration_year(self, expiration_year):
        I = self
        I.fill_field(self.config['custom'][
                     'expiration_year']).with_value(expiration_year)
        self._browser.fill(self.config['custom'][
                           'expiration_year'], expiration_year)
        return self

    def fill_card_owner_name(self, card_owner_name):
        I = self
        I.fill_field(self.config['custom'][
                     'card_owner_name']).with_value(card_owner_name)
        self._browser.fill(self.config['custom'][
                           'card_owner_name'], card_owner_name)
        return self

    def fill_security_code(self, security_code):
        I = self
        I.fill_field(self.config['custom'][
                     'security_code']).with_value(security_code)
        self._browser.fill(self.config['custom'][
                           'security_code'], security_code)
        return self

    def select_installments(self, installments):
        I = self
        I.click_on_list(self.config['custom'][
                        'installments']).then().select_element(installments)
        return self

    def login(self, username, password):
        """
        Log in to the platform.
        """
        first_url = self.url()
        I = self
        url_to_visit = "%s%s" % (
            self.config['urls']['base'], self.config['urls']['login'])
        I.visit_url(url_to_visit)\
            .then()\
            .fill_field(self.config['login']['username'])\
            .with_value(username)\
            .then()\
            .fill_field(self.config['login']['password'])\
            .with_value(password)\
            .then()\
            ._browser.find_by_css(self.config['login']['button']).click()
        I.wait(3)
        new_url = self.url()
        assert new_url != first_url
        token = "&token=%s" % self.url().split('token=')[-1]
        return token
