# -*- coding: utf-8 -*-
from django import forms
from people.models import KnownLanguage, Person, Demographic
from corpus.base_settings import LANGUAGES, LANGUAGE_CODE, DIALECTS, ACCENTS
from dal import autocomplete
from django.db.models.fields import BLANK_CHOICE_DASH

# from django.conf.settings import LANGUAGES

# form = modelform_factory(KnownLanguage, fields = ('language', 'level_or_proficiency'), initial = 'set person somehow, max_num = len(available_languages)')

import logging
logger = logging.getLogger('corpora')


class KnownLanguageFormWithPerson(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        person = kwargs.pop('person', None)
        require_proficiency = kwargs.pop('require_proficiency', None)

        super(KnownLanguageFormWithPerson, self).__init__(*args, **kwargs)

        instance = kwargs['instance']  # this is a known language instance.

        # I have a feeling this will braeak when there's an empty instance - e.g. known language is None
        # We'll need to use autocomplete light to update fields when someone adds a new language.

        language_accents = None
        for i in range(len(ACCENTS)):
            if ACCENTS[i][0] == instance.language:
                language_accents = ACCENTS[i][1]

        language_dialects = None
        for i in range(len(DIALECTS)):
            if DIALECTS[i][0] == instance.language:
                language_dialects = DIALECTS[i][1]

        # if language_accents:
        #     self.fields['accent'].choices = ()
        #     self.fields['accent'].choices.append(BLANK_CHOICE_DASH)
        #     for i in language_accents:
        #         self.fields['accent'].choices.append(i)
        # if language_dialects:
        #     self.fields['dialect'].choices = ()
        #     self.fields['dialect'].choices.append(BLANK_CHOICE_DASH)
        #     for i in language_dialects:
        #         self.fields['dialect'].choices.append(i)

        self.fields['language'].disabled = True
        self.fields['accent'].choices = BLANK_CHOICE_DASH + list(language_accents)
        self.fields['dialect'].choices = BLANK_CHOICE_DASH + list(language_dialects)

        if require_proficiency:
            self.fields['level_of_proficiency'].required = require_proficiency


class PersonForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Person
        fields = ('full_name', 'email')


class DemographicForm(forms.ModelForm):
    # date_of_birth = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Demographic
        fields = ('age', 'sex', 'tribe')
        widgets = {
            'tribe': autocomplete.ModelSelect2Multiple(url='people:tribe-autocomplete')
        }


class DemographicFormAdmin(forms.ModelForm):
    # date_of_birth = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Demographic
        fields = ('__all__')
        widgets = {
            'tribe': autocomplete.ModelSelect2Multiple(url='people:tribe-autocomplete')
        }
