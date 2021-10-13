import csv
import os
import jellyfish
import numpy as np
import matplotlib.pyplot as plt 

id = 'lorenzo'
#hdd = '/media/' + id + '/Lisa/MP/'
hdd = '/home/' + id + '/Desktop/MP/'

def distance(str1, str2):
    d = jellyfish.levenshtein_distance(str1, str2)
    return d

def comparison(font):
    pdist = os.path.join(hdd + 'evaluate/results', font)
    pgt = os.path.join(hdd + 'evaluate/gt', font)

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

def noDistEval(font):
    path = os.path.join(hdd + 'evaluate/results', font)
    pdist = os.path.join(hdd + 'evaluate/normal', font)
    pgt = os.path.join(hdd + 'evaluate/gt', font)
    
    sum = 0
    count = 0
    for file in os.listdir(pdist):
        if file.endswith('.txt'):
            gtpath = pgt + '/' + file
            fpath = pdist + '/' + file

            with open(gtpath, 'r') as gt, open(fpath, 'r') as f:
                str1 = gt.read()
                str2 = f.read()
                value = distance(str1, str2)
                sum = sum + value
                count = count + 1
            
            with open(path + '/data.csv', mode = 'a') as cfile:
                fileWriter = csv.writer(cfile, delimiter = ',')
                fileWriter.writerow([str(font), 'normal', 0, str(file), value])
                cfile.close()
    
    mean = sum/count
    with open(path + '/mean.csv', mode = 'a') as cfile:
        fileWriter = csv.writer(cfile, delimiter = ',')
        fileWriter.writerow([str(font), 'normal', 0, count, mean])
        cfile.close()

def meanOfMeans(category, distortion):
    path = hdd + 'evaluate/results'
    with open(path + '/meanOfMeans.csv', mode = 'w+') as cfile:
        fileWriter = csv.writer(cfile, delimiter = ',')
        fileWriter.writerow(['CATEGORY', 'DISTORTION', 'PARAMETER', 'VALUE'])
        cfile.close()
    
    for d in distortion:
        for p in distortion[d]:
            for c in category:
                mean = 0 
                count = len(category[c])
                for f in category[c]:
                    pathc = os.path.join(path,f)
                    with open(pathc + '/mean.csv', mode='r') as file:
                        fileReader = csv.reader(file, delimiter=',')
                        for row in fileReader:
                            if row[1] == d and row[2]==str(p):
                                mean = mean + float(row[4])
                mean = mean / count
                with open(path + '/meanOfMeans.csv', mode = 'a') as cfile:
                    fileWriter = csv.writer(cfile, delimiter = ',')
                    fileWriter.writerow([c, d, p, mean])
                    cfile.close()
    
    for c in category:
        mean = 0 
        count = len(category[c])
        for f in category[c]:
            pathc = os.path.join(path,f)
            with open(pathc + '/mean.csv', mode='r') as file:
                fileReader = csv.reader(file, delimiter=',')
                for row in fileReader:
                    if row[1] == 'normal' and row[2]=='0':
                        mean = mean + float(row[4])
        mean = mean / count
        with open(path + '/meanOfMeans.csv', mode = 'a') as cfile:
            fileWriter = csv.writer(cfile, delimiter = ',')
            fileWriter.writerow([c, 'normal', '0', mean])
            cfile.close()




def barAverages(font, distortion):
    path = hdd + 'evaluate/results'
    data = {}
    listfont = []
    listpar = []
    for f in font:
        listfont.append(font[f])
        dir = os.path.join(path, font[f])
        with open(dir + '/mean.csv', mode = 'r') as cfile:
            fileReader = csv.reader(cfile, delimiter = ',')
            for row in fileReader:
                if row[1] == distortion or row[1] == 'normal':
                    mean = round(float(row[4]), 2)
                    data[(font[f], row[2])] = mean
                    if row[2] not in listpar:
                        listpar.append(row[2])

    value = []
    listpar.sort()
    listfont.sort()
    for p in listpar:
        tmp = []
        for f in listfont:
            tmp.append(data[(f, p)])
        value.append(tmp)
    
    X = np.arange(len(listfont))
    plt.figure(figsize =(12, 12))
    plt.grid(axis = 'y')
    coef = 1/(len(listpar) + 1)
    for i in range(len(listpar)):
        plt.bar(X + (coef*i), value[i], width = coef)
    plt.ylabel('Mean')
    plt.xticks(X, listfont)
    plt.xticks(rotation='vertical')
    plt.legend(labels = listpar)
    plt.title(distortion)

    plt.savefig(path + '/' + distortion + '.png')


def barCategory(category, distortion):
    path = hdd + 'evaluate/results'
    data = {}
    listcat = []
    listpar = []
    for c in category:
        listcat.append(c)
        with open(path + '/meanOfMeans.csv', mode = 'r') as cfile:
            fileReader = csv.reader(cfile, delimiter = ',')
            for row in fileReader:
                if (row[1] == distortion or row[1] == 'normal') and row[0] == c:
                    mean = round(float(row[3]), 2)
                    data[(c, row[2])] = mean
                    if row[2] not in listpar:
                        listpar.append(row[2])

    value = []
    listpar.sort()
    listcat.sort()
    for p in listpar:
        tmp = []
        for f in listcat:
            tmp.append(data[(f, p)])
        value.append(tmp)
    
    X = np.arange(len(listcat))
    plt.figure(figsize =(12, 12))
    plt.grid(axis = 'y')
    coef = 1/(len(listpar) + 1)
    for i in range(len(listpar)):
        plt.bar(X + (coef*i), value[i], width = coef)
    plt.ylabel('Mean')
    plt.xticks(X, listcat)
    plt.xticks(rotation='vertical')
    plt.legend(labels = listpar)
    plt.title(distortion)

    plt.savefig(path + '/' + distortion + '.png')
                                

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

    category = {
        'Dyslexic' : ['LexieReadable', 'OpenDyslexic', 'Sylexiad'],
        'SansSerif' :  ['Arial', 'ComicSansMs', 'Tahoma', 'Verdana'],
        'Serif' : ['Baskervville', 'Georgia', 'TimesNewRoman']
        }
    
    distortion = {
        'blurring' : [3, 5, 7],
        'slant' : [0.1, 0.25, 0.4],
        'superimposition' : [1, 2, 3]
    }

    
    
    for f in font:
        comparison(font[f])
        noDistEval(font[f])
    

    '''
    distortion = ['blurring', 'slant', 'superimposition']
    
    for d in distortion:
        barAverages(font, d)
    '''

    meanOfMeans(category, distortion)

    for d in distortion:
        barCategory(category, d)