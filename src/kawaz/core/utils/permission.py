# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.core.exceptions import ObjectDoesNotExist
from permission.utils.permissions import perm_to_permission


def check_object_permission(user_obj, codename, obj):
    """
    指定ユーザが省略形パーミッションを指定オブジェクトに対して持つか調べる

    Args:
        user_obj (user instance): 対象ユーザインスタンス
        codename (str): 省略形パーミッション（例: `'add'`）
        obj (model instance): 対象モデルインスタンス

    Returns:
        bool or None: 指定されたパーミッションが存在する場合は`True`/`False`を
            返し、存在しない場合は`None`を返す
    """
    try:
        perm = get_full_permission_name(codename, obj)
        # 文字列 permission を実体に変換（してみる）
        perm_to_permission(perm)
        # 指定されたパーミッションが存在するためチェックを行う
        return user_obj.has_perm(perm, obj=obj)
    except ObjectDoesNotExist:
        # 指定されたパーミッションが存在しないため None を返す
        return None


def get_full_permission_name(codename, obj):
    """
    Return permission string from codename and model

    Args:
        codename (str): A codename of the permission (e.g. 'add')
        obj (instance): An instance of model
    """
    app_label = obj._meta.app_label
    model_name = obj._meta.object_name.lower()
    perm = '{}.{}_{}'.format(app_label, codename, model_name)
    return perm


def filter_with_perm(user_obj, qs, perm):
    """
    Filter the queryset or list of object with object permission

    Args:
        user_obj (obj): An instance of User model
        qs (obj): An instance of QuerySet or list of object
        perm (string): A name of the permission（e.g. 'add'）

    Returns:

    """
    perm = get_full_permission_name(perm, qs.model)
    iterator = qs if isinstance(qs, (list, tuple)) else qs.iterator()
    iterator = filter(lambda x: user_obj.has_perm(perm, obj=x), iterator)
    return iterator
