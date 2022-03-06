import json


def getGrammar(language):
    with open("Grammar\\" + language + ".json", "r") as f:
        return json.load(f)


def internationalize(file_name, language):
    language_grammar = getGrammar(language)
    # A flattened, reversed version of the language grammar which is useful during tokenizing
    reversed_l_grammar = {}
    for group_key in language_grammar:
        reversed_l_grammar[group_key] = {}
        for token_key in language_grammar[group_key]:
            try:
                reversed_l_grammar[language_grammar[group_key]
                                   [token_key]] = token_key
            except:
                reversed_l_grammar[language_grammar[group_key]
                                   [token_key][0]] = token_key
    with open(file_name, "r") as f:
        # Reads the file and then splits it by the character return token
        file = f.read().split(language_grammar["symbols"]["CR"])
    international_g_file = []
    for line in file:
        lexed_line = []
        continue_ = 0
        for pos, char in enumerate(line):
            if continue_ != 0:
                continue_ -= 1
                continue
            # Symbols
            if char in list(language_grammar["symbols"].values()) + language_grammar["symbols"]["QUOTE"]:
                if char not in language_grammar["symbols"]["QUOTE"]:
                    lexed_line.append(reversed_l_grammar[char])
                else:
                    # Strings
                    string = ""
                    for _, i in enumerate(line[pos+1:]):
                        if i == '"':
                            end_quote_pos = _
                            break
                        string += i
                    lexed_line.append(
                        ("STR", language_grammar["data_types"]["STR"].replace('$', string)))
                    continue_ = end_quote_pos + 1

            else:
                if char in '1234567890':
                    # Numbers
                    number = ""
                    for _, i in enumerate(line[pos+1:]):
                        if i not in '.1234567890':
                            number_end_pos = _
                            break
                        number += i
                    lexed_line.append(
                        ("NUM", language_grammar["data_types"]["NUM"].replace('$', number)))
                    continue_ = number_end_pos + 1
        international_g_file.append(lexed_line)

    return international_g_file


def internationalToLanguage(file_name, language, international_g_file):
    ending_language_g = getGrammar(language)
    for line in international_g_file:
        for token in line:
            


def lex(file_name, starting_language, final_language):
    internationalized = internationalize(file_name, starting_language)
    international_g_file = internationalized[0]
    grammar = [1]
    converted_file_string = internationalToLanguage(file_name, final_language, international_g_file)

    return international_g_file


if __name__ == "__main__":
    import os
    import sys
    os.chdir(os.path.dirname(sys.argv[0]))
    supported_languages = ["python", "javascript"]

    print(lex("example_files\\example.py", "python", "javascript"))
