import requests
import json
import os
# import codecs

input_file = 'C:\\Users\\1596949\\Documents\\Test_Input_Folder\\1005027-041218.000001.01.01.tif'


with open(input_file, 'rb') as f:

    binary_data = f.read()

headers = {"env": 'NP2', 'org' : 'gfs', 'country' : 'IND', 'foldername' : 'test_folder', 'filename' : 'test_file.tif', 'mode' : ''}

# json_data = json.dumps(data)

url = "http://127.0.0.1:8000/ib_call/"
resp_data = requests.post(url, headers = headers, data = binary_data, verify = False)
print(resp_data.content)