
with open('C:/Users/lisac/Desktop/MarinaiProgetto/text/text-spazi.txt', 'r') as fin, open('C:/Users/lisac/Desktop/MarinaiProgetto/text/text.txt', 'w+') as fout:
    lines = fin.readlines()
    cleaned = [line.strip() for line in lines]
    joined = ' '.join(cleaned)
    fout.write(joined)