#!/usr/bin/env python3
import sys
import argparse


def shift(c, dd):
    if not (ord('A') <= ord(c) <= ord('Z') or ord('a') <= ord(c) <= ord('z')):
        return c
    base_ind = ord('a') if c == c.lower() else ord('A')
    return chr((ord(c) - base_ind + dd) % 26 + base_ind)


def shift_text(text, k, type):
    result_text = ['a' for i in range(len(text))]
    for i in range(len(text)):
        if type == "stc":
            result_text[i] = shift(text[i], k)
        if type == "dv":
            result_text[i] = shift(text[i], 26 - ((ord(k[i % len(k)]) - ord('a')) % 26))
        if type == "stv":
            result_text[i] = shift(text[i], ((ord(k[i % len(k)]) - ord('a')) % 26))
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


def MAE(frequencies1, frequencies2):
    error = 0
    for i in range(26):
        error += abs(frequencies1[i] - frequencies2[i]) / 26
    return error


def decode(text, sample):
    min_error = 10000
    min_k = 30
    for k in range(26):
        freqs = count_frequencies(shift_text(text, 26 - k, "stc"))
        if MAE(freqs, sample) < min_error:
            min_error = MAE(freqs, sample)
            min_k = k
    return shift_text(text, 26 - min_k, "stc")


f = open('War_and_Peace.txt')
sample_text = f.read()
f.close()
sample_freqs = count_frequencies(sample_text)


pasrsing = argparse.ArgumentParser()
pasrsing.add_argument("action", type=str, help="decode/encode/decode-without-key")
pasrsing.add_argument("--cipher", type=str, help="caesar/vigenere")
pasrsing.add_argument("--key", type=str)
pasrsing.add_argument("--input_file", type=str)
pasrsing.add_argument("--output_file", type=str)
arguments = pasrsing.parse_args()


if arguments.action == "encode":
    if arguments.cipher == "caesar":
        k = int(arguments.key)
        if len(sys.argv) == 6:
            input_txt = input()
            print(shift_text(input_txt, k, "stc"))
        else:
            input_1 = open(arguments.input_file)
            input_txt = input_1.read()
            input_1.close()
            output_1 = open(arguments.output_file, "w")
            output_1.write(shift_text(input_txt, k, "stc"))
            output_1.close()
    else:
        k = arguments.key
        if len(sys.argv) == 6:
            input_txt = input()
            print(shift_text(input_txt, k, "stv"))
        else:
            input_1 = open(arguments.input_file)
            input_txt = input_1.read()
            input_1.close()
            output_1 = open(arguments.output_file, "w")
            output_1.write(shift_text(input_txt, k, "stv"))
            output_1.close()
if arguments.action == "decode":
    if arguments.cipher == "caesar":
        k = int(arguments.key)
        if len(sys.argv) == 6:
            input_txt = input()
            print(shift_text(input_txt, 26 - k, "stc"))
        else:
            input_1 = open(arguments.input_file)
            input_txt = input_1.read()
            input_1.close()
            output_1 = open(arguments.output_file, "w")
            output_1.write(shift_text(input_txt, 26 - k, "stc"))
            output_1.close()
    else:
        k = arguments.key
        if len(sys.argv) == 6:
            input_txt = input()
            print(shift_text(input_txt, k, "dv"))
        else:
            input_1 = open(arguments.input_file)
            input_txt = input_1.read()
            input_1.close()
            output_1 = open(arguments.output_file, "w")
            output_1.write(shift_text(input_txt, k, "dv"))
            output_1.close()
if arguments.action == "decode-without-key":
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
