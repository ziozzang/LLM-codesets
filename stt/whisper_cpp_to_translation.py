# This code is PoC of Local LLM(translation) + STT (transcription)
#  - by Jioh L. Jung (ziozzang@gmail.com)
# Transcript: using whisper.cpp (stream) & whisper.ggml model (whisper large v3)
# Translation: Openchat 3.5 or synatra-translation (mistral 7B based) with quantized and runned by llama.cpp
#
import subprocess

import requests
import json


prompt_to_en = """<|im_start|>system
주어진 문장을 영어로 번역해라.<|im_end|>
<|im_start|>user
{sentence}<|im_end|>
<|im_start|>assistant"""
prompt_to_kr = """<|im_start|>system
주어진 문장을 한국어로 번역해라.<|im_end|>
<|im_start|>user
{sentence}<|im_end|>
<|im_start|>assistant"""
eos = ["<|im_end|>",]

def _translate(templates, conts):
  data = {'prompt': templates.replace('{sentence}', conts.strip()), "stop":eos }
  endpoint = "http://127.0.0.1:8080/completion"
  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  res = requests.post(endpoint, data=json.dumps(data), headers=headers)
  ret = res.json()['content'].replace('<0x0A>','\n').lstrip()
  return ret

# Execute Whisper.cpp stream process
proc = subprocess.Popen(
      "./stream -tdrz" +
      " --keep 800 --step 6000 --length 12000" +
      " -l ko -kc " +
      " -m ./models/ggml-large.bin",
      shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )

# Do Loop to Capture
started = False
stream_text = ''
splitter = ''
while True:
  # Acquire Transcribed streamed texts
  line = proc.stdout.readline()
  if not line:
    break
  # Detect Program Loading
  if started == False:
    if b'[Start speaking]' == line.strip():
      started = True
    continue
  # Detect EoS
  s = line.split(b'\x1b[2K\r')
  #print('>B')
  l = ''
  for i in s:
    l = i.decode('utf-8').strip()
    #print("LEN:%d /'%s'" % (len(l), l))
  #print('>E')
  stream_text += l
  stream_text += ' '# Append Lastest Line
  if stream_text.rfind('.') > 0:
    text, stream_text = stream_text.rsplit('.',1)
    text += '.'
    text = text.strip()
    print('>>', text)
    tr = _translate(prompt_to_en, text)
    print('<<', tr)
  #print(s[-1].decode('utf-8'))
