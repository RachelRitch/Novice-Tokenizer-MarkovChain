
symbols = ("! ( ) - [ ] { } ; : \' \" — , < > . / ? @ # $ % ^ & * _ ~")
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

def special_token_insert(token_list: list, special_token_list: list):
    return

def rm_duplicates(training_list: list):
    for i in range(len(training_list)):
        if training_list[i] != '':
            words = training_list[i]
            for j in range(len(training_list)):
                if words == list[j] and j != i:
                    training_list[j] = ''
    training_list = [t for t in training_list if t != '']
    return training_list

def encoder(list: list, dict: dict):
    encoded_list = []
    for word in list[:]:
        if word in dict:
            encoded_list.append(dict[word])
        else:
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

    
    text = text[:500]
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

    token_list = rm_duplicates(token_list)
    

    for i in range(len(token_list)):
        token_number.append(i)
    for i, token in enumerate(special_token):
        encoder_tokenizer[special_token[i]] = special_token.index(token)
        decoder_tokenizer[special_token.index(token)] = special_token[i]

    for i in range(len(token_list)):
        encoder_tokenizer[token_list[i]] = token_number[i]
    print(encoder_tokenizer)

    decoder_tokenizer = dict((v, k) for k, v in encoder_tokenizer.items())
    input_splitter = text_splice(input_splitter)
    print(input_splitter)
    input_splitter = collapse_nested_list(input_splitter)
    print(input_splitter)
    print(" ".join(input_splitter))


    input_token = encoder(input_splitter, encoder_tokenizer)

    print(" ".join(str(t) for t in input_token))
    print("UNK: ", special_token.index("<unk>"))

    input_token = decoder(input_token, decoder_tokenizer)
    print(" ".join(input_token))


if __name__ == '__main__':
    main()