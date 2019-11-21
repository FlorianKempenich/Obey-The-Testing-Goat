from django.test import TestCase
from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ItemForm, NewListFromItemForm
from lists.models import List, Item
import unittest
from unittest.mock import patch

# My understanding of forms so far
# --------------------------------
#
# Forms are wrapper around Models that:
# - Perform automatic validation before saving
#   - Based on the Model constraints
#   - As opposed to calling 'save()' on the model itself
#     (without calling 'full_clean()' before)
# - Generate HTML & error message
#


class ItemFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        item = Item(list=list_)
        form = ItemForm(instance=item, data={'text': ''})

        with self.assertRaises(ValueError):
            form.save()

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        item = Item(list=list_)
        form = ItemForm(instance=item, data={'text': 'hello'})

        new_item = form.save()
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'hello')
        self.assertEqual(new_item.list, list_)

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='duplicate')

        item = Item(list=list_)
        form = ItemForm(instance=item, data={'text': 'duplicate'})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])


class NewListFromItemFormTest(unittest.TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = NewListFromItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg', form.as_p())

    @patch('lists.forms.List')
    def test_saves_new_list_with_item(self, MockList):
        form = NewListFromItemForm(data={'text': 'New item text'})

        form.is_valid()  # Populate 'cleaned_data'
        saved_list = form.save()

        MockList.create_new.assert_called_once_with(
            first_item_text='New item text')
        self.assertEqual(saved_list, MockList.create_new.return_value)

    def test_valid_items_are_valid(self):
        form = NewListFromItemForm(data={'text': 'valid item'})
        self.assertTrue(form.is_valid())

    def test_blank_items_are_not_valid(self):
        form = NewListFromItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
