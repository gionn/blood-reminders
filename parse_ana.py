with open('0002LU065_ana.txt', 'r') as f:
    for line in f:
        # print(line)
        # print(line[:5])  # poco interessante
        print(f'cognome={line[5:41]}')
        print(f'nome={line[41:77]}')
        # print(f'sesso={line[77:78]}')  # 1 uomo 2 donna
        # print(f'nascita={line[78:86]}')
        # print(f'cf={line[86:102]}')
        # print(line[102:104])  # quasi tutti 0A
        # print(f'CRegionale={line[104:113]}')
        # print(line[113:119])  # codice comune residenza?
        # print(f'indirizzo={line[119:182]}')
        # print(line[182:184])  # sempre I1
        #print(f'centro raccolta={line[184:187]}')
        print(f'id donatore pre={line[187:197]}')
        print(f'{line[197:207]}')
        #print(f'data sospensione={line[207:215]}')
        #print(f'data riattivazione={line[215:223]}')
        print(f'{line[223:]}')
        print('------')
        if 'BACCELLI' in line[5:41]:
            break
