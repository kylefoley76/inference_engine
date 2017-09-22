from django.contrib import admin
from django import forms
import os.path
import pkgutil
from inference2 import Proofs
from inference2.models import Define3, Archives, Profile
from django.contrib.auth.models import User
from django.forms import ModelForm

from django.contrib import admin

try:
    from admin_import.options import add_import
except ImportError:
    pass
else:
    add_import(admin.ModelAdmin, add_button=True)
from inference2.models import Define3, Input, Output, InstructionFile, Algorithm
from django.contrib import admin
from .actions import export_as_csv_action
from .actions import change_text_to_symbol_action
from .actions import change_symbol_to_text_action
from .actions import export_as_json_action
from .actions import export_as_xml_action
from .actions import export_as_yaml_action

from .admincsv import ImportCSVModelAdmin

admin.site.add_action(export_as_csv_action)
admin.site.add_action(change_text_to_symbol_action)
admin.site.add_action(change_symbol_to_text_action)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'extra', 'type', 'word', 'rel', '')
    empty_value_display = ""
    ordering = ("id",)
    list_per_page = 1000


# admin.site.register(Define3, AuthorAdmin)
class MyDefineImporter(ModelForm):
    class Meta:
        model = Define3
        fields = ('id', 'extra', 'type', 'word',
                  'rel', 'definition', 'subject', 'def_object', 'archives')


class MyDefineForm(ModelForm):
    class Meta:
        model = Define3
        fields = ('id', 'extra', 'type', 'word',
                  'rel', 'definition', 'subject', 'def_object', 'archives')


def delete_everything(modeladmin, request, queryset):
    Define3.objects.all().delete()


class MyDefine(ImportCSVModelAdmin):
    importer_class = MyDefineImporter
    form = MyDefineForm
    list_display = ('id', 'extra', 'type', 'word', 'rel', 'definition', 'subject', 'def_object',)
    empty_value_display = ""
    ordering = ("id",)
    list_per_page = 100
    actions = [delete_everything]


class MyInputImporter(ModelForm):
    class Meta:
        model = Input
        fields = ('col1', 'col2', 'col3', 'archives')


class MyInputForm(ModelForm):
    class Meta:
        model = Input
        fields = ('col1', 'col2', 'col3', 'archives')


class MyInput(ImportCSVModelAdmin):
    importer_class = MyInputImporter
    form = MyInputForm
    list_display = ('col1', 'col2', 'col3', 'archives')
    empty_value_display = ""
    ordering = ("id",)
    list_per_page = 50


class MyArchiveImporter(ModelForm):
    class Meta:
        model = Archives
        fields = ('archives_date', 'algorithm')


class MyArchiveForm(ModelForm):
    def get_my_choices():
        return [(_.data.name.split('/')[-1], _.data.name.split('/')[-1])
                for _ in Algorithm.objects.all()]

    def get_my_dict_choices():
        return [(_.dictionary.name.split('/')[-1] if _.dictionary else '',
                 _.dictionary.name.split('/')[-1] if _.dictionary else '')
                for _ in Algorithm.objects.all()]

    algorithm = forms.ChoiceField(choices=get_my_choices)
    dictionary = forms.ChoiceField(choices=get_my_dict_choices)

    class Meta:
        model = Archives
        fields = ('archives_date', 'algorithm')


class MyArchive(ImportCSVModelAdmin):
    importer_class = MyArchiveImporter
    form = MyArchiveForm
    list_display = ('archives_date', 'algorithm', 'input_link',
                    'output_link', 'dictionary_link')
    ordering = ("archives_date",)
    list_per_page = 1000
    empty_value_display = ""

    def input_link(self, obj):
        return '<a href="/export_xlsx/%d?only_input=1" class="link">Download input</a>' % obj.id

    input_link.short_description = 'Inputs'
    input_link.allow_tags = True

    def dictionary_link(self, obj):
        return '<a href="/export_xlsx/%d" class="link">Download dictionary</a>' % obj.id

    dictionary_link.short_description = 'Dictionaries'
    dictionary_link.allow_tags = True

    def output_link(self, obj):
        return '<a href="/export_xlsx/%d?only_output=1" class="link">Download argument</a>' % obj.id

    output_link.short_description = 'Outputs'
    output_link.allow_tags = True


class OutputAdmin(admin.ModelAdmin):
    list_display = ('col1', 'col2', 'col3', 'archives')
    empty_value_display = ""
    ordering = ("id",)
    list_per_page = 50


class AlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'data', 'dictionary', 'created_at')
    empty_value_display = ""
    ordering = ("id",)
    list_per_page = 50


class InstructionFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file_type', 'color_type')
    ordering = ("id",)
    list_per_page = 50


"""
class MyArchivesForm(admin.ModelAdmin):
    list_display = ('archives_date','algorithm')
    ordering = ("archives_date",)
    list_per_page = 1000
"""


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'about', 'hobbies', 'skills', 'facebook', 'twitter', 'instagram')
    ordering = ("id",)
    list_per_page = 50


admin.site.register(Define3, MyDefine)
admin.site.register(Input, MyInput)
admin.site.register(Archives, MyArchive)
admin.site.register(Output, OutputAdmin)
admin.site.register(InstructionFile, InstructionFileAdmin)
admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Profile, ProfileAdmin)
