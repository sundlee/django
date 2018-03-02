from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
import re

class HomePageTest(TestCase):

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertTrue(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        self.assertIn('신규 작업 아이템', response.content.decode())
        expected_html1 = render_to_string(
            'home.html',
            {'new_item_text': '신규 작업 아이템'},
        )
        expected_html2 = response.content.decode()
        # print("response.content.decode(): 1111111111111111")
        # print(expected_html2)
        # print("render_to_string: 2222222222222222")
        # print(self.remove_csrf(expected_html1))


        self.assertEqual(self.remove_csrf(expected_html2), self.remove_csrf(expected_html1))
