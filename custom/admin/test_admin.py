# coding: utf-8

import unittest
import os.path
import json
from admin_data import AdminData


class AdminTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://localhost:8888/oc21/'
        json_file = open(
            os.path.dirname(__file__) + '/../../admin_data.json', 'r').read()
        fields_file = open(
            os.path.dirname(__file__) + '/../../admin_fields.json', 'r').read()
        self.config = json.loads(json_file)
        self.fields = json.loads(fields_file)
        self.admin_data = AdminData()
        self.login("admin/",
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
        self.token = "&token=%s" % self.admin_data.url().split('token=')[-1]

    def tearDown(self):
        self.admin_data.exit()

    def test_must_load_payment_methods(self):
        I = self.admin_data
        module_url = "admin/index.php?route=payment/mp_transparente%s"
        url = "%s%s%s" % (self.base_url, module_url, self.token)
        I.visit_url(url)
        initial_payment_methods_length = I.get_element_in_page("mp_transparente_methods[]")
        I.select_country(self.config).then().wait(5)
        final_payment_methods_length = I.get_element_in_page("mp_transparente_methods[]")
        self.assertGreaterThan(final_payment_methods_length, initial_payment_methods_length)

   # def test_must_save_admin_data(self):
    #    pass

   # def test_must_reload_payment_methods_according_to_country(self):
   #     pass

if __name__ == '__main__':
    unittest.main()
