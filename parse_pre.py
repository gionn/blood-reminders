with open('0002LU065_pre.txt', 'r') as f:
    for line in f:
        # print(line)
        # print(line[:5])  # punto prelievo I1006 o I1029
        print(f'id donatore={line[5:15]}')
        # print(f'{line[15:16]}')  # tipologia omologa o controllo
        print(f'data donazione={line[16:24]}')
        # print(f'{line[24:27]}')  # dove donazione? 006 lucca
        print(f'tipo donazione={line[27:29]}')  # 00 niente 01 sangue 02 plasma
        print(f'ml donati={line[29:32]}')  # ml donazione
        print('------')
