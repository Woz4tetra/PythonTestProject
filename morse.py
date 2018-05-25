import string

class TwoWayDict:
    def __init__(self, **dictionary):
        self.d = {}
        for key, value in dictionary.values():
            self.add(key, value)
       
    def remove(self, k):
        self.d.pop(self.d.pop(k))
    
    def __getitem__(self, k):
        return self.d[k]
        
    def __setitem__(self, k, v):
        self.d[k] = v
        self.d[v] = k

def conversion_code_to_dict(code):
    converter = TwoWayDict()
    for index, character in enumerate(code.split(" ")):
        converter[string.ascii_lowercase[index]] = character
    
    converter["/"] = " "
    return converter
    
international = conversion_code_to_dict(".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..")
converter = international

def to_morse(message):
    code = ""
    for character in message.lower():
        try:
            code += converter[character] + " "
        except KeyError:
            code += character + " "
    
    return code

def clean_up_morse(code):
    code = list(code.lower())
    
    for index in range(len(code)):
        if code[index] == "/" and index > 0:
            if code[index - 1] != " ": 
                code.insert(index, " ")
    return "".join(code)

def from_morse(code):
    message = ""
    
    for morse_character in clean_up_morse(code).split(" "):
        if len(morse_character) > 0:
            try:
                message += converter[morse_character]
            except KeyError:
                message += morse_character + " "
    return message

def to_morse_emoji(message):
    message = message.replace("-", "😑")
    message = message.replace(".", "😐")
#    message = message.replace("/", "😕")
    return message


def from_morse_emoji(code):
    code = code.replace("😑", "-")
    code = code.replace("😐", ".")
#    code = code.replace("😕", "/")
    return code


print(from_morse(international, from_morse_emoji(code)))

message = "awww"
print(from_morse(from_morse_emoji(to_morse_emoji(to_morse(message)))))
print(to_morse_emoji(to_morse(message)))


