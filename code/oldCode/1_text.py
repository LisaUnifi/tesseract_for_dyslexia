import subprocess, os

font = {
    'Open Dyslexic' : 'OpenDyslexic', 
    'Nisaba' : 'Nisaba',
    'Lexie Readable' : 'LexieReadable',
    'Arial' : 'Arial',
    'Tahoma' : 'Tahoma',
    'Verdana' : 'Verdana',
    'Comic Sans Ms' : 'ComicSansMs',
    'Baskervville' : 'Baskervville',
    'Times New Roman' : 'TimesNewRoman',
    'Georgia' : 'Georgia'
    }

with open('/home/lisa/Desktop/MP/text/text.txt','r', encoding = 'utf8') as txt:
    data = txt.read()

with open('/home/lisa/Desktop/MP/font/fontcreator.tex','w', encoding = 'utf8') as file:
    file.write('\\documentclass{report}\n')
    file.write('\\usepackage[english]{babel}\n')
    file.write('\\usepackage{blindtext}\n')
    file.write('\\usepackage{lipsum}\n')
    file.write('\\usepackage{fontspec}\n')
    file.write('\\usepackage[margin=0.5in]{geometry}\n')
    file.write('\\setmainfont{var}\n')
    file.write('\\renewcommand{\\baselinestretch}{1.8}\n')
    file.write('\n')
    file.write('\\begin{document}\n')
    file.write(data)
    file.write('\\end{document}\n')

for f in font:    
    with open('/home/lisa/Desktop/MP/font/fontcreator.tex','r') as myfile:
        text = myfile.read()
        text_new = text.replace('var', f)

    with open('/home/lisa/Desktop/MP/font/font_'+ font[f] +'.tex', 'w') as output:
        output.write(text_new)

for f in font:  
    x = subprocess.call('lualatex --output-directory=/home/lisa/Desktop/MP/font/ /home/lisa/Desktop/MP/font/font_'+ font[f] +'.tex', shell = True)
    if x != 0:
        print('Exit-code not 0, check result!')
