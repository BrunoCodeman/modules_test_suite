# coding: utf-8

import json
from base_config import BaseConfig


class AdminData(BaseConfig):

    """docstring for ClassName"""

    def __init__(self):
        super(AdminData, self).__init__()
        config_file = open('admin_fields.json', 'r').read()
        self.config = json.loads(config_file)

    def fill_public_key(self, pk):
        self._browser.fill(self.config['admin']['public_key'], pk)
        return self

    def fill_access_token(self, access_token):
        self._browser.fill(self.config['admin']['access_token'], access_token)
        return self

    def select_debug_mode(self, debug_mode):
        self._browser.select(self.config['admin']['debug_mode'], debug_mode)
        return self

    def select_status(self, status):
        self._browser.select(self.config['admin']['status'], status)
        return self

    def select_maximum_installments(self, max_installments):
        self._browser.select(self.config['admin'][
                             'installments'], max_installments)
        return self

    def select_category(self, store_category):
        self._browser.select(self.config['admin']['category'], store_category)
        return self

    def select_country(self, country):
        self._browser.select(self.config['admin']['country'], country)
        return self

    def check_payment_methods(self, payment_methods=[]):
        pm_elem = self._browser.find_by_name(
            self.config['admin']['accepted_payment_methods'])
        for pm in pm_elem:
            if pm.value in payment_methods:
                pm.check()
        # for pm in payment_methods:
        #    self._browser.check(
        #        self.config['admin']['accepted_payment_methods'][pm], pm)
        return self

    def select_order_status(self, order_status, value):
        desired_status = '%s_order_status' % order_status
        self._browser.select(
            self.config['admin'][desired_status], value)
        return self
