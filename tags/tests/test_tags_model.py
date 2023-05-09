from django.test import TestCase

from tags.models import Tag


class TestTagModel(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_createTag_error(self):
        """
        모델 생성시 slug도 존재해야함
        str -> name
        """

        PAYLOAD = dict(
            name="sample1",
        )
        tag = Tag.objects.create(**PAYLOAD)
        self.assertEqual(str(tag), PAYLOAD["name"])

        self.assertTrue(tag.slug)
        self.assertEqual(tag.name, PAYLOAD["name"])
