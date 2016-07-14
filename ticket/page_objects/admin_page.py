import os.path
import json
import inspect
from base_page import BasePage


class AdminPage(BasePage):

    def __init__(self):

        super(AdminPage, self).__init__()
        config_file = open(os.path.dirname(__file__) +
                           '/../config/admin_fields.json', 'r').read()
        self.config = json.loads(config_file)
        my_name = inspect.currentframe()
        print("executing %s" % my_name)

    def fill_access_token(self, access_token):
        my_name = inspect.currentframe()
        print("executing %s" % my_name)
        I = self
        I.fill_field(self.config['ticket'][
                     'access_token']).with_value(access_token)
        self._browser.fill(self.config['ticket']['access_token'], access_token)
        return self

    def select_debug_mode(self, debug_mode):
        my_name = inspect.currentframe()
        print("executing %s" % my_name)
        I = self
        I.click_on_list(self.config['ticket'][
                        'debug_mode']).then().select_element(debug_mode)
        # self._browser.select(self.config['admin']['debug_mode'], debug_mode)
        return self

    def select_status(self, status):
        I = self
        I.click_on_list(self.config['ticket']['status']
                        ).then().select_element(status)
        # self._browser.select(self.config['admin']['status'], status)
        return self

    def select_category(self, store_category):
        I = self
        I.click_on_list(self.config['ticket']['category']).then(
        ).select_element(store_category)
        # self._browser.select(self.config['admin']['category'], store_category)
        return self

    def check_payment_methods(self, payment_methods=[]):
        I = self
        pm_elem = self._browser.find_by_name(
            self.config['ticket']['accepted_payment_methods'])
        for pm in pm_elem:
            if pm.value in payment_methods:
                pm.check()
        return self

    def select_order_status(self, order_status, value):
        I, desired_status = self, '%s_order_status' % order_status
        I.click_on_list(self.config['ticket'][desired_status]).then().select_element(value)
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
