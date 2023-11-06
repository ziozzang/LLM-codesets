# Generate Tokenizer (Tokenizer Rebuild)

if model has only 3 json files for tokenizer, first generate vocab.json

- special_tokens_map.json
- tokenizer.json
- tokenizer_config.json


```
cat > extract_vocab.py<<EOF
import json, sys
tokenizer = json.load(sys.stdin)
json.dump(tokenizer['model']['vocab'], sys.stdout)
EOF

# Run Script to extract
python3 extract_vocab.py < tokenizer.json > vocab.json

```

After that, Run llama.cpp convert.py script

```
python3 convert.py \
  ~/models/some \
  --vocab-only \
  --outfile ~/models/some/tokenizer.model \
  --vocabtype bpe
```

After that, tokenizer.model will be generated.
