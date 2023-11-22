# How-to
- This guide is how to expand tokenizer.

# Use of spm

```
from transformers import AutoTokenizer, PreTrainedTokenizerFast
import sentencepiece as spm


# Load Tokenizer from Foundation Model.
tk = AutoTokenizer.from_pretrained('/test_foundation/model')

# Load Sentance Pieces Tokenizer
sp = spm.SentencePieceProcessor(model_file='./spm.model')

# Extract Tokenizer Dict.
k = tk.get_vocab().keys()

# Compare/Filtering pre-existances
nt = []
for i in range(sp.vocab_size()):
  if sp.id_to_piece(i) in k:
    #print(i, '-> EXIST')
    pass
  else:
    print(i,':', sp.id_to_piece(i))
    nt.append(sp.id_to_piece(i))

# Append filtered tokens to Foundation Tokenizer
tk.add_tokens(nt)

# Save Tokenizer
tk.save_pretrained('./some_output_dirs')

# Resize Models
#model.resize_token_embeddings(len(tokenizer))
```
