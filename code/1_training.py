import subprocess, os
from pdf2image import convert_from_path
import subprocess, os
from PIL import Image
import json
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBox, LTTextLine

id = 'lisa'

#Get a text and remove "end of line" character
def getText():
    with open('/home/'+ id +'/Desktop/MP/text/text-spazi.txt', 'r') as fin, open('/home/lisa/Desktop/MP/text/text.txt', 'w+') as fout:
        lines = fin.readlines()
        cleaned = [' '.join(line.strip().split()) for line in lines]
        joined = ' '.join(cleaned)
        fout.write(joined)

    with open('/home/'+ id +'/Desktop/MP/text/text.txt', 'r') as file:
        line = file.readline()

    with open('/home/'+ id +'/Desktop/MP/text/text.txt', 'w') as file:
        line = line.replace('  ', ' ')
        line = line.replace('   ', ' ')
        line = line.replace('    ', ' ')
        line = line.replace('     ', ' ')
        line = line.replace('  ', ' ')
        file.write(line)


def makePDF(font):
    with open('/home/'+id+'/Desktop/MP/text/text.txt','r', encoding = 'utf8') as txt:
        data = txt.read()

    #Use "fontspec" to generate file with differnt fonts
    with open('/home/'+id+'/Desktop/MP/font/fontcreator.tex','w', encoding = 'utf8') as file:
        file.write('\\documentclass{report}\n')
        file.write('\\usepackage{fontspec}\n')
        file.write('\\usepackage[margin=0.5in]{geometry}\n')
        file.write('\\setmainfont{var}\n')
        file.write('\\renewcommand{\\baselinestretch}{1.8}\n')
        file.write('\n')
        file.write('\\begin{document}\n')
        file.write('\\pagestyle{empty}\n')
        file.write(data + '\n')
        file.write('\\end{document}\n')

    for f in font:    
        with open('/home/'+id+'/Desktop/MP/font/fontcreator.tex','r') as myfile:
            text = myfile.read()
            text_new = text.replace('var', f)

        with open('/home/'+id+'/Desktop/MP/font/font_'+ font[f] +'.tex', 'w') as output:
            output.write(text_new)

    for f in font:  
        x = subprocess.call('buf_size=2000000000 lualatex --output-directory=/home/'+id+'/Desktop/MP/font/ /home/'+id+'/Desktop/MP/font/font_'+ font[f] +'.tex', shell = True)
        if x != 0:
            print('Exit-code not 0, check result!')

#Create single line text images
def kraken(font):
    path = '/home/'+id+'/Desktop/MP/image/'

    #convertire pdf in tif
    for f in font:
        directory = font[f]
        pdir = os.path.join(path, directory)
        os.mkdir(pdir)
        image = convert_from_path('/home/'+id+'/Desktop/MP/font/font_'+ font[f] +'.pdf') 
        count = 1
        for i in image:
            i.save(pdir + '/font_'+ font[f] + str(count) + '.tif')
            count = count + 1

    #binarizzazione e segmentazione
    for dir in os.listdir(path):  
        pdir = os.path.join(path, dir)
        for d in os.listdir(pdir):

            if font[f] == 'Sylexiad':
                x = subprocess.call('kraken -i ' + pdir + '/' + d + ' ' + pdir + '/bw_'+ d + ' binarize --threshold=0.90', shell = True)
            else:
                x = subprocess.call('kraken -i ' + pdir + '/' + d + ' ' + pdir + '/bw_'+ d + ' binarize --threshold=0.75', shell = True)
            if x != 0:
                print('Exit-code not 0, check result!')
                
            name = d.replace('.tif', '')
            y = subprocess.call('kraken -i ' + pdir + '/bw_'+ d + ' ' + pdir + '/lines_'+ name +'.json segment', shell = True)
            if y != 0:
                print('Exit-code not 0, check result!')

    #divisione in segmenti
    path2 = '/home/'+id+'/Desktop/MP/data/'
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

#Generate ground truth from PDFs 
def generateGT(font):
    for f in font:
        document = open('/home/'+id+'/Desktop/MP/font/font_'+ font[f] +'.pdf','rb')
        rsrcmgr = PDFResourceManager()
        # Set parameters for analysis.
        laparams = LAParams(char_margin=3.0)
        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        path = '/home/'+id+'/Desktop/MP/gt/'
        directory = font[f]
        pdir = os.path.join(path, directory)
        os.mkdir(pdir)
        
        count = 1
        for page in PDFPage.get_pages(document):
            line = []
            interpreter.process_page(page)
            # receive the LTPage object for the page.
            layout = device.get_result()
            for element in layout:
                if isinstance(element, LTTextBox):
                    for el in element:
                        if isinstance(el, LTTextLine):
                            line.append(el.get_text())

            for l in range(len(line)): 
                with open(pdir + '/font_'+ font[f] + str(count) + '_seg' + str(l) + '.gt.txt', 'w', encoding = 'utf8') as file:
                    line[l].replace('\n','')
                    file.write(line[l])
            count = count + 1
        


if __name__ == "__main__":
    #font usati 
    font = {
        'Sylexiad Sans Medium' : 'Sylexiad'
        }
    
    getText()
    makePDF(font)
    kraken(font)
    generateGT(font)