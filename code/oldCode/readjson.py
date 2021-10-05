from PIL import Image
import json

f = open('C:/Users/lisac/Desktop/MarinaiProgetto/data/lines.json',) #apre il file json

data = json.load(f)

boxes = data['boxes'] #prendi i valori che hanno come chiave boxes 

print(boxes)

im = Image.open('C:/Users/lisac/Desktop/MarinaiProgetto/data/prova.tif') #apre immagine relativa al json utilizzato
count = 0
p = 3 #aggiunto un padding di 3 per evitare il crop dei caratteri di bordo
for i in boxes:
    box = (i[0]-p,i[1]-p,i[2]+p,i[3]+p) #creazione del box con le 4 coordinate 
    print(box)
    region = im.crop(box) #estrae la regione dell'immagine prova.tif della dimensione delle coordinate date
    name = "C:/Users/lisac/Desktop/MarinaiProgetto/data/prova"+"_seg"+str(count)+".tif"
    region.save(name)
    count = count+1