import os.path
import json
from base_page import BasePage


class AdminPage(BasePage):

    def __init__(self):
        super(AdminPage, self).__init__()
        config_file = open(os.path.dirname(__file__) +
                           '/../config/admin_fields.json', 'r').read()
        self.config = json.loads(config_file)

    def fill_public_key(self, pk):
        I = self
        I.fill_field(self.config['custom']['public_key']).with_value(pk)
        # self._browser.fill(self.config['admin']['public_key'], pk)
        return self

    def fill_access_token(self, access_token):
        I = self
        I.fill_field(self.config['custom'][
                     'access_token']).with_value(access_token)
        self._browser.fill(self.config['custom']['access_token'], access_token)
        return self

    def select_debug_mode(self, debug_mode):
        I = self
        I.click_on_list(self.config['custom'][
                        'debug_mode']).then().select_element(debug_mode)
        # self._browser.select(self.config['admin']['debug_mode'], debug_mode)
        return self

    def select_status(self, status):
        I = self
        I.click_on_list(self.config['custom']['status']
                        ).then().select_element(status)
        # self._browser.select(self.config['admin']['status'], status)
        return self

    def select_maximum_installments(self, max_installments):
        I = self
        I.click_on_list(self.config['custom']['installments']).then(
        ).select_element(max_installments)
       # self._browser.select(self.config['admin']['installments'], max_installments)
        return self

    def select_category(self, store_category):
        I = self
        I.click_on_list(self.config['custom']['category']).then(
        ).select_element(store_category)
        # self._browser.select(self.config['admin']['category'], store_category)
        return self

    def select_country(self, country):
        I = self
        I.click_on_list(self.config['custom'][
                        'country']).then().select_element(country)
        # self._browser.select(self.config['admin']['country'], country)
        return self

    def check_payment_methods(self, payment_methods=[]):
        I = self
        pm_elem = self._browser.find_by_name(
            self.config['custom']['accepted_payment_methods'])
        for pm in pm_elem:
            if pm.value in payment_methods:
                pm.check()
        return self

    def select_order_status(self, order_status, value):
        I, desired_status = self, '%s_order_status' % order_status
        I.click_on_list(self.config['custom'][desired_status]).then().select_element(value)
        # self._browser.select(self.config['admin'][desired_status], value)
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
