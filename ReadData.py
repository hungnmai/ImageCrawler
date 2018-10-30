import pandas as pd

df = pd.read_excel('./inputs.xlsx')
names = df.values.tolist()


def getListNames():
    listNames = []
    for name in names:
        listNames.append(name[0])
    return listNames

