# coding: utf-8
import unittest
import os.path
import json
from datetime import datetime
from page_objects.admin_page import AdminPage


class AdminTicketTest(unittest.TestCase):

    def setUp(self):
        print("\nstarting at: %s " % datetime.now().strftime("%x %X"))
        json_file = open(os.path.dirname(__file__) +
                         '/../../config/admin_data.json', 'r')
        fields_file = open(os.path.dirname(__file__) +
                           '/../../config/admin_fields.json', 'r')
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
        country = self.config["common_fields"]["sales_country"]
        new_country = "MLA"
        module_url = self.fields['urls']['admin']
        url = "%s%s%s" % (self.base_url, module_url, self.token)

        self.assertNotEqual(self.config["sellers"][new_country][0]["access_token"],
                            self.config["sellers"][country][0]["access_token"])
        I.visit_url(url)\
            .then()\
            .fill_access_token(self.config["sellers"][country][0]["access_token"])\
            .then()\
            .click_on_list(self.fields["ticket"]["status"])\
            .then()\
            .wait(5)\
            

        initial_list = I.get_list_of_elements_in_page(self.fields["ticket"]["accepted_payment_methods"])

        initial_length = len(initial_list)
        I.visit_url(url)\
            .then()\
            .fill_access_token(self.config["sellers"][new_country][0]["access_token"])\
            .click_on_list(self.fields["ticket"]["status"])\
            .then()\
            .wait(5)\
        
        final_list = I.get_list_of_elements_in_page(self.fields["ticket"]["accepted_payment_methods"])
        final_length = len(final_list)

        self.assertGreater(initial_length, 0)
        self.assertGreater(final_length, 0)
        self.assertNotEqual(initial_length,
                            final_length)

    def test_must_save_admin_data(self):
        I = self.admin_page
        country = self.config["common_fields"]["sales_country"]
        module_url = self.fields['urls']['admin']
        url = "%s%s%s" % (self.base_url, module_url, self.token)
        I.visit_url(url)\
            .then()\
            .select_status(self.config["common_fields"]["status"])\
            .then()\
            .fill_access_token(self.config["sellers"][country][0]["access_token"])\
            .then()\
            .select_category(self.config["common_fields"]["category"])\
            .then()\
            .check_payment_methods(self.config["common_fields"]["payment_methods"])

        for k, v in self.config["common_fields"]["default_statuses"].items():
            I.select_order_status(k, v)

        I.click_on_button("btn_save").then().visit_url(url)

        status_value = I.get_element_in_page(
            self.fields['ticket']["status"]).value
        self.assertEqual(status_value, self.config["common_fields"]["status"])

        access_token_value = I.get_element_in_page(
            self.fields['ticket']["access_token"]).value
        self.assertEqual(access_token_value, self.config[
                         "sellers"][country][0]["access_token"])
        category_value = I.get_element_in_page(
            self.fields['ticket']["category"]).value
        self.assertEqual(category_value, self.config[
                         "common_fields"]["category"])

        for k, v in self.config["common_fields"]["default_statuses"].items():
            elem_value = I.get_element_in_page(
                self.fields['ticket']['%s_order_status' % k]).value
            self.assertEqual(elem_value, v)

if __name__ == '__main__':
    unittest.main()
