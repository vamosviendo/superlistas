class PagMisListas:

    def __init__(self, test):
        self.test = test

    def ir_a_pag_mis_listas(self):
        self.test.browser.get(self.test.live_server_url)
        self.test.browser.find_element_by_link_text('Mis listas').click()
        self.test.esperar_a(
            lambda: self.test.assertEqual(
                self.test.browser.find_element_by_tag_name('h1').text,
                'Mis listas'
            )
        )
        return self
