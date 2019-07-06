#!/usr/bin/env python

import os
import requests
import json
from StringIO import StringIO
import pandas as pd
import sqlalchemy

def ib_parameters(env, org, country):

    if env == 'NP1':
        HOST_URL = 'https://instabase.apps.edm-hk-np1.ocp.standardchartered.com/api/v1/drives'
        API_TOKEN = 'qxlhBzpMF6UciCekaTMzsaSfJAZMjb'
    else:
        HOST_URL = 'https://instabase.apps.edm-hk-np2.ocp.standardchartered.com/api/v1/drives'
        API_TOKEN = 'BDSaEXogfZtpAozhTKW3bfKmtPgfzU'

    ROOT_DICT = {'gfs' : {'flow_root_dir' : '{}/GFS/GFSINVOICE-DEV/fs/Instabase Drive/GFS/{}/workflows/'.format(HOST_URL, country),
                          'flow_bin_root_dir' : '{}/GFS/GFSINVOICE-DEV/fs/Instabase Drive/GFS/{}/build/bin/'.format(HOST_URL, country),
                          'samples_root_dir' : '{}/GFS/GFSINVOICE-DEV/fs/Instabase Drive/GFS/{}/samples/'.format(HOST_URL, country)}}
    
    FLOW_DICT = {'gfs' : 'Multiple_Invoices_'}

    SAMPLES_ROOT_DIR = ROOT_DICT[org]['samples_root_dir']
    FLOW_ROOT_DIR = ROOT_DICT[org]['flow_root_dir']
    FLOW_NAME = FLOW_DICT[org]
    FLOW_BIN_ROOT_DIR = ROOT_DICT[org]['flow_bin_root_dir']

    return  HOST_URL, API_TOKEN, SAMPLES_ROOT_DIR, FLOW_ROOT_DIR, FLOW_NAME, FLOW_BIN_ROOT_DIR

def ib_create_folder(env, org, country, folder_name):
    
    _, API_TOKEN, SAMPLES_ROOT_DIR, _, _, _ = ib_parameters(env, org, country)

    URL_BASE = '{}{}'.format(SAMPLES_ROOT_DIR, folder_name)

    api_args=dict(
    type='folder',
    )

    headers = {
        'Authorization': 'Bearer {0}'.format(API_TOKEN),
        'Instabase-API-Args': json.dumps(api_args)
    }

    data = None

    resp = requests.post(URL_BASE, headers=headers, data = data, verify = False)

    try:
        resp = resp.json()
    except:
        pass

    return resp

def ib_create_file(env, org, country, folder_name, file_name = None, file_data = None):

    _, API_TOKEN, SAMPLES_ROOT_DIR, _, _, _ = ib_parameters(env, org, country)

    URL_BASE = '{}{}/{}'.format(SAMPLES_ROOT_DIR, folder_name, file_name)

    api_args=dict(
    type='file',
    cursor=1,
    if_exists='overwrite'
    # mime_type='jpg'
    )

    headers = {
        'Authorization': 'Bearer {0}'.format(API_TOKEN),
        'Instabase-API-Args': json.dumps(api_args)
    }

    resp = requests.post(URL_BASE, headers=headers, data = file_data, verify = False)

    try:
        resp = resp.json()
    except:
        pass

    return resp

def ib_trigger_flow_binary(env, org, country, folder_name):

    HOST_URL, API_TOKEN, SAMPLES_ROOT_DIR, _, FLOW_NAME, FLOW_BIN_ROOT_DIR = ib_parameters(env, org, country)

    URL_BASE = '{}{}'.format(HOST_URL.replace('drives',''),'flow/run_binary_async')

    api_args = {
    'input_dir': '{}{}'.format(SAMPLES_ROOT_DIR.replace(HOST_URL,''), folder_name),
    'binary_path': '{}{}{}/{}{}.ibflowbin'.format(FLOW_BIN_ROOT_DIR.replace(HOST_URL,''),FLOW_NAME, country, FLOW_NAME, country),
    'settings': {
        'delete_out_dir': False,
        'output_has_run_id': True,
        'notification_emails': ["Venkatesh.KM1@sc.com"],
    },
    'post_flow_fn': 'csv_to_excel'
    }

    headers = {
        'Authorization': 'Bearer {0}'.format(API_TOKEN),
        'Instabase-API-Args': json.dumps(api_args)
    }

    data = json.dumps(api_args)

    resp = requests.post(URL_BASE, headers=headers, data = data, verify = False)

    try:
        resp = resp.json()
    except:
        pass

    return resp

def ib_trigger_flow(env, org, country, folder_name):

    HOST_URL, API_TOKEN, SAMPLES_ROOT_DIR, FLOW_ROOT_DIR, FLOW_NAME, _ = ib_parameters(env, org, country)

    URL_BASE = '{}{}'.format(HOST_URL.replace('drives',''),'flow/run_flow_async')

    api_args=dict(
        input_dir='{}{}'.format(SAMPLES_ROOT_DIR.replace(HOST_URL,''), folder_name),
        ibflow_path='{}{}{}.ibflow'.format(FLOW_ROOT_DIR.replace(HOST_URL,''),FLOW_NAME, country),
        output_has_run_id=False,
        post_flow_fn= 'csv_to_excel'
    )

    headers = {
        'Authorization': 'Bearer {0}'.format(API_TOKEN),
        'Instabase-API-Args': json.dumps(api_args)
    }

    data = json.dumps(api_args)

    resp = requests.post(URL_BASE, headers=headers, data = data, verify = False)

    try:
        resp = resp.json()
    except:
        pass

    return resp

def ib_flow_status(env, org, country, job_id):

    HOST_URL, API_TOKEN, _, _, _, _ = ib_parameters(env, org, country)

    URL_BASE = '{}{}{}'.format(HOST_URL.replace('drives',''),'jobs/status?job_id=',job_id)

    headers = {
        'Authorization': 'Bearer {0}'.format(API_TOKEN),
    }

    resp = requests.get(URL_BASE, headers=headers, data = None, verify = False)

    try:
        resp = resp.json()
    except:
        pass

    return resp

def ib_flow_output(env, org, country, out_path):

    HOST_URL, API_TOKEN, _, _, _, _ = ib_parameters(env, org, country)

    URL_BASE = '{}{}'.format(HOST_URL.replace('drives',''),'flow/export/review_batch')

    headers = {
        'Authorization': 'Bearer {0}'.format(API_TOKEN),
    }

    out_path = out_path + '/out.ibocr'

    data = {"path": out_path}
    data = json.dumps(data)

    resp = requests.post(URL_BASE, headers=headers, data = data, verify = False)

    try:
        resp = resp.json()
    except:
        pass

    return resp