import time

symbols = ["!", "(", ")", "-", "[", "]", "{", "}", ";", ":", "\'", "\"", "—", ",", "<", ">", ".", "/", "?", "@", "#", "$", "%", "^", "&", "*", "_", "~"]
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
special_token = ["<unk>", "<spc>"]

def text_splice(text: list):
    text_list = [] 
    for t in text:
        word = ''
        nested_text_list = []
        for letter in t:
            if letter.lower() in symbols:
                if word != '':
                    nested_text_list.append(word)                      
                nested_text_list.append(letter)
                word = ''
            elif letter.lower() in alphabet and word != '-':
                word += letter
        if word != '':
            nested_text_list.append(word)
        text_list.append(nested_text_list)
    return text_list

def adds_encoder_spacer(nested_list: list):
    special_index = special_token.index("<spc>")
    for list in nested_list:
        j = 0
        for i in range(len(list[:])):
            if i < len(list) and i > 0:
                list.insert(i + j, special_token[special_index])
                j += 1         
    return nested_list

def decoder_rm_spacer(output_text: str):
    special_index = special_token.index("<spc>")
    special_str = special_token[special_index]
    while special_str in output_text:
        output_text = output_text.replace(f' {special_str} ', '')
    return output_text

def special_token_insert(token_list: list, special_token_list: list):
    return

def encoder(list: list, dict: dict):
    encoded_list = []
    for word in list[:]:
        if word in dict:
            encoded_list.append(dict[word])
        elif word not in special_token or word in special_token[0]:
            encoded_list.append(dict[special_token[0]])
    return encoded_list

def decoder(list: list, dict: dict):
    decoded_list = []
    for i in list[:]:
        if i in dict:
            decoded_list.append(dict[i])
        else:
            decoded_list.append(dict[special_token.index('<unk>')])
    return decoded_list

def heat_map(token_list: list):
    return

def collapse_nested_list(nested: list):
    flat = []
    for chunk in nested:
        for token in chunk:
            flat.append(token)
    return flat

def main():
    with open("aliceinwonderland.txt", encoding="utf-8") as f:
        text = f.read()

    
    #text = text[:500]
    input_text = input("Enter your text: ")

    text_list = text.split()
    input_splitter = input_text.split()

    token_list = []
    token_number = []
    input_token = []

    encoder_tokenizer = {}
    decoder_tokenizer = {}
   

    token_list = text_splice(text_list)
    token_list = collapse_nested_list(token_list)
    for i in range(len(special_token)):
        token_list.insert(i, special_token[i])
    start = time.perf_counter()
    token_list = list(dict.fromkeys(token_list))
    
    print("took", time.perf_counter() - start, "seconds")
    for i in range(len(token_list)):
        token_number.append(i)
    for i, token in enumerate(special_token):
        encoder_tokenizer[special_token[i]] = special_token.index(token)
        decoder_tokenizer[special_token.index(token)] = special_token[i]

    for i in range(len(token_list)):
        encoder_tokenizer[token_list[i]] = token_number[i]
    #print(encoder_tokenizer)

    decoder_tokenizer = dict((v, k) for k, v in encoder_tokenizer.items())

    input_splitter = text_splice(input_splitter)
    input_splitter = adds_encoder_spacer(input_splitter)
    print(input_splitter)
    input_splitter = collapse_nested_list(input_splitter)
    print(input_splitter)
    print(" ".join(input_splitter))


    input_token = encoder(input_splitter, encoder_tokenizer)

    print(" ".join(str(t) for t in input_token))
    print("UNK: ", special_token.index("<unk>"))

    input_token = decoder(input_token, decoder_tokenizer)
    input_token = decoder_rm_spacer(' '.join(input_token))
    print(input_token)


if __name__ == '__main__':
    main()