from unittest.mock import MagicMock
from django.contrib.contenttypes.models import ContentType
from django.template import Context
from django.test import TestCase
from activities.mediator import ActivityMediator
from activities.models import Activity
from activities.registry import registry
from .factories import CommentTestArticleFactory
from .factories import CommentFactory
from kawaz.core.activities.tests.factories import ActivityFactory
from kawaz.core.comments.tests.models import CommentTestArticle

__author__ = 'giginet'


class CommentActivityMediatorTestCase(TestCase):
    def setUp(self):
        registry.register(CommentTestArticle, ActivityMediator())

    def test_add_comment(self):
        """
        あるオブジェクトにコメントが付いたとき、そのオブジェクトのイベントとして、`add_comment`Activityが付く
        """
        target_object = CommentTestArticleFactory()

        nactivities = Activity.objects.get_for_object(target_object).count()

        # コメントをする
        comment = CommentFactory(content_object=target_object)

        activities = Activity.objects.get_for_object(target_object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        self.assertEqual(activity.status, 'add_comment')
        self.assertEqual(activity.snapshot, target_object)
        # remarksにコメントのpkが入る
        self.assertEqual(activity.remarks, str(comment.pk))

    def test_render_add_comment(self):
        """
         render_activityでadd_commentが正しく表示できる
        """
        target_object = CommentTestArticleFactory()
        ct = ContentType.objects.get_for_model(CommentTestArticle)
        pk = target_object.pk
        activity = ActivityFactory(content_type=ct, object_id=pk, status='add_comment')
        mediator = registry.get(activity)

        self.assertTrue(mediator.render(activity, Context()))

    def test_comment_delete(self):
        """
        コメントが削除されても特に通知されない
        """
        # コメントをする
        comment = CommentFactory()
        target_object = comment.content_object

        nactivities = Activity.objects.get_for_object(target_object).count()

        # コメントを削除する
        comment.delete()
        self.assertEqual(Activity.objects.get_for_object(target_object).count(), nactivities)

    def test_comment_update(self):
        """
        コメントが更新されても特に通知されない
        """
        # コメントをする
        comment = CommentFactory()
        target_object = comment.content_object

        nactivities = Activity.objects.get_for_object(target_object).count()

        # コメントを変更する
        comment.comment = 'コメント書き換えコメント書き換えコメント書き換え'
        comment.save()

        # 特に何も生成されてないはず
        self.assertEqual(Activity.objects.get_for_object(target_object).count(), nactivities)
