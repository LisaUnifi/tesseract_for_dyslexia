import subprocess, os
from os import path, write
from os import pathconf_names
import sys
import shutil
import jellyfish
import csv
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBox, LTTextLine
from pdf2image import convert_from_path
from PIL import Image
import json
import cv2

def renameGT(font):
    for f in font: 
        path = os.path.join('/home/lisa/Desktop/MP/contDist/gt', font[f])
        for file in os.listdir(path):
            old = os.path.join(path, file)
            new = old.replace('.gt.txt', '.txt')
            os.rename(old, new)

def blurred(font, parameter):
    pdata = '/home/lisa/Desktop/MP/contDist/data/'
    pblur = '/home/lisa/Desktop/MP/contDist/blurring/'
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

def evaluate(font, distortion):
    pin = os.path.join('/home/lisa/Desktop/MP/contDist', distortion)
    path = '/home/lisa/Desktop/MP/contDist/results'
    for f in font:
        pdir = os.path.join(pin, f)
        pout = os.path.join(path, f)
        if not os.path.isdir(pout):
            os.mkdir(pout)
        pout = os.path.join(pout, distortion)
        if not os.path.isdir(pout):
            os.mkdir(pout)
        for dist in os.listdir(pdir):
            pdist = os.path.join(pout, dist)
            if not os.path.isdir(pdist):
                os.mkdir(pdist)
            pfile = os.path.join(pdir, dist)
            for file in os.listdir(pfile):
                if file.endswith('.tif'):
                    name = file.replace('.tif', '')
                    x = subprocess.call('tesseract ' + pfile + '/' + file + ' ' + pdist + '/' + name + ' -l ' + font[f], shell = True)
                    if x != 0:
                        print('Exit-code not 0, check result!')
        try: 
            shutil.rmtree(pfile)
        except OSError as e:
            print('Errore!')

def eraseLS(path):
    for file in os.listdir(path):
        f = os.path.join(path,file)
        if '.txt' in f:
            eraseLastCharacter(f)

def eraseLastCharacter(filepath):
    
    with open(filepath, 'r') as file:
        data = file.read()
        data = data.replace('\n','')
        data = data.replace('\x0c','')
        
    with open(filepath,'w') as file:
        file.write(data)

def distance(str1, str2):
    d = jellyfish.levenshtein_distance(str1, str2)
    return d

def comparison(font):
    pdist = os.path.join('/home/lisa/Desktop/MP/contDist/results', font)
    pgt = os.path.join('/home/lisa/Desktop/MP/contDist/gt', font)

    with open(pdist + '/data.csv', mode = 'w') as cfile:
        fileWriter = csv.writer(cfile, delimiter = ',')
        fileWriter.writerow(['FONT', 'DISTORSION', 'PARAMETER', 'ELEMENT', 'VALUE'])
        cfile.close()
    
    with open(pdist + '/mean.csv', mode = 'w') as cfile:
        fileWriter = csv.writer(cfile, delimiter = ',')
        fileWriter.writerow(['FONT', 'DISTORSION', 'PARAMETER', 'TOTAL', 'MEAN'])
        cfile.close()

    for dist in os.listdir(pdist):
        if not dist.endswith('.csv'):        
            distpar = os.path.join(pdist, dist)
            for par in os.listdir(distpar):
                if not par.endswith('.csv'):
                    sum = 0
                    count = 0
                    distfile = os.path.join(distpar, par)
                    for file in os.listdir(distfile):
                        if file.endswith('.txt'):
                            gtpath = pgt + '/' + file
                            fpath = distfile + '/' + file

                            with open(gtpath, 'r') as gt, open(fpath, 'r') as f:
                                str1 = gt.read()
                                str2 = f.read()
                                value = distance(str1, str2)
                                sum = sum + value
                                count = count + 1
                            
                            with open(pdist + '/data.csv', mode = 'a') as cfile:
                                fileWriter = csv.writer(cfile, delimiter = ',')
                                fileWriter.writerow([str(font), str(dist), str(par), str(file), value])
                                cfile.close()
                    
                    mean = sum/count
                    with open(pdist + '/mean.csv', mode = 'a') as cfile:
                        fileWriter = csv.writer(cfile, delimiter = ',')
                        fileWriter.writerow([str(font), str(dist), str(par), count, mean])
                        cfile.close()


if __name__ == "__main__":
    #font usati 
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
    
    lang = {
        'OpenDyslexic' : 'opd', 
        'Nisaba' : 'nsb',
        'LexieReadable' : 'lxr',
        'Arial' : 'ari',
        'Tahoma' : 'thm',
        'Verdana' : 'vrd',
        'ComicSansMs' : 'csm',
        'Baskervville' : 'bkv',
        'TimesNewRoman' : 'tnr',
        'Georgia' : 'grg'
        }

    renameGT(font)

    blurCoef = [1, 3, 5, 7, 9, 11, 13, 15]
    for b in blurCoef:
        blurred(font, b)
        evaluate(lang, 'blurring')

        path = '/home/lisa/Desktop/MP/contDist/results'
        for fold in os.listdir(path):
            path2 = os.path.join(path,fold)
            if not path2.endswith('.csv'):
                for fold2 in os.listdir(path2):
                    path3 = os.path.join(path2,fold2)
                    if not path3.endswith('.csv'):
                        for fold3 in os.listdir(path3):
                            path4 = os.path.join(path3,fold3)
                            eraseLS(path4)

        for f in font:
            comparison(font[f])
