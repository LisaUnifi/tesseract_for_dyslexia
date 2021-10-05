import random

#prendere testo da latex
text = str('Ciao sto\'s bene. Character Reversal, prova.')

text = text.replace(',', ' ,').replace('.', ' .').replace(':', ' :').replace(';', ' ;').replace('-', ' -').replace('_', ' _').replace('\'', ' \' ')
t = text.split(' ')
print(t)

txt = ''
for el in t:
    if len(el) > 1:
        tmpel = list(el)
        print(tmpel)
        for i in range(len(tmpel)-1):
            r = random.random()
            print(r)
            if r > 0.66:
                tmp = tmpel[i]
                tmpel[i] = tmpel[i+1]
                tmpel[i+1] = tmp
        el = ''.join(tmpel)
        print(el)
    txt = txt + el + ' '

print(txt)
txt = txt.replace(' ,', ',').replace(' .', '.').replace(' :', ':').replace(' ;', ';').replace(' -', '-').replace(' _', '_').replace(' \' ', '\'')
print(txt)


