from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermissions
from rest_framework import filters
from .filters import KawazObjectPermissionFilterBackend

class KawazGenericViewSetMixin(GenericViewSet):
    renderer_classes = (JSONRenderer,)
    author_field_name = None
    permission_classes = (DjangoObjectPermissions, DjangoModelPermissions)
    filter_backends = (filters.DjangoFilterBackend, KawazObjectPermissionFilterBackend)

    def pre_save(self, obj):
        if self.author_field_name and self.request.user.is_authenticated():
            setattr(obj, self.author_field_name, self.request.user)

    def get_queryset(self):
        manager = self.model.objects
        if self.request.method == 'GET':
            return self.get_queryset_for_read(manager)
        return self.get_queryset_for_write(manager)

    def get_queryset_for_read(self, manager):
        if hasattr(manager, 'published'):
            return manager.published(self.request.user)
        return manager.all()

    def get_queryset_for_write(self, manager):
        if hasattr(manager, 'related'):
            return manager.related(self.request.user)
        return manager.all()


class KawazReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                                  mixins.ListModelMixin,
                                  KawazGenericViewSetMixin,
                                  GenericViewSet):
    """
    パーミッションを考慮した読み込み専用のViewSetです
    retrieve, listAPIのみを提供します
    """


class KawazModelViewSet(KawazGenericViewSetMixin,
                               ModelViewSet):
    """
    パーミッションを考慮した汎用的なViewSetです
    retrieve, listに加え、create, destroy, update, partial_updateを提供します
    """