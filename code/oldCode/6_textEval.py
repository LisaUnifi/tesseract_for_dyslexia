import subprocess, os

font = {
    'Open Dyslexic' : 'OpenDyslexic', 
    'Nisaba' : 'Nisaba',
    'Lexie Readable' : 'LexieReadable',
    'Arial' : 'Arial',
    'Tahoma' : 'Tahoma',
    'Verdana' : 'Verdana',
    'Comic Sans Ms' : 'ComicSansMs',
    'BaskervilleF' : 'BaskervilleF',
    'Times New Roman' : 'TimesNewRoman',
    'Georgia' : 'Georgia'
    }

with open('/home/lisa/Desktop/MP/evaluation/font/fontcreator.tex','w', encoding = 'utf8') as file:
    file.write('\\documentclass{report}\n')
    file.write('\\usepackage[english]{babel}\n')
    file.write('\\usepackage{fontspec}\n')
    file.write('\\usepackage[margin=0.5in]{geometry}\n')
    file.write('\\setmainfont{var}\n')
    file.write('\\renewcommand{\\baselinestretch}{1.8}\n')
    file.write('\n')
    file.write('\\begin{document}\n')
    file.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nibh nisl condimentum id venenatis a condimentum vitae sapien. Elementum nisi quis eleifend quam adipiscing vitae proin sagittis. Id aliquet lectus proin nibh. Sapien faucibus et molestie ac feugiat. Et sollicitudin ac orci phasellus egestas tellus rutrum tellus. Eget gravida cum sociis natoque penatibus. Sed viverra ipsum nunc aliquet bibendum. Sed viverra ipsum nunc aliquet bibendum enim. Semper eget duis at tellus at urna. Eu ultrices vitae auctor eu augue. A scelerisque purus semper eget. Consectetur libero id faucibus nisl tincidunt eget. Eget sit amet tellus cras adipiscing. Leo a diam sollicitudin tempor id. Et ultrices neque ornare aenean euismod elementum nisi quis eleifend. Felis eget nunc lobortis mattis.')
    file.write('\n')
    file.write('\\end{document}\n')

for f in font:    
    with open('/home/lisa/Desktop/MP/evaluation/font/fontcreator.tex','r') as myfile:
        text = myfile.read()
        text_new = text.replace('var', f)

    with open('/home/lisa/Desktop/MP/evaluation/font/font_'+ font[f] +'.tex', 'w') as output:
        output.write(text_new)

for f in font:  
    x = subprocess.call('lualatex --output-directory=/home/lisa/Desktop/MP/evaluation/font /home/lisa/Desktop/MP/evaluation/font/font_'+ font[f] +'.tex')
    if x != 0:
        print('Exit-code not 0, check result!')