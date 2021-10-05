from pdf2image import convert_from_path
import subprocess, os
from PIL import Image
import json

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

path = '/home/lisa/Desktop/MP/evaluation/image/'

#convertire pdf in tif
for f in font:
    directory = font[f]
    pdir = os.path.join(path, directory)
    os.mkdir(pdir)
    image = convert_from_path('/home/lisa/Desktop/MP/evaluation/font/font_'+ font[f] +'.pdf') 
    count = 1
    for i in image:
        i.save(pdir + '/font_'+ font[f] + str(count) + '.tif')
        count = count + 1

#binarizzazione e segmentazione
for dir in os.listdir(path):  
    pdir = os.path.join(path, dir)
    for d in os.listdir(pdir):

        x = subprocess.call('kraken -i ' + pdir + '/' + d + ' ' + pdir + '/bw_'+ d + ' binarize')
        if x != 0:
            print('Exit-code not 0, check result!')
            
        name = d.replace('.tif', '')
        y = subprocess.call('kraken -i ' + pdir + '/bw_'+ d + ' ' + pdir + '/lines_'+ name +'.json segment')
        if y != 0:
            print('Exit-code not 0, check result!')

#divisione in segmenti
path2 = '/home/lisa/Desktop/MP/evaluation/data/'
for f in font:
    directory = font[f]
    pdir = os.path.join(path2, directory)
    os.mkdir(pdir)

for dir in os.listdir(path):  
    pdir = os.path.join(path, dir)
    for d in os.listdir(pdir):
        if d.endswith('.json'):
            with open(pdir + '/' + d, 'r') as file: #apre il file json
                data = json.load(file)
                boxes = data['boxes'] #prendi i valori che hanno come chiave boxes

                n = d.replace('lines_', '').replace('.json', '.tif')
                im = Image.open(pdir + '/' + n) #apre immagine relativa al json utilizzato
                count = 0
                p = 3 #aggiunto un padding di 3 per evitare il crop dei caratteri di bordo
                f = n.replace('.tif', '')
                for i in boxes:
                    box = (i[0]-p,i[1]-p,i[2]+p,i[3]+p) #creazione del box con le 4 coordinate 
                    region = im.crop(box) #estrae la regione dell'immagine prova.tif della dimensione delle coordinate date
                    name = path2 + '/' + dir + '/'+ f + '_seg'+ str(count) + '.tif'
                    region.save(name)
                    count = count + 1
        