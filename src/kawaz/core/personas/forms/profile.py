from django import forms
from django.forms import ModelForm
from django.forms.utils import flatatt
from django.forms.models import inlineformset_factory
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.forms import widgets
from kawaz.core.forms.fields import MarkdownField
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import (Bootstrap3HorizontalFormHelperMixin,
                                     Bootstrap3InlineFormHelperMixin)
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton

from ..models import Profile, Service
from ..models import Skill
from ..models import Account


class ProfileForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):
    form_tag = False

    skills = forms.ModelMultipleChoiceField(
        label=_('Skills'),
        widget=widgets.CheckboxSelectMultiple,
        queryset=Skill.objects.all().order_by('pk'), required=False)
    remarks = MarkdownField(label=pgettext_lazy('Profile', 'Remarks'))
    birthday = forms.DateField(label=_('Birthday'),
                               widget=forms.DateInput(attrs={'type': 'date'}),
                               required=False)

    class Meta:
        model = Profile
        exclude = (
            'user',
            'created_at',
            'updated_at',
        )

    def get_additional_objects(self):
        # Saveボタンを描画しない
        return []

class ServiceSelectWidget(widgets.Select):
    """
    サービスを選択するフォームセットのサービスを選択するフィールド用のWidget
    選択項目にサービスのfaviconが埋め込まれるようになっている
    """

    def render_options(self, *args, **kwargs):
        self.option_urls = {str(s.pk): '' if not s.icon else s.icon.url
                            for s in Service.objects.all()}
        return super().render_options(*args, **kwargs)

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        url = self.option_urls.get(option_value, '')
        return format_html('<option value="{}" icon-url="{}"{}>{}</option>',
                           option_value,
                           url,
                           selected_html,
                           force_text(option_label))


class AccountForm(Bootstrap3InlineFormHelperMixin, ModelForm):
    form_tag = False
    service = forms.ModelChoiceField(label=_('Service'),
                                     queryset=Service.objects.all(),
                                     widget=ServiceSelectWidget)

    class Meta:
        model = Account
        fields = (
            'service',
            'username',
            'pub_state',
        )
        exclude = ('user',)


AccountFormSet = inlineformset_factory(Profile, Account, form=AccountForm,
                                       extra=1, can_delete=True)
