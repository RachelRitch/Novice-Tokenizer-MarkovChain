import time
import random
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so

from pathlib import Path
from collections import Counter
from datasets import load_dataset

symbols = ["!", "(", ")", "-", "[", "]", "{", "}", ";", ":", "\'", "\"", "—", ",", "<", ">", ".", "/", "?", "@", "#", "$", "%", "^", "&", "*", "_", "~"]
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
number = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
special_token = ["<unk>", "<spc>"]

def text_splice(text):
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
            elif letter.lower() in alphabet and word != '-' or letter in number and word != '-':
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
    #ns.set_theme()
    dataset_values = {}
    counts = Counter()
    for j in range(len(token_list) - 1):
        chart = token_list[j : j + 3]
        counts[tuple(chart)] += 1
    top = counts
    #print(top)
    fig, ax = plt.subplots(figsize=(8, 4))
    for label, value in top.items():
        sample = []
        prediction = []
        for i, s in enumerate(label):
            if i == 2:
                prediction.append(s)
            else:
                sample.append(s)
        #print(type(sample), sample, type(prediction), prediction, value)
        if prediction != []:
            if (sample[0], sample[1]) not in dataset_values:
                dataset_values[sample[0], sample[1]] = {}
            dataset_values[sample[0], sample[1]][prediction[0]] = dataset_values[sample[0], sample[1]].get(prediction[0], 0) + float(value)

    
    pairs = sorted(dataset_values, key=lambda p: len(dataset_values[p]), reverse=True)[:10]
    small = {}
    for p in pairs:
        top_words = sorted(dataset_values[p].items(), key=lambda x: x[1], reverse=True)[:10]
        small[" ".join(p)] = dict(top_words)
    df = pd.DataFrame.from_dict(small, orient="index").fillna(0)
    df = df.div(df.sum(axis=1), axis=0)
    sns.heatmap(df, annot=False, xticklabels=True, fmt=".2f", cmap="viridis")
    plt.tight_layout()
    plt.show()
    
    return dataset_values


def collapse_nested_list(nested: list):
    flat = []
    for chunk in nested:
        for token in chunk:
            flat.append(token)
    return flat

def openlibrary():
    text = ''
    for path in Path('Books').glob('*.txt'):
        with open(f'Books/{path.name}' , encoding='utf-8-sig') as f:
            text += f.read()
    return text

def markov_chain(predictive_data_set: dict, input_txt: list, loops: int, temp: float):
    t = temp
    sentence_str = ''
    list_words = ['of', 'the', '']
    if input_txt[1] != '':
        list_words[0] = input_txt[len(input_txt) -2] 
        list_words[1] = input_txt[len(input_txt) -1] 
        #print(list_words[0], list_words[1])
        for _ in range(loops):
            if predictive_data_set[list_words[0], list_words[1]] != []:
                str3_data = predictive_data_set[(list_words[0], list_words[1])]
                #print(str3_data)
                str3_word = list(str3_data.keys())
                str3_weights = list(str3_data.values())
                for i in range(len(str3_data)):
                    str3_weights[i] = str3_weights[i]**(1/t)
                pick = random.choices(str3_word, weights=str3_weights)[0]
                list_words[0] = list_words[1] 
                list_words[1] = pick
                sentence_str += ''.join(f' {pick}')
        return sentence_str


def main():
    stories = load_dataset("roneneldan/TinyStories", split="train[:1%]")
    story_list = stories["text"]

    books_list = []
    text = openlibrary()
    text += ''.join(story_list)
    text += ''.join(symbols)
    
    #text = text[:10000]
    input_text = input("Enter two words: ")
    input_loops = int(input("Words: "))
    input_temp = float(input("Temperature: "))

    text_list = text.split()
    input_splitter = input_text.split()

    token_list = []
    token_number = []
    input_token = []

    encoder_tokenizer = {}
    decoder_tokenizer = {}
   

    token_list = text_splice(text_list)
    token_list = collapse_nested_list(token_list)
    predictive_data_set = heat_map(token_list)
    output_text = markov_chain(predictive_data_set, input_splitter, input_loops, input_temp)
    for i in range(len(special_token)):
        token_list.insert(i, special_token[i])
    start = time.perf_counter()
    token_list = list(dict.fromkeys(token_list))
    
    print("Removing duplicates took: ", time.perf_counter() - start, "seconds")
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
    print(input_text + ' ' + str(output_text))

if __name__ == '__main__':
    main()