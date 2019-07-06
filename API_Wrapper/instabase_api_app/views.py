# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import requests
import os
from requests.auth import HTTPBasicAuth
import instabase_api_calls
import pandas as pd
from StringIO import StringIO

# Create your views here.

@api_view(["POST"])
def test_api_call(jsondata, format = str):
    
    try:
        
        env = jsondata.META['HTTP_ENV']
        org = jsondata.META['HTTP_ORG']
        country = jsondata.META['HTTP_COUNTRY']
        folder_name = jsondata.META['HTTP_FOLDERNAME']
        file_name = jsondata.META['HTTP_FILENAME']
        file_data = jsondata.body
        mode = jsondata.META['HTTP_MODE']

        # create_folder
        resp = instabase_api_calls.ib_create_folder(env = env, org = org, country = country, folder_name = folder_name)
        
        if resp[u'status'] != 'OK':
            return JsonResponse("Folder Status: Not Created", safe=False)
                
        # upload_files

        resp = instabase_api_calls.ib_create_file(env = env, org = org, country = country, folder_name = folder_name, file_name = file_name, file_data = file_data)

        if resp[u'status'] != 'OK':
            return JsonResponse("File Status: Not Created", safe=False)

        #trigger_flow
        resp = instabase_api_calls.ib_trigger_flow(env = env, org = org, country = country, folder_name = folder_name)
        
        job_id = resp[u'data'][u'job_id']
        output_path = resp[u'data'][u'output_folder']

        # output_path = output_path.replace('/', '', 1)
        # if org == 'gfs':
        #     output_path = output_path + '/s4_merge_files'
        
        if mode == 'async':
            return JsonResponse("Your flow has been initiated. You will receive your output in your target location.", safe=False)
        
        # #monitor_flow_status

        flow_status = True
        max_retries = 30
        retries = 0

        while flow_status:

            try:
                resp = instabase_api_calls.ib_flow_status(env = env, org = org, country = country, job_id = job_id)

                if resp[u'state'] == 'DONE':
                    flow_status = False
            
            except:
                
                if retries > max_retries:
                    return JsonResponse("Max reretries to get flow status exceeded", safe=False)
                else:
                    retries+= 1
                
        #get_flow_output
        resp = instabase_api_calls.ib_flow_output(env = env, org = org, country = country, out_path = output_path)
        data = resp[u'csv_text']

        # TESTDATA = StringIO(data)

        # df = pd.read_csv(TESTDATA, sep=",")
        # df = df.astype(str)

        return JsonResponse("Output CSV Text: " + data, safe=False)

    except ValueError as e:

        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)