with open('referat.txt', 'r', encoding='utf-8') as referat:
    words = referat.read()
    length_words = len(words)
    word = words.split()
    length = len(word)
    sub = words.replace('.', '!')
    print(length_words, length)
with open('referat2.txt', 'w', encoding='utf-8') as referat2:
    referat2.writelines(sub)


