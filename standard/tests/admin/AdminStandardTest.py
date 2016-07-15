# coding: utf-8
import unittest
import os.path
import json
from datetime import datetime
from page_objects.admin_page import AdminPage


class AdminStandardTest(unittest.TestCase):

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
        module_url = "admin/index.php?route=payment/mp_standard"
        url = "%s%s%s" % (self.base_url, module_url, self.token)
        I.visit_url(url)
        initial_payment_methods_length = I._browser.find_by_name(
            "mp_standard_methods[]")

        I.select_country("MLB").then().wait(5)

        final_payment_methods_length = I._browser.find_by_name(
            "mp_standard_methods[]")
        self.assertNotEqual(final_payment_methods_length,
                            initial_payment_methods_length)

    def test_must_save_admin_data(self):
        I = self.admin_page
        country = self.config["common_fields"]["sales_country"]
        module_url = self.fields["urls"]["admin"] #"admin/index.php?route=payment/mp_standard"
        url = "%s%s%s" % (self.base_url, module_url, self.token)
        I.visit_url(url)\
            .then()\
            .select_status(self.config["common_fields"]["status"])\
            .then()\
            .select_country(self.config["common_fields"]["sales_country"])\
            .then()\
            .fill_client_id(self.config["sellers"][country][0]["client_id"])\
            .then()\
            .fill_client_secret(self.config["sellers"][country][0]["client_secret"])\
            .then()\
            .select_category(self.config["common_fields"]["category"])\
            .then()\
            .select_autoreturn(self.config["common_fields"]["autoreturn"])\
            .then()\
            .select_debug_mode(self.config["common_fields"]["debug_mode"])\
            .then()\
            .select_checkout_type(self.config["common_fields"]["checkout_type"])\
            .then()\
            .select_maximum_installments(self.config["common_fields"]["installments"])\
            .then()\
            .check_payment_methods(self.config["common_fields"]["payment_methods"])
            
        for k, v in self.config["common_fields"]["default_statuses"].items():
            I.select_order_status(k, v)

        I.click_on_button("btn_save").then().visit_url(url)
        
        status_value = I.get_element_in_page(
            self.fields['standard']["status"]).value
        self.assertEqual(status_value, self.config["common_fields"]["status"])
        
        country_value = I.get_element_in_page(
            self.fields['standard']["country"]).value
        self.assertEqual(country_value, country)
        
        client_id_value = I.get_element_in_page(
            self.fields['standard']["client_id"]).value
        self.assertEqual(str(client_id_value), str(self.config[
                         "sellers"][country][0]["client_id"]))
        
        client_secret_value = I.get_element_in_page(
            self.fields['standard']["client_secret"]).value
        self.assertEqual(str(client_secret_value), str(self.config[
                         "sellers"][country][0]["client_secret"]))
        
        category_value = I.get_element_in_page(
            self.fields['standard']["category"]).value
        self.assertEqual(category_value, self.config[
                         "common_fields"]["category"])
        
        installments_value = I.get_element_in_page(
            self.fields['standard']["installments"]).value
        self.assertEqual(installments_value, self.config[
                         "common_fields"]["installments"])

        for k, v in self.config["common_fields"]["default_statuses"].items():
            elem_value = I.get_element_in_page(
                self.fields['standard']['%s_order_status' % k]).value
            self.assertEqual(elem_value, v)

    def test_must_reload_payment_methods_according_to_country(self):
        I = self.admin_page
        are_different = False
        module_url = self.fields["urls"]["admin"]
        url = "%s%s%s" % (self.base_url, module_url, self.token)
        I.visit_url(url)
        payment_methods = I._browser.find_by_name(
            self.fields["standard"]["accepted_payment_methods"])
        selected_before = filter(lambda x: x.value, payment_methods)
        I.get_element_in_page(self.fields["standard"]["country"]).select("MLA")
        I.wait(3)

        new_payment_methods = I._browser.find_by_name(
            self.fields["standard"]["accepted_payment_methods"])
        selected_now = filter(lambda x: x.value, new_payment_methods)

        for val in selected_before:
            if val not in selected_now:
                are_different = True
                break

        self.assertTrue(are_different)
        self.assertNotEqual(len(selected_before), len(selected_now))


if __name__ == '__main__':
    unittest.main()
