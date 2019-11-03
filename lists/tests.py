from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

from superlists.features import feature_flags


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        content = response.content.decode()
        self.assertIn('itemey 1', content)
        self.assertIn('itemey 2', content)


class MultiUser_HomePageTest(TestCase):
    def setUp(self):
        self.multiple_lists_flag = feature_flags.multiple_lists
        feature_flags.multiple_lists = True

    def tearDown(self):
        feature_flags.multiple_lists = self.multiple_lists_flag

    def test_go_home_creates_new_list(self):
        self.assertEqual(List.objects.count(), 0)
        self.client.get('/')
        self.assertEqual(List.objects.count(), 1)

    def test_go_home_redirects_to_list_url(self):
        response = self.client.get('/')
        new_list_id = List.objects.first().id
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/lists/{new_list_id}')

class MultiUser_ListPageTest(TestCase):
    def setUp(self):
        self.list = List()
        self.list.save()

    def test_list_page_return_correct_template(self):
        response = self.client.get(f'/lists/{self.list.id}')
        self.assertTemplateUsed(response, 'list.html')



class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
