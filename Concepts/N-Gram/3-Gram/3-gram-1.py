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
STOP_TOKEN = 18

# Unique token IDs used in dataset text
used_tokens = set(Dataset_array)

biTable = {}
triTable = {}


def processToken(k,tble, gram):
    if k + gram >= Dataset_len:
        return

    token1 = Dataset_array[k]  
    if gram == 2:                           #bi
        next_token = Dataset_array[k + 1]
        key = (token1)

    if gram == 3:
        token2 = Dataset_array[k + 1]       #tri
        next_token = Dataset_array[k + 2]
        key = (token1, token2)
    

    if key not in tble:
        tble[key] = {}
    
    if next_token not in tble[key]:
        tble[key][next_token] = 1
    else:
        tble[key][next_token] += 1
    


for k in range(Dataset_len):
    processToken(k,biTable,2)
    processToken(k,triTable,3)
    


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

    #Begin Weighted Interpolation of Bigram and Trigram
    '''    
    biTable = {}
    triTable = {}
    by now are both loaded each n-gram respectfully (bi/tri)
    '''

    def normalize(counter):
        total = len(counter)
        return {k: v / total for k, v in counter} if total else {}
    
    while True:
        key_tokens = (tokenizer.id_to_token(token1),tokenizer.id_to_token(token2))
        #get trigram of token2
        key3 = (token1, token2)
        c3 = sorted(triTable[key3].items(), key=lambda x: x[1], reverse=True)
        next_tokens = [(k, tokenizer.id_to_token(k), v) for k, v in c3]
        print(f"Debug Key: {key3} ({key_tokens[0]}, {key_tokens[1]}) → {next_tokens}")

        
        p3 = normalize(c3)

        #get bigram of token2
        key2 = (token2)
        c2 = sorted(biTable[key2].items(), key=lambda x: x[1], reverse=True)
        next_tokens = [(k, tokenizer.id_to_token(k), v) for k, v in c2]
        print(f"Debug Key: {key2} ({key_tokens[1]}) → {next_tokens}")

        p2 = normalize(c2)

        #apply interpolation
        lambda3 = 0.7
        lambda2 = 0.3
        penalty_weight = 0.8  # between 0.5 and 0.9 usually works well

        final_probs = {}
        for token in set(p3) | set(p2):
            final_probs[token]= lambda3 * p3.get(token,0.0) + lambda2*p2.get(token,0.0)
        next_token = max(final_probs, key=final_probs.get)

        print(next_token)
        

        out.append(tokenizer.id_to_token(next_token))
        generated_ids.add(next_token)
        

        # shift window
        token1, token2 = token2, next_token
        loopcnt += 1
        if loopcnt > 100:
            break

    print(" ".join(out))
    print("\nEnd of Inquire\n")