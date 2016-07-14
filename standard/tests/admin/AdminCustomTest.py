# coding: utf-8
import unittest
import os.path
import json
from datetime import datetime
from page_objects.admin_page import AdminPage


class AdminCustomTest(unittest.TestCase):

    def setUp(self):
        print("\nstarting at: %s " % datetime.now().strftime("%x %X"))
        json_file = open(os.path.dirname(__file__) + '/../../config/admin_data.json', 'r')
        fields_file = open(os.path.dirname(__file__) + '/../../config/admin_fields.json', 'r')
        self.config = json.loads(json_file.read())
        self.fields = json.loads(fields_file.read())
        self.base_url = self.fields['urls']['base']
        self.admin_page = AdminPage()
        self.token = self.admin_page.login(self.config["common_fields"]['login'][
                              'username'], self.config["common_fields"]['login']['password'])
    def tearDown(self):
        print("\nfinished at: %s " % datetime.now().strftime("%x %X"))
        self.admin_page.exit()

    def test_must_load_payment_methods(self):
        I = self.admin_page
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
        I = self.admin_page
        country = self.config["common_fields"]["sales_country"]
        module_url = self.fields["urls"]["admin"] #"admin/index.php?route=payment/mp_transparente"
        url = "%s%s%s" % (self.base_url, module_url, self.token)
        I.visit_url(url)\
            .then()\
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

        I.click_on_button("btn_save").then().visit_url(url)
        
        status_value = I.get_element_in_page(
            self.fields['custom']["status"]).value
        self.assertEqual(status_value, self.config["common_fields"]["status"])
        country_value = I.get_element_in_page(
            self.fields['custom']["country"]).value
        self.assertEqual(country_value, self.config[
                         "common_fields"]["sales_country"])
        public_key_value = I.get_element_in_page(
            self.fields['custom']["public_key"]).value
        self.assertEqual(public_key_value, self.config[
                         "sellers"][country][0]["public_key"])
        access_token_value = I.get_element_in_page(
            self.fields['custom']["access_token"]).value
        self.assertEqual(access_token_value, self.config[
                         "sellers"][country][0]["access_token"])
        category_value = I.get_element_in_page(
            self.fields['custom']["category"]).value
        self.assertEqual(category_value, self.config[
                         "common_fields"]["category"])
        installments_value = I.get_element_in_page(
            self.fields['custom']["installments"]).value
        self.assertEqual(installments_value, self.config[
                         "common_fields"]["installments"])

        for k, v in self.config["common_fields"]["default_statuses"].items():
            elem_value = I.get_element_in_page(
                self.fields['custom']['%s_order_status' % k]).value
            self.assertEqual(elem_value, v)

    def test_must_reload_payment_methods_according_to_country(self):
        I = self.admin_page
        are_different = False
        module_url = "admin/index.php?route=payment/mp_transparente"
        url = "%s%s%s" % (self.base_url, module_url, self.token)
        print("visiting %s" % url)
        I.visit_url(url)
        payment_methods = I._browser.find_by_name(
            self.fields["custom"]["accepted_payment_methods"])
        selected_before = filter(lambda x: x.value, payment_methods)
        I.get_element_in_page(self.fields["custom"]["country"]).select("MLA")
        I.wait(3)

        new_payment_methods = I._browser.find_by_name(
            self.fields["custom"]["accepted_payment_methods"])
        selected_now = filter(lambda x: x.value, new_payment_methods)

        for val in selected_before:
            if val not in selected_now:
                are_different = True
                break

        self.assertTrue(are_different)
        self.assertNotEqual(len(selected_before), len(selected_now))


if __name__ == '__main__':
    unittest.main()
