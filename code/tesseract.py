import subprocess, os

id = 'lisa'

def tesseract(font):
    x = subprocess.call('cd /media/' + id + '/Lisa/MP/tesstrain-main', shell = True)
    if x != 0:
        print('Exit-code not 0, check result!')
    for f in font:
        x = subprocess.call('make training MODEL_NAME=' + font[f] + 'PSM=7 MAX_ITERATION=50000', shell = True, stdout = '/media/' + id + '/Lisa/MP/tesstrain-main/data/' + font[f] + '.txt')
        if x != 0:
            print('Exit-code not 0, check result!')
                


if __name__ == "__main__":
    #font usati 
    font = {
        'Open Dyslexic' : 'opd', 
        'Sylexiad Sans Medium' : 'slx',
        'Lexie Readable' : 'lxr',
        'Arial' : 'ari',
        'Tahoma' : 'tha',
        'Verdana' : 'vrd',
        'Comic Sans Ms' : 'csm',
        'Baskervville' : 'bsk',
        'Times New Roman' : 'tnr',
        'Georgia' : 'grg'
        }
    
    tesseract(font)