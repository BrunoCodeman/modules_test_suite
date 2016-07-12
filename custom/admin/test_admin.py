# coding: utf-8

import unittest
import os.path
import json
from datetime import datetime
from admin_data import AdminData


class AdminTest(unittest.TestCase):

    def setUp(self):
        print("starting at: %s " % datetime.now().strftime("%x %X"))
        self.base_url = 'http://172.17.0.3/oc22/'
        json_file = open(
            os.path.dirname(__file__) + '/../../admin_data.json', 'r').read()
        fields_file = open(
            os.path.dirname(__file__) + '/../../admin_fields.json', 'r').read()
        self.config = json.loads(json_file)
        self.fields = json.loads(fields_file)
        self.admin_data = AdminData()
        self.login("admin/",
                   self.config["common_fields"]['login']['username'],
                   self.config["common_fields"]['login']['password'])

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
        print("finished at: %s " % datetime.now().strftime("%x %X"))
        self.admin_data.exit()

    def test_must_load_payment_methods(self):
        I = self.admin_data
        module_url = "admin/index.php?route=payment/mp_transparente"
        url = "%s%s%s" % (self.base_url, module_url, self.token)
        I.visit_url(url)
        initial_payment_methods_length = I._browser.find_by_name(
            "mp_transparente_methods[]")

        I.select_country("MLB").then().wait(5)

        final_payment_methods_length = I._browser.find_by_name(
            "mp_transparente_methods[]")
        self.assertNotEqual(final_payment_methods_length,
                            initial_payment_methods_length)

    def test_must_save_admin_data(self):
        I = self.admin_data
        country = self.config["common_fields"]["sales_country"]
        module_url = "admin/index.php?route=payment/mp_transparente"
        url = "%s%s%s" % (self.base_url, module_url, self.token)
        I.visit_url(url).then()\
            .select_status(self.config["common_fields"]["status"])\
            .then()\
            .select_country(self.config["common_fields"]["sales_country"])\
            .then()\
            .fill_public_key(self.config["sellers"][country][0]["public_key"])\
            .then()\
            .fill_access_token(self.config["sellers"][country][0]["access_token"])\
            .then()\
            .select_category(self.config["common_fields"]["category"])\
            .then()\
            .select_maximum_installments(self.config["common_fields"]["installments"])\
            .then()\
            .check_payment_methods(self.config["common_fields"]["payment_methods"])

        for k, v in self.config["common_fields"]["default_statuses"].items():
            I.select_order_status(k, v)

        I.get_element_in_page("btn_save").click()  # and
        I.visit_url(url)
        status_value = I.get_element_in_page(
            self.fields['admin']["status"]).value
        self.assertEqual(status_value, self.config["common_fields"]["status"])
        country_value = I.get_element_in_page(
            self.fields['admin']["country"]).value
        self.assertEqual(country_value, self.config[
                         "common_fields"]["sales_country"])
        public_key_value = I.get_element_in_page(
            self.fields['admin']["public_key"]).value
        self.assertEqual(public_key_value, self.config[
                         "sellers"][country][0]["public_key"])
        access_token_value = I.get_element_in_page(
            self.fields['admin']["access_token"]).value
        self.assertEqual(access_token_value, self.config[
                         "sellers"][country][0]["access_token"])
        category_value = I.get_element_in_page(
            self.fields['admin']["category"]).value
        self.assertEqual(category_value, self.config[
                         "common_fields"]["category"])
        installments_value = I.get_element_in_page(
            self.fields['admin']["installments"]).value
        self.assertEqual(installments_value, self.config[
                         "common_fields"]["installments"])

        for k, v in self.config["common_fields"]["default_statuses"].items():
            elem_value = I.get_element_in_page(
                self.fields['admin']['%s_order_status' % k]).value
            self.assertEqual(elem_value, v)

    def test_must_reload_payment_methods_according_to_country(self):
        I = self.admin_data
        are_different = False
        module_url = "admin/index.php?route=payment/mp_transparente"
        url = "%s%s%s" % (self.base_url, module_url, self.token)
        I.visit_url(url)
        payment_methods = I._browser.find_by_name(self.fields["admin"]["accepted_payment_methods"])
        selected_before = filter(lambda x: x.value, payment_methods)
        I.get_element_in_page(self.fields["admin"]["country"]).select("MLA")
        I.wait(3)

        new_payment_methods = I._browser.find_by_name(self.fields["admin"]["accepted_payment_methods"])
        selected_now = filter(lambda x: x.value, new_payment_methods)
        
        for val in selected_before:
            if val not in selected_now:
                are_different = True
                break

        self.assertTrue(are_different)
        self.assertNotEqual(len(selected_before), len(selected_now))


if __name__ == '__main__':
    unittest.main()
