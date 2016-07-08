# coding: utf-8

import unittest
import os.path
import json
from admin_data import AdminData


class AdminTest(unittest.TestCase):

    def setUp(self):
        self.base_url = ""
        json_file = open(
            os.path.dirname(__file__) + '/../../admin_data.json', 'r').read()
        fields_file = open(
            os.path.dirname(__file__) + '/../../admin_fields.json', 'r').read()
        self.config = json.loads(json_file)
        self.fields = json.loads(fields_file)
        self.admin_data = AdminData()
        self.login("",
                   self.config['login']['username'],
                   self.config['login']['password'])

    def login(self, login_url, username, password):
        I = self.admin_data
        url_to_visit = self.base_url + login_url
        I.visit_url(url_to_visit).then().get_element_in_page(
            self.fields['login']['username']).value = username
        I.get_element_in_page(
            self.fields['login']['password']).value = username
        I._browser.find_by_css(".btn-primary").first.click()
        I.wait(3)
        self.assertNotEqual(url_to_visit, I.url())

    def tearDown(self):
        self.admin_data.exit()

    def test_must_load_payment_methods(self):
        pass

    def test_must_save_admin_data(self):
        pass

    def test_must_reload_payment_methods_according_to_country(self):
        pass

if __name__ == '__main__':
    unittest.main()
