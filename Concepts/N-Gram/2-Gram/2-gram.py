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
from tokenizers.decoders import ByteLevel as ByteLevelDecoder

# Load the trained BPE tokenizer
tokenizer = Tokenizer.from_file("tokenizer_bpe/tokenizer.json")
# Tokenized dataset filename 
filename = 'tokenized_dataset1.txt'  

def read_integers_from_file(filename):
    '''
    Returns list array of integer from dataset file
    '''
    integer_array = []
    with open(filename, 'r') as file:
        for line in file:
            integer_array.extend([int(x) for x in line.split()])
    return integer_array


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

if tble == None:
    # Create a sparse transition table
    tble = {token_id: [STOP_TOKEN] * subsize for token_id in used_tokens}


def processToken(k):
    root = Dataset_array[k]

    vari = [None] * subsize
    freq = [0] * subsize
    j = 0

    for i in range(k+1, Dataset_len - 1):
        if Dataset_array[i] == root:
            next_tok = Dataset_array[i + 1]

            # Check if next_tok already exists
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
    for m in range(j-1):
        for n in range(j-1-m):
            if freq[n] < freq[n+1]:
                freq[n], freq[n+1] = freq[n+1], freq[n]
                vari[n], vari[n+1] = vari[n+1], vari[n]

    # Fill the table only if empty
    if tble[root][0] == STOP_TOKEN:
        for n in range(min(j, subsize)):
            tble[root][n] = vari[n] if vari[n] is not None else STOP_TOKEN


for k in range(start_k, Dataset_len):
    processToken(k)
    if k % 100 == 0:
        print(f"Saving checkpoint: {k} / {Dataset_len}")
        save_checkpoint(tble, k,filename=f"checkpoint_{k}.pkl")
save_checkpoint(tble, Dataset_len-1,filename="final_checkpoint.pkl")

    


while True:
    word = input("Enter your words:\n").strip()
    if not word:
        continue

    ids = tokenizer.encode(word).ids
    if not ids:
        print("Word not recognized.")
        continue

    token_id = ids[0]
    out = []

    loopcnt = 0
    while True:
        if token_id not in tble:
            print(f"Token {token_id} not in transition table.")
            break

        token_id = tble[token_id][0]
        if token_id == STOP_TOKEN:
            break

        out.append(tokenizer.id_to_token(token_id))
        loopcnt += 1
        if loopcnt > 100:
            break

    print(" ".join(out))
    print("\nEnd of Inquire\n")
