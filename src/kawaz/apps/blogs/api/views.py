# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/19
#
__author__ = 'giginet'
from kawaz.api import mixins
from kawaz.api.views import KawazGenericViewSet
from .serializers import CategorySerializer
from ..models import Category


class CategoryViewSet(mixins.CreateModelMixin,
                      KawazGenericViewSet):
    """
    ブログカテゴリを作成するためのAPIエンドポイント
    """
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    author_field_name = 'author'