# coding: utf-8

import time

try:
    from splinter import Browser
except Exception, e:
    install_command = 'sudo pip install -r requirements.txt'
    print("Error on import - %s" % e)
    print('Tip: You probably forgot to run "%s".' % install_command)
    exit()


class BasePage(object):

    """Page Object class to implement navigation. 
        All methods return "self", except if specified.
    """

    def __init__(self):
        """
        Start the browser object and load currencies and countries
        """
        self._browser = Browser("chrome")
        self.__element = None
        self.countries = ("MLA", "MLB", "MLC", "MCO", "MLM", "MLV", "MPE")
        self.currencies = ('ARS', 'BRL', 'MEX', 'CHI', 'PEN', 'VEF', 'COP')

    def visit_url(self, url_to_visit):
        """
        Visit specific url
        """
        self._browser.visit(url_to_visit)
        return self

    def get_element_in_page(self, element_name):
        """
        Get an specific element in the page with the specified name. 
        Returns the specific element.
        """
        elems = self._browser.find_by_id(element_name)
        elem = elems.first if elems else self._browser.find_by_name(
            element_name).first
        return elem

    def get_list_of_elements_in_page(self, elements_name):
        """
        Get an specific element in the page with the specified name. 
        Returns the specific element.
        """
        elems = self._browser.find_by_name(elements_name)
        return elems if elems else self._browser.find_by_id(elements_name)

    def click_on_button(self, button_name):
        """
        Click on a button in the page with the specified name
        """
        self.get_element_in_page(button_name).click()
        return self

    def fill_field(self, field_name):
        """
        Select a specific field on page and assign it to an internal private value
        """
        self.__set_element(field_name)
        return self

    def with_value(self, input_value):
        """
        Set the value to the previous element selected on fill_field method
        """
        self.__element.value = input_value
        self.__empty_element()
        return self

    def click_on_list(self, element_name):
        """
        Semantic method to select an element inside a DropDown List
        """
        self.__set_element(element_name)
        self.get_element_in_page(element_name).click()
        return self

    def select_element(self, list_name):
        """
        Select the value on the previous DropDownList selected on click_on_list method
        """
        self.__element.select(list_name)
        self.__empty_element()
        return self

    def click_on_checkbox(self, checkbox_name):
        """
        Check or uncheck the specified element
        """
        elem = self.get_element_in_page(checkbox_name)
        if elem.checked:
            elem.uncheck()
        else:
            elem.check()
        return self

    def then(self):
        """
        Semantic Method - returns self
        """
        return self

    def wait(self, seconds):
        """
        Wait for N seconds before continue
        """
        time.sleep(seconds)
        return self

    def login(self, login_url, username, password):
        """
        Platfom-specific login. Must be implemented to test your platform
        """
        raise NotImplementedError

    def url(self):
        """
        Returns actual url
        """
        return self._browser.url

    def exit(self):
        """
        Close the browser and finish the tests
        """
        self._browser.quit()

    def __set_element(self, element_name):
        """
        Set the internal element
        """
        self.__element = self.get_element_in_page(element_name)
        return self

    def __empty_element(self):
        """
        Empty the internal element
        """
        self.__element = None
        return self

if __name__ == '__main__':
    try:
        url = "http://www.mercadopago.com.br"
        x = BaseConfig()
        x.visit_url(url).then()\
            .get_element_in_page("common-register") \
            .click()
        x.get_element_in_page("signupFirstName").value = "Henrique"
        x.get_element_in_page("signupLastName").value = u'Juguetón'

    except Exception, e:
        print("Error - %s" % e)
