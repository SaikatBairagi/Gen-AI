import tiktoken

text = "hello how are you?"


"""
Choose the encoding used by the model you want to work with
For example, "cl100k_base" is used in GPT-4 and GPT-3.5-turbo
"""

encoding = tiktoken.get_encoding("cl100k_base")
tokenList = encoding.encode(text)
print(tokenList)

decoding = encoding.decode(tokenList)
print("Decoding string:", decoding)