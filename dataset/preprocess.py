#!python3
# Code by Jioh L. Jung

####################################################
# Text Pre-processor routine.

import json
import pyarrow.parquet as pq
import csv
#from pyarrow import csv

####################################################
# Basic Row Processing Function (Template)
def process_row(row):
  #res = {}
  #return res
  return row

####################################################
# Data Loader
def load_parquet(pq_name, func_process_row=process_row):
  dl = []
  df = pq.read_pandas(pq_name)
  ln = df.num_rows
  keys = df.column_names
  for i in range(ln):
    row = {}
    for j in keys:
      row[j] = df[j][i].as_py()
    dl.append(func_process_row(row))
  return dl

def load_csv(csv_name, func_process_row=process_row):
  data = []
  dl = []
  with open(csv_name, 'r') as csv_file:
    df = csv.DictReader(csv_file)
    data = list(df)
  for row in data:
    dl.append(func_process_row(row))
  return dl

def load_json(json_name, func_process_row=process_row):
  dl = []
  df = json.load(open(json_name))
  for i in df:
    dl.append(func_process_row(i))
  return dl

def load_jsonl(jsonl_name, func_process_row=process_row):
  dl = []
  for i in open(jsonl_name).readlines()
    row = json.loads(i)
    dl.append(func_process_row(row))
  return dl


####################################################
# Dumper
def save_json(json_file, py_types):
  with open(json_file, 'a+', encoding="UTF-8") as fp:
    json.dump(py_types, fp, ensure_ascii=False, indent=2)

####################################################
# Usages

## Specific Function to Row Parser
def process_idioms(row):
  res = {}
  res['question'] = row['question'].replace('\t','\n')
  res['answer'] = '%d' % (row['label'] + 1)
  return res
lst = load_parquet('korean_idioms.parquet', process_idioms)
save_json('korean_idioms.json', lst)

