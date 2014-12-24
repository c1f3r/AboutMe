from functional_tests.base import FunctionalTest


class TestIndexPage(FunctionalTest):

    def test_can_get_to_other_pages(self):
        # User comes to main page and sees info about me
        self.browser.get(self.server_url)
        self.assertIn('About Me', self.browser.title)
        # Then he clicks on login link and gets to login page
        login_link = self.browser.find_element_by_id("login_link")
        login_link.click()
        self.assertIn("Login page", self.browser.title)
        # On login page he sees input fields and submit button
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')
        LOGIN_BUTTON_XPATH = '//input[@type="submit"]'
        submit_btn = self.browser.find_element_by_xpath(LOGIN_BUTTON_XPATH)
        # He inputs login/pass and gets back to index page
        username_input.send_keys(u'admin')
        password_input.send_keys(u'admin')
        submit_btn.click()
        self.assertIn('About Me', self.browser.title)
