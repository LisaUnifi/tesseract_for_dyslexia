import subprocess, os

font = {
    'Open Dyslexic' : 'OpenDyslexic', 
    'Nisaba' : 'Nisaba',
    'Lexie Readable' : 'LexieReadable',
    'Arial' : 'Arial'
    }

with open('C:/Users/lisac/Desktop/MarinaiProgetto/font/fontcreator.tex','w') as file:
    file.write('\\documentclass{report}\n')
    file.write('\\usepackage[english]{babel}\n')
    file.write('\\usepackage{blindtext}\n')
    file.write('\\usepackage{lipsum}\n')
    file.write('\\usepackage{fontspec}\n')
    file.write('\\setmainfont{var}\n')
    file.write('\\renewcommand{\\baselinestretch}{1.8}\n')
    file.write('\n')
    file.write('\\begin{document}\n')
    file.write('a A b B c C d D e E f F g G h H i I j J k K l L m M n N o O p P q Q r R s S t T u U v V w W x X y Y z Z\n')
    file.write('\n')
    file.write('\\medskip\n')
    file.write('1 2 3 4 5 6 7 8 9 0\n')
    file.write('\n')
    file.write('\\medskip\n')
    file.write('\\`{a} \`{e} \`{i} \`{o} \`{u}\n')
    file.write("\\'{a} \\'{e} \\'{i} \\'{o} \\'{u}\n")
    file.write('\n')
    file.write('\\medskip\n')
    file.write('\\blindtext\n')
    file.write('\\end{document}\n')

for f in font:    
    with open('C:/Users/lisac/Desktop/MarinaiProgetto/font/fontcreator.tex','r') as myfile:
        text = myfile.read()
        text_new = text.replace('var', f)

    with open('C:/Users/lisac/Desktop/MarinaiProgetto/font/font_'+ font[f] +'.tex', 'w') as output:
        output.write(text_new)

for f in font:  
    x = subprocess.call('lualatex --output-directory=C:/Users/lisac/Desktop/MarinaiProgetto/font/ C:/Users/lisac/Desktop/MarinaiProgetto/font/font_'+ font[f] +'.tex')
    if x != 0:
        print('Exit-code not 0, check result!')