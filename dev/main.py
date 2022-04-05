#!/usr/bin/env python3
import sys


def shift(c, dd):
    if not (ord('A') <= ord(c) <= ord('Z') or ord('a') <= ord(c) <= ord('z')):
        return c
    base_ind = ord('a') if c == c.lower() else ord('A')
    return chr((ord(c) - base_ind + dd) % 26 + base_ind)


def shift_text_vigenere(text, k):
    result_text = ['a' for i in range(len(text))]
    for i in range(len(text)):
        result_text[i] = shift(text[i], ((ord(k[i % len(k)]) - ord('a')) % 26))
    return ''.join(result_text)


def decode_vigenere(text, k):
    result_text = ['a' for i in range(len(text))]
    for i in range(len(text)):
        result_text[i] = shift(text[i], 26 - ((ord(k[i % len(k)]) - ord('a')) % 26))
    return ''.join(result_text)

def shift_text_caesar(text, k):
    result_text = ['a' for i in range(len(text))]
    for i in range(len(text)):
        result_text[i] = shift(text[i], k)
    return ''.join(result_text)


def count_frequencies(text):
    frequencies = [0 for i in range(26)]
    total = 0
    for c in text.lower():
        if not 97 <= ord(c) <= 122:
            continue
        total += 1
        frequencies[ord(c) - 97] += 1
    for i in range(26):
        frequencies[i] /= total
    return frequencies


def L2_MSE(frequencies1, frequencies2):
    error = 0
    for i in range(26):
        error += abs(frequencies1[i] - frequencies2[i])
    return error


def decode(text, sample):
    min_error = 10000
    min_k = 30
    for k in range(26):
        freqs = count_frequencies(shift_text_caesar(text, 26 - k))
        if L2_MSE(freqs, sample) < min_error:
            min_error = L2_MSE(freqs, sample)
            min_k = k
    return shift_text_caesar(text, 26 - min_k)


f = open('War_and_Peace.txt')
sample_text = f.read()
f.close()
sample_freqs = count_frequencies(sample_text)

if sys.argv[1] == "encode":
    if sys.argv[3] == "caesar":
        k = int(sys.argv[5])
        if len(sys.argv) == 6:
            input_txt = input()
            print(shift_text_caesar(input_txt, k))
        else:
            input_1 = open(sys.argv[7])
            input_txt = input_1.read()
            input_1.close()
            output_1 = open(sys.argv[9], "w")
            output_1.write(shift_text_caesar(input_txt, k))
            output_1.close()
    else:
        k = sys.argv[5]
        if len(sys.argv) == 6:
            input_txt = input()
            print(shift_text_vigenere(input_txt, k))
        else:
            input_1 = open(sys.argv[7])
            input_txt = input_1.read()
            input_1.close()
            output_1 = open(sys.argv[9], "w")
            output_1.write(shift_text_vigenere(input_txt, k))
            output_1.close()
if sys.argv[1] == "decode":
    if sys.argv[3] == "caesar":
        k = int(sys.argv[5])
        if len(sys.argv) == 6:
            input_txt = input()
            print(shift_text_caesar(input_txt, 26 - k))
        else:
            input_1 = open(sys.argv[7])
            input_txt = input_1.read()
            input_1.close()
            output_1 = open(sys.argv[9], "w")
            output_1.write(shift_text_caesar(input_txt, 26 - k))
            output_1.close()
    else:
        k = sys.argv[5]
        if len(sys.argv) == 6:
            input_txt = input()
            print(decode_vigenere(input_txt, k))
        else:
            input_1 = open(sys.argv[7])
            input_txt = input_1.read()
            input_1.close()
            output_1 = open(sys.argv[9], "w")
            output_1.write(decode_vigenere(input_txt, k))
            output_1.close()
if sys.argv[1] == "decode-without-key":
    if len(sys.argv) == 2:
        input_txt = input()
        print(decode(input_txt, sample_freqs))
    else:
        input_1 = open(sys.argv[3])
        input_txt = input_1.read()
        input_1.close()
        output_1 = open(sys.argv[5], "w")
        output_1.write(decode(input_txt, sample_freqs))
        output_1.close()
