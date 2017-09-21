import csv

from django.db import transaction
from django import forms
from django.forms.forms import NON_FIELD_ERRORS
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from inference2.models import Archives, Define3

from django.forms import ModelChoiceField


class CSVImportError(Exception):
    pass


class ImportCSVForm(forms.Form):
    csv_file = forms.FileField(required=True, label=_('CSV File'))
    has_headers = forms.BooleanField(
        label=_('Has headers'),
        help_text=_('Check this if your CSV file '
                    'has a row with column headers.'),
        initial=True,
        required=False,
    )
    archives = forms.ModelChoiceField(
        queryset=Archives.objects.all(),
        label=_('Select for Archives'),
        required=False,
        help_text=_('Create Archives if it is not here.'),
    )
    archives_check = forms.BooleanField(
        label=_('Check for Old Archives'),
        help_text=_('UnCheck this if your Definition has to replace '
                    'the old entries of same archive date.'),
        initial=True,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.importer_class = kwargs.pop('importer_class')
        self.dialect = kwargs.pop('dialect')
        super(ImportCSVForm, self).__init__(*args, **kwargs)
        self.fields['csv_file'].help_text = "Expected fields: {}".format(
            self.expected_fields)

    # def clean_csv_file(self):
    #     if six.PY3:
    #         # DictReader expects a str, not bytes in Python 3.
    #         csv_text = self.cleaned_data['csv_file'].read()
    #         csv_decoded = six.StringIO(csv_text.decode('utf-8'))
    #         print(csv_decoded)
    #         return csv_decoded
    #     else:
    #         return self.cleaned_data['csv_file']

    @property
    def expected_fields(self):
        fields = self.importer_class._meta.fields
        return ', '.join(fields)

    @transaction.atomic
    def import_csv(self):
        try:
            # print(self.cleaned_data['csv_file'])
            data = str(self.cleaned_data['csv_file'].read())
            lines = data.split('\\n')
            if len(lines) < 3:
                lines = data.split('\\r')
            reader = []
            fieldnames = self.importer_class.Meta.fields
            for line in lines:
                words = line.replace('"', '').replace("\\'", "'").split(',')
                temp = {}
                for index, value in enumerate(fieldnames):
                    try:
                        temp[value] = words[index]
                    except IndexError:
                        pass

                reader.append(temp)
            # reader =
            # reader = csv.DictReader(
            #     self.cleaned_data['csv_file'],
            #     fieldnames=self.importer_class.Meta.fields,
            #     dialect=self.dialect,
            # )
            print(reader)
            reader_iter = enumerate(reader, 1)
            archives_id = -1  # No Archives
            if self.cleaned_data['has_headers']:
                six.advance_iterator(reader_iter)
            if self.cleaned_data['archives']:
                archives_id = self.cleaned_data['archives'].id
            old_archives = self.importer_class.Meta.model.objects.filter(
                id=archives_id)
            if old_archives:
                # if self.cleaned_data['archives_check']:
                #     self.append_import_error(_("Defination already exist for this archives."))
                #     raise CSVImportError()
                # else:
                old_archives.delete()
            self.process_csv(reader_iter, archives_id)
            if not self.is_valid():
                raise CSVImportError()  # Abort the transaction
        except csv.Error:
            self.append_import_error(_("Bad CSV format"))
            raise CSVImportError()

    def process_csv(self, reader, archives_id=-1):
        list_obj = []
        for i, row in reader:
            # if not row.get('definition') and 'definition' in self.importer_class.Meta.fields:
            #     # SKIP empty rows
            #     continue
            if archives_id != -1:
                row['archives'] = archives_id
            row_result = self.process_row(i, row)
            if row_result:
                list_obj.append(row_result)

                # if list_obj:
                #     list_obj[0].__class__.objects.bulk_create(
                #         list_obj, batch_size=len(list_obj))

    def append_import_error(self, error, rownumber=None, column_name=None):
        if rownumber is not None:
            if column_name is not None:
                # Translators: "{row}", "{column}" and "{error}"
                # should not be translated
                fmt = _("Could not import row #{row}: {column} - {error}")
            else:
                # Translators: "{row}" and "{error}" should not be translated
                fmt = _("Could not import row #{row}: {error}")
        else:
            if column_name is not None:
                raise ValueError("Cannot raise a CSV import error on a specific "
                                 "column with no row number.")
            else:
                # Translators: "{error}" should not be translated
                fmt = _("Could not import the CSV document: {error}")

        if NON_FIELD_ERRORS not in self._errors:
            self._errors[NON_FIELD_ERRORS] = self.error_class()
        self._errors[NON_FIELD_ERRORS].append(
            fmt.format(error=error, row=rownumber, column=column_name))

    def process_row(self, i, row):
        importer = self.importer_class(data=row)
        if importer.is_valid():
            return importer.save(commit=True)
        else:
            for error in importer.non_field_errors():
                self.append_import_error(rownumber=i, error=error)
            for field in importer:
                for error in field.errors:
                    self.append_import_error(rownumber=i, column_name=field.label,
                                             error=error)
            return None
