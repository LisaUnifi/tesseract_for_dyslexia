import subprocess, os 

fontName = ['ari', 'bkv', 'csm', 'grg', 'lxr', 'nsb', 'opd', 'thm', 'tnr', 'vrd']
gt = '-ground-truth'


#move .traineddata in tessdata to complete the training
path = '/home/lisa/Desktop/MP/tesstrain-main/data'
psave = 'usr/local/share/tessdata'
for el in os.listdir(path):  
    if el.endswith('.traineddata'):
        x = subprocess.call('sudo cp ' + path + '/' + el + ' ' + psave, shell =True)
        if x != 0:
            print('Exit-code not 0, check result!')


