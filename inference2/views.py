import json
import os
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.conf import settings
import time

from .models import Output, InstructionFile, Algorithm, Profile
import importlib
from inference2.models import Input

from .models import Define3, Archives
import openpyxl
from openpyxl.cell import get_column_letter


def save_result(archive_id, post_data):
    Output.objects.filter(archives_id=archive_id).delete()
    archive = Archives.objects.get(pk=archive_id)
    Rows = []
    data_found = False

    for idx in range(len(post_data) - 1):
        if post_data.get("text_" + str(idx) + "_2", '') or post_data.get("text_" + str(idx) + "_3", ''):
            data_found = True
        if not data_found:
            continue
        c1 = post_data.get("text_" + str(idx) + "_1", '')
        c2 = post_data.get("text_" + str(idx) + "_2", '')
        c3 = post_data.get("text_" + str(idx) + "_3", '')
        if type(c1) == type([]):
            c1 = c1[0]
        if type(c2) == type([]):
            c2 = c2[0]
        if type(c3) == type([]):
            c3 = c3[0]
        R = Output(col1=c1,
                   col2=c2,
                   col3=c3,
                   archives=archive,
                   )
        Rows.append(R)
    Output.objects.bulk_create(Rows)


def current_archive():
    archive = Archives.objects.latest('archives_date')
    return archive


def index(request, archive=None):
    ins_file = InstructionFile.objects.filter(
        file_type='0').order_by('-id').first()
    if (ins_file):
        ins_file = '/' + str(ins_file.data)
    else:
        ins_file = ''
    progressbar_send(request, 1, 100, 1)
    url_path = ''
    archive_date = ''
    if not archive:
        archive = current_archive()
        url_path = '/'
    else:
        url_path = '/archives/{}/'.format(archive.id)
        archive_date = archive.archives_date
    input = Input.objects.filter(archives_id=archive.id)
    result = {}
    output = []
    # output = Output.objects.all()
    show_column = False
    if request.method == 'POST':
        show_column = True
        Output.objects.all().delete()
        post_data = request.POST.copy()
        prove_algorithm = importlib.import_module('.' + archive.algorithm.split('.py')[0], package='inference2.Proofs')
        prove_dictionary = importlib.import_module('.' + archive.dictionary.split('.py')[0],
                                                   package='inference2.Proofs')
        post_data = prove_algorithm.get_result(
            request.POST.copy(), archive.id, request, prove_dict=prove_dictionary)
        print(post_data)
        if post_data:
            post_data["type"] = "prove"
            result = json.dumps(post_data, cls=DjangoJSONEncoder)

            save_result(archive.id, post_data)
        output = Output.objects.all()

    algo = Algorithm.objects.latest('id')

    template_args = {'result': result, 'input': input,
                     'url_path': url_path, 'archive_date': archive_date,
                     'output': output, 'ins_file': ins_file,
                     'archive': archive, 'show_column': show_column, 'algo': algo.name if algo else archive
                     }
    return render(request, "inference2/index.html", template_args)


def try_input(request, archive=None):
    output = []
    if not archive:
        archive = current_archive()
        url_path = '/'
    if request.method == 'POST':
        # input = "It is|a contradictory that I do not have many|n points"
        input = request.POST.get('try_input')
        Output.objects.all().delete()
        prove_algorithm = importlib.import_module('.' + archive.algorithm.split('.py')[0], package='inference2.Proofs')
        post_data = prove_algorithm.get_result(
            request.POST.copy(), archive.id, request, input)
        print(post_data)
        if post_data:
            post_data["type"] = "prove"
            result = json.dumps(post_data, cls=DjangoJSONEncoder)

            save_result(archive.id, post_data)
        output = Output.objects.all()

    template_args = {
        'url_path': url_path,
        'output': output,
        'archive': archive,
    }
    return render(request, "inference2/try_input.html", template_args)


