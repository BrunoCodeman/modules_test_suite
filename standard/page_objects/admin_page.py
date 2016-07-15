import os.path
import json
from base_page import BasePage


class AdminPage(BasePage):

    def __init__(self):
        super(AdminPage, self).__init__()
        config_file = open(os.path.dirname(__file__) +
                           '/../config/admin_fields.json', 'r').read()
        self.config = json.loads(config_file)

    def fill_client_id(self, client_id):
        I = self
        I.fill_field(self.config['standard']['client_id']).with_value(client_id)
        return self

    def fill_client_secret(self, client_secret):
        I = self
        I.fill_field(self.config['standard'][
                     'client_secret']).with_value(client_secret)
        self._browser.fill(self.config['standard']['client_secret'], client_secret)
        return self

    def select_debug_mode(self, debug_mode):
        I = self
        I.click_on_list(self.config['standard'][
                        'debug_mode']).then().select_element(debug_mode)
        return self


    def select_autoreturn(self, autoreturn):
        I = self
        I.click_on_list(self.config['standard'][
                        'autoreturn']).then().select_element(autoreturn)
        return self

    def select_checkout_type(self, checkout_type):
        I = self
        I.click_on_list(self.config['standard'][
                        'checkout_type']).then().select_element(checkout_type)
        return self

    def select_sandbox(self, sandbox):
        I = self
        I.click_on_list(self.config['standard'][
                        'sandbox']).then().select_element(sandbox)
        return self

    def select_status(self, status):
        I = self
        I.click_on_list(self.config['standard']['status']
                        ).then().select_element(status)
        return self

    def select_maximum_installments(self, max_installments):
        I = self
        I.click_on_list(self.config['standard']['installments']).then(
        ).select_element(max_installments)
        return self

    def select_category(self, store_category):
        I = self
        I.click_on_list(self.config['standard']['category']).then(
        ).select_element(store_category)
        return self

    def select_country(self, country):
        I = self
        I.click_on_list(self.config['standard'][
                        'country']).then().select_element(country)
        return self

    def check_payment_methods(self, payment_methods=[]):
        I = self
        pm_elem = self._browser.find_by_name(
            self.config['standard']['accepted_payment_methods'])
        for pm in pm_elem:
            if pm.value in payment_methods:
                pm.check()
        return self

    def select_order_status(self, order_status, value):
        I, desired_status = self, '%s_order_status' % order_status
        I.click_on_list(self.config['standard'][desired_status]).then().select_element(value)
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
