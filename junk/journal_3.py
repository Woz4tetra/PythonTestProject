import string
import enchant

len_alphabet = 26
dict_en = enchant.Dict("en_US")

def de_caesar(sentence, shift):
    decrypted = ""
    for character in sentence:
        if character.lower() in string.ascii_lowercase:
            alpha_index = ord(character.lower()) - ord('a')
            alpha_index = (alpha_index - shift) % len_alphabet
            decrypted += chr(alpha_index + ord('a'))
        else:
            decrypted += character
    return decrypted

def de_atbash(sentence):
    decrypted = ""
    for character in sentence:
        if character.lower() in string.ascii_lowercase:
            alpha_index = ord(character.lower()) - ord('a')
            alpha_index = -alpha_index + len_alphabet - 1
            decrypted += chr(alpha_index + ord('a'))
        else:
            decrypted += character
    return decrypted

def de_a1z26(numbers):
    decrypted = ""
    for number in numbers:
        decrypted += chr((number - 1) % len_alphabet + ord('a'))
    return decrypted

def check_sentence(sentence):
    threshold = 0.4
    likelihood = 0
    if " " in sentence:
        split = sentence.split(" ")
        word_num = len(split)
        for word in split:
            if len(word) > 0:
                if not all([char.isalpha() for char in str(word)]):
                    word_num -= 1
                if dict_en.check(word):
                    likelihood += 1
    else:
        word_num = 1
    
    if likelihood / word_num >= threshold:
        return sentence
    else:
        return None

def decrypt(sentence):
    sentence = sentence.replace("\n", " ")
    sentence = sentence.replace("\t", " ")
    
    for shift in range(len_alphabet):
        decrypted = check_sentence(de_caesar(sentence, shift))
        if decrypted is not None:
            return decrypted, shift
    decrypted = check_sentence(de_atbash(sentence))
    if decrypted is not None:
        return decrypted


print(decrypt(
"""L zrq pb Lqilqlwb qlh khuh!
    """))

# print(de_a1z26([0, 1, 2, 3]))