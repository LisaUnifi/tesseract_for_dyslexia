import os
from os import write
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBox, LTTextLine

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
        
for f in font:
    document = open('C:/Users/lisac/Desktop/MarinaiProgetto/font/font_'+ font[f] +'.pdf','rb')
    rsrcmgr = PDFResourceManager()
    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    path = 'C:/Users/lisac/Desktop/MarinaiProgetto/gt/'
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
        line.pop()

        for l in range(len(line)): 
            with open(pdir + '/font_'+ font[f] + str(count) + '_seg' + str(l) + '.gt.txt', 'w', encoding = 'utf8') as file:
                line[l].replace('\n','')
                file.write(line[l])
        count = count + 1

    

    
