
with open("aliceinwonderland.txt", encoding="utf-8") as f:
    text = f.read()

text = text[:500]
#text = "the abc is a test."
input_text = input("Enter your text: ")
special = ("! ( ) - [ ] { } ; : \' \" — \u2014 \u201c \u2019 , < > . / ? @ # $ % ^ & * _ ~")
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

word = text.split()
input_splitter = input_text.split()

token_dict = []
token_number = []
encoder_tokenizer = {}
decoder_tokenizer = {}
input_token = []

def text_splice(text: list):
    text_list = [] 
    
    for t in text:
        w = ''
        text_nest = []
        for letter in t:
            if letter.lower() in special:
                if w != '':
                    text_nest.append(w)                      
                text_nest.append(letter)
                w = ''
            elif letter.lower() in alphabet and w != '-':
                w += letter
        if w != '':
            text_nest.append(w)
        text_list.append(text_nest)
    return text_list

def rm_duplicates(list: list):
    temp_list = list
    for i in range(len(temp_list)):
        if temp_list[i] != '':
            word = temp_list[i]
            for j in range(len(temp_list)):
                if word == list[j] and j != i:
                    temp_list[j] = ''
    temp_list = [t for t in temp_list if t != '']
    return temp_list

def encoder(list: list, dict: dict, length: int):
    encoded_list = []
    for word in list[:]:
        if word in dict:
            encoded_list.append(dict[word])
        else:
            encoded_list.append(length)
    return encoded_list

def decoder(list: list, dict: dict, length: int):
    decoded_list = []
    for i in list[:]:
        if i in dict:
            decoded_list.append(dict[i])
        elif i == length:
            decoded_list.append('<unk>')
    return decoded_list

def heat_map(list: list):
    None

def collapsed_nested_list(nested: list):
    flat = []
    for chunk in nested:
        for token in chunk:
            flat.append(token)
    return flat

token_dict = text_splice(word)
#print("Token Dict: ", token_dict)
token_dict = collapsed_nested_list(token_dict)
token_dict = rm_duplicates(token_dict)
#print("Token Dict after remove_dup: ", token_dict)

for i in range(len(token_dict)):
    token_number.append(i)

#print(token_number)
#print(len(token_number))
encoder_tokenizer["<unk>"] = (len(token_dict))
decoder_tokenizer[(len(token_dict))] = "<unk>"

for i in range(len(token_dict)):
    encoder_tokenizer[token_dict[i]] = token_number[i]
    

decoder_tokenizer = dict((v, k) for k, v in encoder_tokenizer.items())
input_splitter = text_splice(input_splitter)
print(input_splitter)
input_splitter = collapsed_nested_list(input_splitter)
print(input_splitter)
print(" ".join(input_splitter))


input_token = encoder(input_splitter, encoder_tokenizer, len(token_dict))
    
print(" ".join(str(t) for t in input_token))
print("UNK: ", len(token_dict))

input_token = decoder(input_token, decoder_tokenizer, len(token_dict))
print(" ".join(input_token))


#print("encoder: ", encoder_tokenizer)
#print("decoder: ", decoder_tokenizer)