from unittest.mock import MagicMock
from django.test import TestCase
from ..preview import SingleObjectPreviewMixin
from .models import Article


class KawazSingleObjectPreviewMixinTestCase(TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.request.GET.dict.return_value = dict(
            foo='foo', bar='bar',
            hoge='hoge', piyo='piyo', ahya='ahya',
        )
        self.instance = SingleObjectPreviewMixin()
        self.instance.model = None
        self.instance.get_queryset = MagicMock(return_value=None)
        self.instance.request = self.request

    def test_has_get_object_method(self):
        """get_objectメソッドを所有する"""
        self.assertTrue(hasattr(SingleObjectPreviewMixin, 'get_object'))

    def test_get_object_with_model(self):
        """Modelに存在しないアトリビュートは削除される (model)"""
        expected = ('foo', 'bar')
        instance = self.instance
        instance.model = Article
        self.assertEqual(sorted(expected),
                         sorted(list(instance.get_object())))

    def test_get_object_with_get_queryset(self):
        """Modelに存在しないアトリビュートは削除される (get_queryset)"""
        expected = ('foo', 'bar')
        queryset = MagicMock()
        queryset.model = Article
        instance = self.instance
        instance.get_queryset = MagicMock(return_value=queryset)
        self.assertEqual(sorted(expected),
                         sorted(list(instance.get_object())))

    def test_get_object_with_queryset(self):
        """Modelに存在しないアトリビュートは削除される (queryset)"""
        expected = ('foo', 'bar')
        queryset = MagicMock()
        queryset.model = Article
        instance = self.instance
        self.assertEqual(sorted(expected),
                         sorted(list(instance.get_object(queryset))))
