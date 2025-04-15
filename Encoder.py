text = "My name is Saikat"
encoding_list = []
for s in text:
    ascii = ord(s)
    encoding_list.append(ascii)
print(encoding_list)


def decoding(encodedlist):
    decodedText = ""
    for c in encodedlist:
        decodedText += chr(c)
    return decodedText;

print(decoding(encoding_list))