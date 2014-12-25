from selenium.common.exceptions import NoSuchElementException
from functional_tests.base import FunctionalTest


class TestIndexPage(FunctionalTest):

    fixtures = ['initial_data.json']

    def is_id_present(self, element_id):
        try:
            self.browser.find_element_by_id(element_id)
            return True
        except NoSuchElementException:
            return False

    def test_user_can_get_to_other_pages_login_an_logout(self):
        # User comes to main page and sees info about me
        self.browser.get(self.server_url)
        # Gets to english version of site
        en_option_xpath = "//select[@name='language']/option[@value='en']"
        self.browser.find_element_by_xpath(en_option_xpath).click()
        self.assertIn('About Me', self.browser.title)
        # Even if not logged in user can go to 10 first requests page
        self.browser.find_element_by_id('requests_link').click()
        self.assertIn("First 10 HttpRequests", self.browser.title)
        # He sees first 10 requests and gets back to index page
        self.browser.get(self.server_url)
        # Then he clicks on login link and gets to login page
        self.browser.find_element_by_id("login_link").click()
        self.assertIn("Login page", self.browser.title)
        # On login page he sees input fields and submit button
        # He inputs login/pass and is redirected to index page
        self.browser.find_element_by_id('id_username').send_keys(u'admin')
        self.browser.find_element_by_id('id_password').send_keys(u'admin')
        self.browser.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertIn('About Me', self.browser.title)
        # Should be sure there is no login link when already logged in
        self.assertFalse(self.is_id_present('login_link'))
        # User now wants to edit info about me in frontend
        # so he clicks on edit_info link
        self.browser.find_element_by_id('edit_info_link').click()
        self.assertIn('Edit info about me', self.browser.title)
        # Then user decides to go back to index page
        self.browser.find_element_by_id('index_link').click()
        self.assertIn('About Me', self.browser.title)
        # After that user decides to edit info about me through admin site
        self.browser.find_element_by_id('admin_edit_link').click()
        admin_url = self.browser.current_url
        self.assertRegexpMatches(admin_url, '/en/admin/hello/aboutuser/1/')
        # He decides to get back to index page and logout then
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('logout_link').click()
        # Now he is redirected to index page
        self.assertIn('About Me', self.browser.title)
        # And when user is logged out there are no edit and logout
        # links in navbar but only login link available
        self.assertTrue(self.is_id_present('login_link'))
        self.assertFalse(self.is_id_present('logout_link'))
        self.assertFalse(self.is_id_present('edit_info_link'))
        self.assertFalse(self.is_id_present('admin_edit_link'))
