from django.contrib.contenttypes.models import ContentType
from activities.mediator import ActivityMediator

__author__ = 'giginet'

class ProfileActivityMediator(ActivityMediator):
    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'updated':
            # あるユーザーのプロフィールが更新されたとき
            # そのActivityをプロフィールについてではなく、
            # そのプロフィールの持ち主のユーザーに所属させる
            target = instance.user
            ct = ContentType.objects.get_for_model(type(target))
            pk = target.pk
            activity.content_type = ct
            activity.object_id = pk
            activity.status = 'profile_updated'

            previous = activity.previous.snapshot
            is_created = lambda x: (
                not getattr(previous, x, None) and
                getattr(instance, x)
            )
            is_updated = lambda x: (
                getattr(previous, x, None) and
                getattr(instance, x) and
                getattr(previous, x) != getattr(instance, x)
            )
            is_deleted = lambda x: (
                getattr(previous, x, None) and
                not getattr(instance, x)
            )
            remarks = []
            attributes = (
                'remarks',
                'birthday',
                'place',
                'url'
            )
            for attribute in attributes:
                if is_created(attribute):
                    remarks.append(attribute + '_created')
                elif is_updated(attribute):
                    remarks.append(attribute + '_updated')
                elif is_deleted(attribute):
                    remarks.append(attribute + '_deleted')
            if not remarks:
                # 通知が必要な変更ではないため通知しない
                return None
            activity.remarks = "\n".join(remarks)
        return activity


class AccountActivityMediator(ActivityMediator):
    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'created':
            # プロフィールに新しくサービスアカウントが作成されたとき
            # このActivityをユーザーの物にしてしまう
            # また、ステータスも`add_account`に変える
            # remarksには付いたアカウントのPKを入れる
            target = instance.profile.user
            ct = ContentType.objects.get_for_model(type(target))
            pk = target.pk
            activity.content_type = ct
            activity.object_id = pk
            activity.status = 'add_account'
            activity.remarks = str(instance.pk)
            return activity