def export_xlsx(request, archives_id=None):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=mymodel.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    ws.title = "MyModel"
    only_output = request.GET.get('only_output', None)
    only_input = request.GET.get('only_input', None)

    queryset = Output.objects.filter(archives_id=int(archives_id))
    input_queryset = Input.objects.filter(archives_id=int(archives_id))
    row_num = 0

    columns = [
        (u"ID", 15),
        (u"Title", 70),
        (u"Description", 70),
    ]

    for col_num in range(len(columns)):
        c = ws.cell(row=row_num + 1, column=col_num + 1)
        c.value = columns[col_num][0]
        c.style.font.bold = True
        # set column width
        ws.column_dimensions[get_column_letter(
            col_num + 1)].width = columns[col_num][1]
    if not only_output:
        for obj in input_queryset:
            row_num += 1
            row = [
                obj.col1,
                obj.col2,
                obj.col3,
            ]
            for col_num in range(len(row)):
                c = ws.cell(row=row_num + 1, column=col_num + 1)
                c.value = row[col_num]
                c.style.alignment.wrap_text = True

    if not only_input:
        for obj in queryset:
            row_num += 1
            row = [
                obj.col1,
                obj.col2,
                obj.col3,
            ]
            for col_num in range(len(row)):
                c = ws.cell(row=row_num + 1, column=col_num + 1)
                c.value = row[col_num]
                c.style.alignment.wrap_text = True

    wb.save(response)
    return response


def stream_response_generator(request):
    for x in range(1, 11):
        yield "%s\n" % x  # Returns a chunk of the response to the browser
        request.session['idx'] = x
        request.session.modified = True

        request.session.save()
        time.sleep(1)


def prove(request, archive=None):
    progressbar_send(request, 1, 100, 1)
    if not archive:
        archive = current_archive()
    result = {}
    if request.method == 'POST':
        post_data = request.POST.copy()
        prove_algorithm = importlib.import_module(
            '.' + archive.algorithm, package='inference2.Proofs')
        post_data = prove_algorithm.get_result(
            request.POST.copy(), archive.id, request)
        result = json.dumps(post_data, cls=DjangoJSONEncoder)

    return result


def dictionary(request, archive=None):
    # url_path = '/archives/'
    # if not archive:
    #     archive = current_archive()
    #     url_path = '/'
    # else:
    #     url_path = '/archives/{}/'.format(archive.id)
    # dict = Define3.objects.filter(archives_id=archive.id)
    from inference2.Proofs.dictionary_new import large_dict
    outputs = Define3.objects.all()
    return render(request, "inference2/dict.html", {'result': large_dict, 'url_path': '/', 'output': outputs})


def tested_dictionary(request, archive=None):
    from inference2.Proofs.dictionary_tested import large_test_dict
    return render(request, "inference2/tested_dict.html", {'result': large_test_dict, 'url_path': '/'})


def download_files(request):
    ins_files = InstructionFile.objects.filter(
        file_type='1').order_by('-id')
    return render(request, "inference2/files.html", {'ins_files': ins_files})


# def download_files_in_brief(request):
#     ins_files = InstructionFile.objects.filter(
#         file_type='2').order_by('-id')
#     return render(request, "inference2/files_in_brief.html", {'ins_files': ins_files})


def archives(request):
    dict = Archives.objects.all()
    return render(request, "inference2/archives.html", {'result': dict})


def assign_archives(request, num=-1, type=None):
    if num == -1:
        return
    archive = Archives.objects.get(pk=num)
    if type:
        return globals()[type](request, archive)
    else:
        return index(request, archive)


def manual(request):
    filename = os.path.join(settings.MANUAL_PATH)
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(
        wrapper, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=' + \
                                      os.path.basename(filename)
    return response


def getdict(request, archive=None):
    if not archive:
        archive = current_archive()

    filename = os.path.join(settings.DICT_DIRS, archive.algorithm + ".csv")
    if not os.path.exists(filename):
        return HttpResponse("No CSV found for Algorithm %s" % archive.algorithm)
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(
        wrapper, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=' + \
                                      os.path.basename(filename)
    return response


def progress(request):
    contxt = {"K": request.session['idx']}
    if request.session.get('status', 0) == 2:
        progressbar_send(request, 1, 100, 1)
        print("prog123 %s" % contxt)
    return HttpResponse(json.dumps(contxt), content_type="application/json")


def progressbar_send(request, strt, stp, k, status=0):
    if request is not None:
        request.session.modified = True
        request.session['strt'] = 0
        request.session['stp'] = 100
        request.session['idx'] = [0, 100, k]
        request.session['status'] = status
        request.session.modified = True
        request.session.save()


def author(request):
    profile = Profile.objects.latest('id')
    return render(request, "inference2/author.html", {'profile': profile})


def clear(request):
    return redirect(reverse('index'))