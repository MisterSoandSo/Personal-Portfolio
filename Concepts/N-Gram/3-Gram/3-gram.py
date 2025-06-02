#=====================================================================
# Set pickle for checkpoint saving 
#=====================================================================

import pickle

def save_checkpoint(tble, last_k, filename="checkpoint.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump({'tble': tble, 'last_k': last_k}, f)

def load_checkpoint(filename="checkpoint.pkl"):
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            return data['tble'], data['last_k']
    except FileNotFoundError:
        return None, 0  # start fresh

#=====================================================================
# Read in tokenized dataset and setup Tokenizer
#=====================================================================
from tokenizers import Tokenizer
# Load the trained BPE tokenizer
tokenizer = Tokenizer.from_file("custom_tokenizer.json")   


# Tokenized dataset filename 
filename = 'tokenized_dataset.txt'  

def read_integers_from_file(filename):
    '''
    Returns list array of integer from dataset file
    '''
    integer_array = []
    with open(filename, 'r') as file:
        for line in file:
            integer_array.extend([int(x) for x in line.split()])
    return integer_array

def generate_ngrams(words_list, n):
    ngrams_list = []
 
    for num in range(0, len(words_list)-n+1):
        ngram = ' '.join(words_list[num:num + n])
        ngrams_list.append(ngram)
 
    return ngrams_list

Dataset_array = read_integers_from_file(filename)
Dataset_len=len(Dataset_array)
print("DataSet Array Size: ",Dataset_len)

amtUniqueID = len(set(Dataset_array))
print(f"Amount of unique integer id: {amtUniqueID}")


#Returns the max token value from the dataset
max_dataValue= max(Dataset_array)
print("max_datavalue :", max_dataValue)

#=====================================================================
# Build Transition Table with dict = {int : [list of int]}
# The C++ equivalent of 'std::map<int, int> table;'
# Table is populated with '.' or `18` as the stop value
#=====================================================================
subsize=35
STOP_TOKEN = 18

# Unique token IDs used in dataset text
used_tokens = set(Dataset_array)

tble, start_k = load_checkpoint()

if tble is None:
    # Create a sparse transition table
    tble = {token_id: [STOP_TOKEN] * subsize for token_id in used_tokens}


def processToken(k):
    if k + 2 >= Dataset_len:
        return

    token1 = Dataset_array[k]
    token2 = Dataset_array[k + 1]
    key = (token1, token2)

    if key in tble and tble[key][0] != STOP_TOKEN:
        return  # Already processed

    vari = [None] * subsize
    freq = [0] * subsize
    j = 0

    for i in range(k + 2, Dataset_len - 1):
        if Dataset_array[i - 2] == token1 and Dataset_array[i - 1] == token2:
            next_tok = Dataset_array[i]
            found = False
            for n in range(j):
                if vari[n] == next_tok:
                    freq[n] += 1
                    found = True
                    break
            if not found and j < subsize:
                vari[j] = next_tok
                freq[j] = 1
                j += 1

    # Sort by frequency (descending)
    for m in range(j - 1):
        for n in range(j - 1 - m):
            if freq[n] < freq[n + 1]:
                freq[n], freq[n + 1] = freq[n + 1], freq[n]
                vari[n], vari[n + 1] = vari[n + 1], vari[n]

    tble[key] = [STOP_TOKEN] * subsize
    for n in range(min(j, subsize)):
        tble[key][n] = vari[n] if vari[n] is not None else STOP_TOKEN


for k in range(start_k, Dataset_len-2):
    processToken(k)
    if k % 10000 == 0:
        print(f"Saving checkpoint: {k} / {Dataset_len}")
        save_checkpoint(tble, k,filename=f"checkpoint/checkpoint_{k}.pkl")
save_checkpoint(tble, Dataset_len-3,filename="checkpoint.pkl")


while True:
    word = input("Enter your words:\n").strip()
    if not word:
        continue

    ids = tokenizer.encode(word).ids
    if len(ids) < 2:
        print("Please enter at least two tokens.")
        continue

    token1, token2 = ids[-2], ids[-1]
    out = [tokenizer.id_to_token(token1), tokenizer.id_to_token(token2)]
    generated_ids = set([token1, token2])
    loopcnt = 0

    while True:
        key = (token1, token2)
        if key not in tble or tble[key][0] == STOP_TOKEN:
            break

        next_token = STOP_TOKEN
        for tok in tble[key]:
            if tok != STOP_TOKEN and tok not in generated_ids:
                next_token = tok
                break  # pick first unused option

        if next_token == STOP_TOKEN:
            break  # no valid next token

        out.append(tokenizer.id_to_token(next_token))
        generated_ids.add(next_token)

        # shift window
        token1, token2 = token2, next_token
        loopcnt += 1
        if loopcnt > 100:
            break

    print(" ".join(out))
    print("\nEnd of Inquire\n")