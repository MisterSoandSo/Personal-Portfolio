#=====================================================================
# Read in tokenized dataset and setup Tokenizer
#=====================================================================
from tokenizers import Tokenizer
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

Dataset_array = read_integers_from_file(filename)
Dataset_len=len(Dataset_array)
print("DataSet Array Size: ",Dataset_len)

amtUniqueID = len(set(Dataset_array))
print(f"Amount of unique integer id: {amtUniqueID}")

#Returns the max token value from the dataset
max_dataValue= max(Dataset_array)
print("max_datavalue :", max_dataValue)

#=====================================================================
# Data Structures with these frequency tables
#=====================================================================

biTable = {}   # key: int     → value: {next_token: count}
triTable = {}  # key: (int,int) → value: {next_token: count}

#=====================================================================
# Set pickle for checkpoint saving 
#=====================================================================

import pickle

def save_checkpoint(biTable, triTable, k, filename="checkpoint.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump({'bi': biTable, 'tri': triTable, 'last_k': k}, f)

def load_checkpoint(filename="checkpoint.pkl"):
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            return data['bi'], data['tri'], data['last_k']
    except FileNotFoundError:
        return {}, {}, 0
    
#=====================================================================
# Preprocessing Loop Function
#=====================================================================.
def processToken(k):
    if k + 2 >= Dataset_len:
        return

    t1 = Dataset_array[k]
    t2 = Dataset_array[k + 1]
    t3 = Dataset_array[k + 2]

    # Bigram update (no redundancy guard needed since it’s from t2 to t3 only)
    if t2 not in biTable:
        biTable[t2] = {}
    biTable[t2][t3] = biTable[t2].get(t3, 0) + 1

    # Trigram update with redundancy check
    key = (t1, t2)
    # Redundancy guard only to skip reprocessing of fully completed keys
    if key in triTable and t3 in triTable[key]:
        triTable[key][t3] += 1  # accumulate
    else:
        if key not in triTable:
            triTable[key] = {}
        triTable[key][t3] = 1


biTable, triTable, start_k = load_checkpoint()

for k in range(start_k, Dataset_len - 2):
    processToken(k)
    if k % 10000 == 0:
        save_checkpoint(biTable, triTable, k)
save_checkpoint(biTable, triTable, Dataset_len - 2)


#=====================================================================
#  Text Generation with Interpolation
#=====================================================================
import random

def sample_from_probs(probs, temperature=1.0):
    if temperature <= 0:
        return max(probs, key=probs.get)

    # Apply temperature
    scaled = {k: v ** (1.0 / temperature) for k, v in probs.items()}
    total = sum(scaled.values())
    r = random.uniform(0, total)
    upto = 0
    for k, v in scaled.items():
        upto += v
        if upto >= r:
            return k

def normalize(counter):
    total = sum(counter.values())
    return {k: v / total for k, v in counter.items()} if total else {}

lambda3 = 0.7
lambda2 = 0.3
recent_keys = set()
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

    loopcnt = 0
    while loopcnt < 100:
        key3 = (token1, token2)
        p3 = normalize(triTable.get(key3, {}))
        key2 = token2
        p2 = normalize(biTable.get(key2, {}))

        # Interpolated probability
        candidates = set(p3.keys()) | set(p2.keys())
        probs = {token: lambda3 * p3.get(token, 0) + lambda2 * p2.get(token, 0) for token in candidates}

        # Filter out recently used tokens (basic repetition ban)
        for recent in recent_keys:
            if recent in probs:
                probs[recent] *= 0.1  # Penalize heavily

        if not probs:
            break

        next_token = sample_from_probs(probs, temperature=0.8)

        out.append(tokenizer.id_to_token(next_token))
        recent_keys.add(next_token)
        if len(recent_keys) > 10:  # Keep only recent N tokens
            recent_keys.pop()

        token1, token2 = token2, next_token
        loopcnt += 1

    print(" ".join(out))
    print("\nEnd of Inquire\n")
