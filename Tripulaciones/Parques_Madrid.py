import pandas as pd
import os

root = os.path.dirname(os.path.abspath(__file__))

# Leemos el texto por líneas
with open(root + os.sep + 'Madrid_Parques.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extraemos los nombres de los centros
centros = []
for i, line in enumerate(lines):
    if line.startswith('MADRID'):
        for j in range(i+2, len(lines)):
            if lines[j] == '\n':
                break
            else:
                centros.append(lines[j])

# Limpiamos y juntamos
centros = [centro.replace('\n', '').replace('  ', ' ') for centro in centros]
centros = [centros[0] + ' ' + centros[1] + ' ' + centros[2],
            centros[3] + ' ' + centros[4][:-1] + centros[5],
            centros[6] + ' ' + centros[7],
            centros[8] + ' ' + centros[9][:-2] + centros[10]]
centros = [(centro.split('.')[0], centro.split('.')[1][1:]) for centro in centros]

# Obtenemos datos de cada centro
data1 = {'Ubicacion':[], 'Centro':[], 'Direccion':[], 'Telefono':[], 'email':[],'Informacion':[]}

clean_lines = [line.replace('\n', '') for line in lines]

for centro in centros:

    data1['Ubicacion'].append(centro[0])
    data1['Centro'].append(centro[1])

    for i, line in enumerate(clean_lines):
        if line == centro[1]:
            for j in range(i+2, len(clean_lines)):
                if clean_lines[j] == 'Información General':
                    texto = ''
                    for k in range(j+2, len(clean_lines)):
                        if clean_lines[k] == '':
                            data1['Informacion'].append(texto)
                            break
                        else:
                            texto += ' ' + clean_lines[k]
                elif j == i + 2:
                    data1['Direccion'].append(clean_lines[j] + ' ' + clean_lines[j+1])
                    data1['Telefono'].append(''.join(clean_lines[j+2].replace('Teléfono / Fax: ', '').split(' ')))
                    data1['email'].append(clean_lines[j+3].replace('Email: ', ''))

centros_df = pd.DataFrame(data1, index=range(len(data1['Centro'])))
centros_df.to_csv(root + os.sep + 'centros_madrid.csv')


# Obtenemos accesibilidad de cada centro
data2 = {'Centro':[]}

excepciones = ['Espacios y Actividades en la Naturaleza Accesibles para Todas las Personas',
            'Centros de interpretación / Casas del Parque y Aulas de la Naturaleza',
            'Ubicación',
            'Características destacables',
            'Zona de Picnic',
            '(cid:2) Dispone de paneles informati-',
            'trastado: Sí',
            'rrelieve: No',
            '(cid:2) Iconos homologados: no hay',
            'Señalización',
            'Sendero Guiado / Autoguiado',
            'pavimento',
            'Arboreto']

found_cols = [] # Columnas que se añaden por centro
cuenta = 0

for centro in centros:

    data2['Centro'].append(centro[1])
    print(len(data2['Centro']))
    #cuenta = 0

    for i, line in enumerate(clean_lines):
        if line == centro[1]:
            for j in range(i+2, len(clean_lines)):
                if clean_lines[j] == 'Accesibilidad Física':
                    for k in range(j+1, len(clean_lines)-1):
                        # Fin de los datos del centro
                        if clean_lines[k] == 'Accesibilidad Visual':
                            #print(found_cols)
                            # Se mira el número de columnas y se añade 'NP' en las que existen pero no se han encontrado
                            for key in data2.keys():
                                if key not in found_cols and key != 'Centro':
                                    data2[key].append('NP')
                            found_cols = [] # Se reinicia la cuenta
                            break
                        # Columna encontrada
                        elif clean_lines[k] != '' and clean_lines[k+1] == '' and clean_lines[k-1] == '' and clean_lines[k].replace(' ', '').isalpha() and '' not in clean_lines[k] and clean_lines[k] not in excepciones:
                            found_cols.append(clean_lines[k])
                            texto = ''
                            # Concatenando líneas de la respectiva columna
                            for n in range(k+2, len(clean_lines)):
                                #print(len(data2['Centro']))
                                if clean_lines[n] == '':
                                    if clean_lines[k] in data2.keys():
                                        data2[clean_lines[k]].append(texto.replace('- ', ''))
                                        break
                                    elif len(data2['Centro']) == 1:
                                        data2[clean_lines[k]] = [texto.replace('- ', '')]
                                        break
                                    else:
                                        data2[clean_lines[k]] = ['NP' for v in range(len(data2['Centro']))].append(texto.replace('- ', ''))
                                        break
                                # Nos saltamos los cambios de página.
                                elif clean_lines[n] == '' and len(clean_lines[n+1]) == 1 or len(clean_lines[n]) == 1 and len(clean_lines[n+1]) == 1:
                                    continue
                                else:
                                    texto += clean_lines[n] + ' '
                elif clean_lines[j] == 'Accesibilidad Visual':
                    break


access_df = pd.DataFrame(data2, index=range(len(data2['Centro'])))
print(access_df)
access_df.to_csv(root + os.sep + 'parques_madrid.csv')
