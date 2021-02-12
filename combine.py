"""
   Copyright 2021 InfAI (CC SES)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import os
import uuid
import requests


dep_instance = os.getenv("DEP_INSTANCE")
job_callback_url = os.getenv("JOB_CALLBACK_URL")
delimiter = os.getenv("delimiter")
time_column = os.getenv("time_column")
source_file_field = "source_file"
data_cache_path = "/data_cache"
output_file = uuid.uuid4().hex
inputs = list()
for key, value in os.environ.items():
    if source_file_field in key:
        inputs.append(value)


def merge_files(file_1_name, file_2_name, out_file_name=uuid.uuid4().hex):
    out_file = open("{}/{}".format(data_cache_path, out_file_name), "w")
    file_1 = open("{}/{}".format(data_cache_path, file_1_name), "r")
    file_2 = open("{}/{}".format(data_cache_path, file_2_name), "r")
    first_line_1 = file_1.readline().strip()
    first_line_2 = file_2.readline().strip()
    first_line_2 = first_line_2.split(delimiter)
    time_col_2 = first_line_2.index(time_column)
    first_line_2.remove(time_column)
    new_first_line = first_line_1 + delimiter + delimiter.join(first_line_2)
    out_file.write(new_first_line + "\n")
    new_first_line = new_first_line.split(delimiter)
    time_col_new = new_first_line.index(time_column)
    right_padding = delimiter * len(first_line_2)
    left_padding = str()
    for num in range(len(first_line_1.split(delimiter))):
        if num == time_col_new:
            left_padding += "{}" + delimiter
        else:
            left_padding += delimiter
    for line in file_1:
        out_file.write(line.strip() + right_padding + "\n")
    for line in file_2:
        line = line.strip().split(delimiter)
        timestamp = line[time_col_2]
        line.remove(timestamp)
        out_file.write(left_padding.format(timestamp) + delimiter.join(line) + "\n")
    file_1.close()
    file_2.close()
    out_file.close()
    return out_file_name


input_files = list()
output_files = list()

print("combining files ...")
for file in inputs:
    if len(input_files) < 2:
        input_files.append(file)
    else:
        output_files.append(merge_files(*input_files))
        input_files.clear()
        input_files.append(output_files[-1])
        input_files.append(file)
merge_files(*input_files, output_file)

for file in output_files:
    os.remove("{}/{}".format(data_cache_path, file))

with open("{}/{}".format(data_cache_path, output_file), "r") as file:
    line_count = 0
    for x in range(5):
        print(file.readline().strip())
        line_count += 1
    for line in file:
        line_count += 1
print("files combined: {}".format(len(inputs)))
print("total number of lines written: {}".format(line_count))

try:
    resp = requests.post(
        job_callback_url,
        json={dep_instance: {"output_csv": output_file}}
    )
    if not resp.ok:
        raise RuntimeError(resp.status_code)
except Exception as ex:
    try:
        os.remove("{}/{}".format(data_cache_path, output_file))
    except Exception:
        pass
    raise ex
