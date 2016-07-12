class AdminTest():

    def setUp(self):
        self.base_url = "http://localhost:8888/oc22/"
        json_file = open(
            os.path.dirname(__file__) + '/../../buyer_data.json', 'r').read()
        fields_file = open(
            os.path.dirname(__file__) + '/../../buyer_fields.json', 'r').read()
        self.config = json.loads(json_file)
        self.fields = json.loads(fields_file)
        self.browser = BuyerData()

  #  def tearDown(self):
   #     pass

    #def test_must_pay_product_with_credit_card(self):
    #    pass

    #def test_must_redirect_if_payment_is_concluded(self):
    #    pass

    #def test_must_load_card_data_when_credit_card_change(self):
    #    pass

   # def test_must_load_installments_when_credit_card_change(self):
   #     pass


if __name__ == '__main__':
    unittest.main()
