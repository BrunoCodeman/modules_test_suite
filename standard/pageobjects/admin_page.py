import os.path
from base_page import BasePage

class AdminPage(BasePage):
	  """docstring for ClassName"""

    def __init__(self):
        super(AdminPage, self).__init__()
        config_file = open('admin_fields.json', 'r').read()
        self.config = json.loads(config_file)

    def fill_public_key(self, pk):
    	I = self
    	I.fill_field(self.config['admin']['public_key']).with_value(pk)
        #self._browser.fill(self.config['admin']['public_key'], pk)
        return self

    def fill_access_token(self, access_token):
    	I.fill_field(self.config['admin']['access_token']).with_value(access_token)
        self._browser.fill(self.config['admin']['access_token'], access_token)
        return self

    def select_debug_mode(self, debug_mode):
        I = self
        I.click_on_list(self.config['admin']['debug_mode']).then().select_element(debug_mode)
        #self._browser.select(self.config['admin']['debug_mode'], debug_mode)
        return self

    def select_status(self, status):
        I = self
        I.click_on_list(self.config['admin']['status']).then().select_element(status)
        #self._browser.select(self.config['admin']['status'], status)
        return self

    def select_maximum_installments(self, max_installments):
        I = self
        I.click_on_list(self.config['admin']['installments']).then().select_element(max_installments)
       # self._browser.select(self.config['admin']['installments'], max_installments)
        return self

    def select_category(self, store_category):
        I = self
        I.click_on_list(self.config['admin']['category']).then().select_element(store_category)
        #self._browser.select(self.config['admin']['category'], store_category)
        return self

    def select_country(self, country):
        I = self
        I.click_on_list(self.config['admin']['country']).then().select_element(country)
        #self._browser.select(self.config['admin']['country'], country)
        return self

    def check_payment_methods(self, payment_methods=[]):
        I = self
        pm_elem = self._browser.find_by_name(
            self.config['admin']['accepted_payment_methods'])
        for pm in pm_elem:
            if pm.value in payment_methods:
                pm.check()
        return self

    def select_order_status(self, order_status, value):
        I, desired_status = self, '%s_order_status' % order_status
        I.click_on_list(self.config['admin']['desired_status']).then().select_element(value)
        #self._browser.select(self.config['admin'][desired_status], value)
        return self

    def login(self, username, password):
        {

        }

		