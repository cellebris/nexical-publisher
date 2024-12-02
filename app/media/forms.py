from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from django_select2 import forms as s2forms

from . import models


class AccessTeamWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["name__icontains", "owner__email"]


class MediaCollectionForm(forms.ModelForm):
    class Meta:
        model = models.TeamMediaCollection
        fields = ["name", "description", "access_teams"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
            "access_teams": AccessTeamWidget,
        }

    def __init__(self, team, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["access_teams"].queryset = self.fields["access_teams"].queryset.exclude(id=team.id)


class MediaCollectionFileForm(forms.ModelForm):
    class Meta:
        model = models.TeamMedia
        fields = ["file", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class BaseMediaCollectionFileFormSet(BaseInlineFormSet):
    def full_clean(self):
        super().full_clean()

        for error in self._non_form_errors.as_data():
            if error.code == "too_many_forms":
                error.message = f"Only {self.max_num} files may be specified per media collection"


MediaCollectionFileFormSet = inlineformset_factory(
    models.TeamMediaCollection,
    models.TeamMedia,
    formset=BaseMediaCollectionFileFormSet,
    form=MediaCollectionFileForm,
    min_num=0,
    max_num=100,
    extra=0,
    can_delete=True,
    validate_max=True,
)


class MediaCollectionBookmarkForm(forms.ModelForm):
    class Meta:
        model = models.TeamMediaBookmark
        fields = ["url", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class BaseMediaCollectionBookmarkFormSet(BaseInlineFormSet):
    def full_clean(self):
        super().full_clean()

        for error in self._non_form_errors.as_data():
            if error.code == "too_many_forms":
                error.message = f"Only {self.max_num} webpages may be specified per media collection"


MediaCollectionBookmarkFormSet = inlineformset_factory(
    models.TeamMediaCollection,
    models.TeamMediaBookmark,
    formset=BaseMediaCollectionBookmarkFormSet,
    form=MediaCollectionBookmarkForm,
    min_num=0,
    max_num=100,
    extra=0,
    can_delete=True,
    validate_max=True,
)
