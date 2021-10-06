import subprocess, os
import shutil
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBox, LTTextLine
from pdf2image import convert_from_path
from PIL import Image
import json
import cv2 #OpenCV

id = 'lisa'
hdd = '/media/' + id + '/Lisa/MP/'
local = '/home/' + id + '/Desktop/MP/'


def getText():
    with open(hdd + 'text/evaluate-spazi.txt', 'r') as fin, open(hdd + 'text/evaluate.txt', 'w+') as fout:
        lines = fin.readlines()
        cleaned = [' '.join(line.strip().split()) for line in lines]
        joined = ' '.join(cleaned)
        fout.write(joined)

    with open(hdd + 'text/evaluate.txt', 'r') as file:
        line = file.readline()

    with open(hdd + 'text/evaluate.txt', 'w') as file:
        line = line.replace('  ', ' ')
        line = line.replace('   ', ' ')
        line = line.replace('    ', ' ')
        line = line.replace('     ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('--', '-')
        line = line.replace('-­‐', '-') 
        line = line.replace(" ʹ ", " ")
        file.write(line)

def generatePDF(font):
    with open(hdd + 'text/evaluate.txt','r', encoding = 'utf8') as txt:
        data = txt.read()
    
    pdir = os.path.join(hdd, 'evaluate')
    if not os.path.isdir(pdir):
        os.mkdir(pdir)

    #generate fontcreator.tex 
    with open(hdd + 'evaluate/font/fontcreator.tex','w', encoding = 'utf8') as file:
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

    #generate .tex with selected font
    for f in font:    
        with open(hdd + 'evaluate/font/fontcreator.tex','r') as myfile:
            text = myfile.read()
            text_new = text.replace('var', f)

        with open(hdd + 'evaluate/font/font_'+ font[f] +'.tex', 'w') as output:
            output.write(text_new)

    #generete .pdf with selected font
    for f in font:  
        x = subprocess.call('buf_size=2000000000 lualatex --output-directory=' + hdd + 'evaluate/font ' + hdd + 'evaluate/font/font_'+ font[f] +'.tex', shell =True)
        if x != 0:
            print('Exit-code not 0, check result!')

def binarizationAndSegmentation(font):
    pdir = os.path.join(hdd + 'evaluate', 'image')
    if not os.path.isdir(pdir):
        os.mkdir(pdir)
    path = hdd + 'evaluate/image/'
    for f in font:
        directory = font[f]
        pdir = os.path.join(path, directory)
        if not os.path.isdir(pdir):
            os.mkdir(pdir)
        image = convert_from_path(hdd + 'evaluate/font/font_'+ font[f] +'.pdf') 
        count = 1
        for i in image:
            i.save(pdir + '/font_'+ font[f] + str(count) + '.tif')
            count = count + 1

    for dir in os.listdir(path):  
        pdir = os.path.join(path, dir)
        for d in os.listdir(pdir):

            if font[f] == 'Sylexiad' or font[f] == 'TimesNewRoman':
                x = subprocess.call('kraken -i ' + pdir + '/' + d + ' ' + pdir + '/bw_'+ d + ' binarize --threshold=0.90', shell = True)
            else:
                x = subprocess.call('kraken -i ' + pdir + '/' + d + ' ' + pdir + '/bw_'+ d + ' binarize --threshold=0.75', shell = True)
            if x != 0:
                print('Exit-code not 0, check result!')
                
            name = d.replace('.tif', '')
            y = subprocess.call('kraken -i ' + pdir + '/bw_'+ d + ' ' + pdir + '/lines_'+ name +'.json segment', shell = True)
            if y != 0:
                print('Exit-code not 0, check result!')

    pdir = os.path.join(hdd + 'evaluate', 'data')
    if not os.path.isdir(pdir):
        os.mkdir(pdir)
    path2 = hdd + 'evaluate/data/'
    for f in font:
        directory = font[f]
        pdir = os.path.join(path2, directory)
        if not os.path.isdir(pdir):
            os.mkdir(pdir)

    for dir in os.listdir(path):  
        pdir = os.path.join(path, dir)
        for d in os.listdir(pdir):
            if d.endswith('.json'):
                with open(pdir + '/' + d, 'r') as file: 
                    data = json.load(file)
                    boxes = data['boxes'] 

                    n = d.replace('lines_', '').replace('.json', '.tif')
                    im = Image.open(pdir + '/' + n) 
                    count = 0
                    p = 3
                    f = n.replace('.tif', '')
                    for i in boxes:
                        box = (i[0]-p,i[1]-p,i[2]+p,i[3]+p) 
                        region = im.crop(box) 
                        name = path2 + '/' + dir + '/'+ f + '_seg'+ str(count) + '.tif'
                        region.save(name)
                        count = count + 1
        
def generateGT(font):  
    pdir = os.path.join(hdd + 'evaluate', 'gt')
    if not os.path.isdir(pdir):
        os.mkdir(pdir)      
    for f in font:
        document = open(hdd + 'evaluate/font/font_'+ font[f] +'.pdf','rb')
        rsrcmgr = PDFResourceManager()
        # Set parameters for analysis.
        laparams = LAParams(char_margin=3.5)
        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        path = hdd + 'evaluate/gt/'
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

def blurred(font, parameter):
    pdir = os.path.join(hdd + 'evaluate', 'blurring')
    if not os.path.isdir(pdir):
        os.mkdir(pdir)
    pdata = hdd + 'evaluate/data/'
    pblur = hdd + 'evaluate/blurring/'
    for f in font:
        directory = font[f]
        pdir = os.path.join(pdata, directory)
        pout = os.path.join(pblur, directory)
        if not os.path.isdir(pout):
            os.mkdir(pout)
        pout = os.path.join(pout, str(parameter))
        if not os.path.isdir(pout):
            os.mkdir(pout)
        for el in os.listdir(pdir):
            image = cv2.imread(pdir + '/' + el)
            blurred = cv2.GaussianBlur(image, (parameter, parameter), 0)
            name = el.replace('.tif', '')
            cv2.imwrite(pout + '/' + name + '.tif', blurred)
        
def superimposition(font, parameter):  
    pdir = os.path.join(hdd + 'evaluate', 'superimposition')
    if not os.path.isdir(pdir):
        os.mkdir(pdir)
    pdata = hdd + 'evaluate/data/'
    psup = hdd + 'evaluate/superimposition/'
    for f in font:
        directory = font[f]
        pdir = os.path.join(pdata, directory)
        pout = os.path.join(psup, directory)
        if not os.path.isdir(pout):
            os.mkdir(pout)
        pout = os.path.join(pout, str(parameter))
        if not os.path.isdir(pout):
            os.mkdir(pout)
        for el in os.listdir(pdir):
            foreground = os.path.join(pout, 'fg')
            if not os.path.isdir(foreground):
                os.mkdir(foreground)
            background = os.path.join(pout, 'bg')
            if not os.path.isdir(background):
                os.mkdir(background)
            name = el.replace('.tif', '')
            #make foreground image: 
            #first - convert it in RGBA
            fg = Image.open(pdir + '/' + name + '.tif')
            fg = fg.convert('RGBA') #red-green-blue-alpha
            #second - make white pixels transparent
            data = fg.getdata()
            newData = []
            for i in data:
                if i[0] == 255 and i[1] == 255 and i[2] == 255:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(i)
            fg.putdata(newData)
            #third - save new data 
            fg.save(foreground + '/' + name + '.fg.tif', 'TIFF')

            fg = Image.open(foreground + '/' + name + '.fg.tif')
            bg = Image.open(pdir + '/' + name + '.tif')

            left = parameter
            top = parameter
            w, h = bg.size
            newW = w + left
            newH = h + top

            newBg = Image.new(bg.mode, (newW, newH), (255, 255, 255))
            newBg.paste(bg, (left, top))
            newBg.save(background + '/' + name + '.bg.tif', 'TIFF')

            newBg = Image.open(background + '/' + name + '.bg.tif')
            newBg.paste(fg, (0,0), mask = fg) #starting at coordinate = (0,0)
            
            newBg.save(pout + '/' + name + '.tif', 'TIFF')
        try: 
            shutil.rmtree(background)
            shutil.rmtree(foreground)
        except OSError as e:
            print('Errore!')

def add_border(img, width):
        new = Image.new('RGB', (img.width + 2*width, img.height),(255,255,255))
        new.paste(img, (width, 0))
        return new

def makeSlant(img, sl):
        s = img.transform(img.size, Image.AFFINE, (1, sl, 0,0,1,0))
        return s

def slant(font, parameter):
    pdir = os.path.join(hdd + 'evaluate', 'slant')
    if not os.path.isdir(pdir):
        os.mkdir(pdir)
    pdata = hdd + 'evaluate/data/'
    pslant = hdd + 'evaluate/slant'
    for f in font:
        directory = font[f]
        pdir = os.path.join(pdata, directory)
        pout = os.path.join(pslant, directory)
        if not os.path.isdir(pout):
            os.mkdir(pout)
        pout = os.path.join(pout, str(parameter))
        if not os.path.isdir(pout):
            os.mkdir(pout)
        for el in os.listdir(pdir):
            img = Image.open(pdir + '/' + el)
            img = add_border(img, 30)
            img = makeSlant(img, parameter)
            img = img.save(pout + '/' + el)

def renameGT(font):
    for f in font: 
        path = os.path.join(hdd + 'evaluate/gt', font[f])
        for file in os.listdir(path):
            old = os.path.join(path, file)
            new = old.replace('.gt.txt', '.txt')
            os.rename(old, new)



if __name__ == "__main__":
    #font usati 
    font = {
        'Open Dyslexic' : 'OpenDyslexic', 
        'Sylexiad Sans Medium' : 'Sylexiad',
        'Lexie Readable' : 'LexieReadable',
        'Arial' : 'Arial',
        'Tahoma' : 'Tahoma',
        'Verdana' : 'Verdana',
        'Comic Sans Ms' : 'ComicSansMs',
        'Baskervville' : 'Baskervville',
        'Times New Roman' : 'TimesNewRoman',
        'Georgia' : 'Georgia'
        }

    getText()
    generatePDF(font)
    binarizationAndSegmentation(font)
    generateGT(font)

    blurCoef = [3, 5, 7]
    for b in blurCoef:
        blurred(font, b)

    superimpCoef = [1, 2, 3]
    for s in superimpCoef:
        superimposition(font, s)

    slantCoef = [0.1, 0.25, 0.4]
    for s in slantCoef:    
        slant(font, s)

    renameGT(font)