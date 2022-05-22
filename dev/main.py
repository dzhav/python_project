#!/usr/bin/env python3
import sys
import argparse


def parse(parsiring):
    subparsering = parsiring.add_subparsers(dest="action")
    encode = subparsering.add_parser("encode")
    encode.add_argument("--cipher")
    encode.add_argument("--key")
    encode.add_argument("--input_file")
    encode.add_argument("--output_file")
    decode = subparsering.add_parser("decode")
    decode.add_argument("--cipher")
    decode.add_argument("--key")
    decode.add_argument("--input_file")
    decode.add_argument("--output_file")
    decode_without_key = subparsering.add_parser("decode-without-key")
    decode_without_key.add_argument("--input_file")
    decode_without_key.add_argument("--output_file")
    return parsiring.parse_args()


alphabet_length = 26


def shift(c, dd):
    if not (ord('A') <= ord(c) <= ord('Z') or ord('a') <= ord(c) <= ord('z')):
        return c
    base_ind = ord('a') if c == c.lower() else ord('A')
    return chr((ord(c) - base_ind + dd) % alphabet_length + base_ind)


def shift_text(text, k, type):
    result_text = ['a' for _ in range(len(text))]
    for i in range(len(text)):
        if type == "shift_text_caesar":
            result_text[i] = shift(text[i], k)
        if type == "decode_vigenere":
            result_text[i] = shift(text[i], alphabet_length - ((ord(k[i % len(k)]) - ord('a')) % alphabet_length))
        if type == "shift_text_vigenere":
            result_text[i] = shift(text[i], ((ord(k[i % len(k)]) - ord('a')) % alphabet_length))
    return ''.join(result_text)


def count_frequencies(text):
    frequencies = [0 for i in range(alphabet_length)]
    total = 0
    for c in text.lower():
        if not ord('a') <= ord(c) <= ord('z'):
            continue
        total += 1
        frequencies[ord(c) - ord('a')] += 1
    for i in range(alphabet_length):
        frequencies[i] /= total
    return frequencies


def MAE(frequencies1, frequencies2):
    error = 0
    for i in range(alphabet_length):
        error += abs(frequencies1[i] - frequencies2[i]) / alphabet_length
    return error


def decode(text, sample):
    min_error = 10000
    min_k = 30
    for k in range(alphabet_length):
        freqs = count_frequencies(shift_text(text, alphabet_length - k, "shift_text_caesar"))
        if MAE(freqs, sample) < min_error:
            min_error = MAE(freqs, sample)
            min_k = k
    return shift_text(text, alphabet_length - min_k, "shift_text_caesar")


if __name__ == '__main__':
    parsing = argparse.ArgumentParser()
    arguments = parse(parsing)
    if arguments.action == "encode":
        if arguments.cipher == "caesar":
            k = int(arguments.key)
            if len(sys.argv) == 6:
                input_txt = input()
                print(shift_text(input_txt, k, "shift_text_caesar"))
            else:
                with open(arguments.input_file) as input_1:
                    input_txt = input_1.read()
                    input_1.close()
                    with open(arguments.output_file, "w") as output_1:
                        output_1.write(shift_text(input_txt, k, "shift_text_caesar"))
                        output_1.close()
        else:
            k = arguments.key
            if len(sys.argv) == 6:
                input_txt = input()
                print(shift_text(input_txt, k, "shift_text_vigenere"))
            else:
                with open(arguments.input_file) as input_1:
                    input_txt = input_1.read()
                    input_1.close()
                    with open(arguments.output_file, "w") as output_1:
                        output_1.write(shift_text(input_txt, k, "shift_text_vigenere"))
                        output_1.close()
    if arguments.action == "decode":
        if arguments.cipher == "caesar":
            k = int(arguments.key)
            if len(sys.argv) == 6:
                input_txt = input()
                print(shift_text(input_txt, alphabet_length - k, "shift_text_caesar"))
            else:
                with open(arguments.input_file) as input_1:
                    input_txt = input_1.read()
                    input_1.close()
                    with open(arguments.output_file, "w") as output_1:
                        output_1.write(shift_text(input_txt, alphabet_length - k, "shift_text_caesar"))
                        output_1.close()
        else:
            k = arguments.key
            if len(sys.argv) == 6:
                input_txt = input()
                print(shift_text(input_txt, k, "decode_vigenere"))
            else:
                with open(arguments.input_file) as input_1:
                    input_txt = input_1.read()
                    input_1.close()
                    with open(arguments.output_file, "w") as output_1:
                        output_1.write(shift_text(input_txt, k, "decode_vigenere"))
                        output_1.close()
    if arguments.action == "decode-without-key":
        with open('War_and_Peace.txt') as f:
            sample_text = f.read()
            f.close()
            sample_freqs = count_frequencies(sample_text)
            if len(sys.argv) == 2:
                input_txt = input()
                print(decode(input_txt, sample_freqs))
            else:
                with open(arguments.input_file) as input_1:
                    input_txt = input_1.read()
                    input_1.close()
                    with open(arguments.output_file, "w") as output_1:
                        output_1.write(decode(input_txt, sample_freqs))
                        output_1.close()
