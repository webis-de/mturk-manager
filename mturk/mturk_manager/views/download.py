import urllib.parse
import json, csv
import os
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from mturk_manager.models import *
from mturk_manager.views.view import normalize_answer

def download(request, name):
    context = {}
    name_quoted = name
    name_project = urllib.parse.unquote(name_quoted)
    db_obj_project = m_Project.objects.prefetch_related(
        'messages_reject'
    ).get(name=name_project)

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=' + 'results.csv'


    writer = None
    list_ids = json.loads(request.GET['list_ids'])

    for index, assignment in enumerate(m_Assignment.objects.filter(id__in=list_ids).select_related('fk_hit')):
        dict_question = json.loads(assignment.fk_hit.parameters)
        # print(dict_question.keys())

        dict_answer = json.loads(normalize_answer(assignment.answer))
        # print(dict_answer.keys())

        dict_result = {}
        dict_result.update(dict_question)
        dict_result.update(dict_answer)


        if index == 0:
            writer = csv.DictWriter(response, fieldnames=sorted(dict_result.keys()))
            writer.writeheader()

        writer.writerow(dict_result)

    return response

    return JsonResponse({})