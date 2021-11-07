import subprocess, os
from datetime import datetime

id = 'lisa'
hdd = '/media/' + id + '/Lisa/MP/'
local = '/home/' + id + '/Desktop/MP/'

def moveData(font):
    for f in font:
        name = font[f] + '-ground-truth'
        ptr = hdd + 'training'
        pdata = hdd + 'data/' + f + '/*'
        pgt = hdd + 'gt/' + f + '/*'
        path = os.path.join(ptr, name)
        if not os.path.isdir(path):
            os.mkdir(path)
        x = subprocess.call('mv ' + pdata + ' ' + path, shell = True)
        if x != 0:
            print('Exit-code not 0, check result!')
        x = subprocess.call('mv ' + pgt + ' ' + path, shell = True)
        if x != 0:
            print('Exit-code not 0, check result!')


def tesseract(font, file):
    x = subprocess.call('make training MODEL_NAME=' + font + ' DATA_DIR=/media/lisa/Lisa/MP/training PSM=7 MAX_ITERATIONS=100000', shell = True, stdout = file)
    if x != 0:
        print('Exit-code not 0, check result!')
                

def clean(font):
    for f in font:
        x = subprocess.call('make clean MODEL_NAME=' + font[f] + ' DATA_DIR=/media/lisa/Lisa/MP/training ', shell = True)
        if x != 0:
            print('Exit-code not 0, check result!')


if __name__ == "__main__":
    #font usati 
    font = {
        'OpenDyslexic' : 'opd', 
        'Sylexiad' : 'slx',
        'LexieReadable' : 'lxr',
        'Arial' : 'ari',
        'Tahoma' : 'tha',
        'Verdana' : 'vrd',
        'ComicSansMs' : 'csm',
        'Baskervville' : 'bsk',
        'TimesNewRoman' : 'tnr',
        'Georgia' : 'grg'
        }
    
    #moveData(font)

    with open('/media/' + id + '/Lisa/MP/training/trainingTime.txt', 'w+') as time:
        now = datetime.now()
        print(now.strftime("%d/%m/%Y, %H:%M:%S"))

    for f in font:
        with open('/media/' + id + '/Lisa/MP/training/' + font[f] + '.txt', 'w') as file:
            tesseract(font[f], file)

    with open('/media/' + id + '/Lisa/MP/training/trainingTime.txt', 'a') as time:
        now = datetime.now()
        print(now.strftime("%d/%m/%Y, %H:%M:%S"))

    #clean(font)

    