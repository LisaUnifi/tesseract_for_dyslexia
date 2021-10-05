import subprocess, os

id = 'lisa'

#OCR read distortion with different parameters for each font and create a .txt file
def evaluate(font, distortion):
    pin = os.path.join('/home/'+id+'/Desktop/MP/distorsion', distortion)
    path = '/home/'+id+'/Desktop/MP/distorsion/results'
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

def evaluateNoDist(font):
    pin = '/home/'+id+'/Desktop/MP/distorsion/data'
    path = '/home/'+id+'/Desktop/MP/distorsion/normal'
    for f in font:
        pdir = os.path.join(pin, f)
        pout = os.path.join(path, f)
        if not os.path.isdir(pout):
            os.mkdir(pout)
        for file in os.listdir(pdir):
            if file.endswith('.tif'):
                name = file.replace('.tif', '')
                x = subprocess.call('tesseract ' + pdir + '/' + file + ' ' + pout + '/' + name + ' -l ' + font[f], shell = True)
                if x != 0:
                    print('Exit-code not 0, check result!')

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
    

if __name__ == "__main__":
    #font usati 
    font = {
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

    distortion = ['blurring', 'slant', 'superimposition']
    
    for d in distortion:
        evaluate(font, d)

    path = '/home/'+id+'/Desktop/MP/distorsion/results'
    for fold in os.listdir(path):
        path2 = os.path.join(path,fold)
        for fold2 in os.listdir(path2):
            path3 = os.path.join(path2,fold2)
            for fold3 in os.listdir(path3):
                path4 = os.path.join(path3,fold3)
                eraseLS(path4)

    evaluateNoDist(font)

    path = '/home/'+id+'/Desktop/MP/distorsion/normal'
    for fold in os.listdir(path):
        path2 = os.path.join(path,fold)
        eraseLS(path2)