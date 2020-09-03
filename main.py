import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

baun = open('data/baun.txt', 'r').read().upper().split(', ')
chettri = open('data/chettri.txt', 'r').read().upper().split('\n')
newar = open('data/newar.txt', 'r').read().upper().split('\n')


def all_available():
    path = 'data/person'
    files = []
    for root, dirname, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(root, filename)
            files.append(filename[:-4])
    return files
    
    
def begin(filename):
    fr = open(filename, 'r')
    full_data = fr.read()
    fr.close()
    line_Sorted = full_data.split('\n')
    name = []
    caste = []
    description = []
    
    for i in range(len(line_Sorted)):
        if line_Sorted[i] == 'Friends' or line_Sorted[i] == 'Add Friend':
            name.append(line_Sorted[i+1].split(' ')[0])
            try:
                caste.append(line_Sorted[i+1].split(' ')[1])
            except IndexError:
                caste.append('NULL')
            description.append(line_Sorted[i])
    
    
    data = pd.DataFrame(data={'Name':name, 'Caste':caste})
    for i in data.columns:
        data[i] = data[i].str.upper()
    return data

    
    
def extract_caste(data):
    for i in range(len(data)):
        temp = ''
        for j in data:
            if j.isalpha() or j == '>':
                temp = temp + str(j)
        return temp.split('>')
    
    
def assign_group(caste, indexx, group):
    if caste[0] in baun or caste[1] in baun:
            return "BAHUN"
    elif caste[0] in chettri or caste[1] in chettri:
        return "KHASCHHETRI"
    elif caste[0] in newar or caste[1] in newar:
        return "NEWAR"
    indexx = np.array(indexx)
    group = np.array(group)
    for caste_ in indexx:
        if caste[0] == caste_:
            return group[np.where(indexx == caste_)][0]
    return 'Not in database'



# print(str(os.path.abspath(os.getcwdb()))[2:-1] + '\\saved\\' + person)
available = ('\n').join(all_available()).upper()
print(f"""Available names:
{available}""")
while 1:
    person = ''.join([i for i in input("Enter the name of person you wanna get chart of: ") if not (i==' ') and i.isalpha()])
    if person.upper() in available:
        break
    else:
        print("Please Enter a Valid Name" + '\n')

print("Loading........PLEASE WAIT")
data = begin('data/person/' + person + '.txt')


fr = open('data/caste.txt', 'r')
caste_full_data = fr.read()
line_sorted_ = caste_full_data.split('\n')
caste_ = []
group = []

caste_ = [extract_caste(line_sorted_[i])[0].upper() for i in range(len(line_sorted_)-1)]
group = [extract_caste(line_sorted_[i])[1] for i in range(len(line_sorted_)-1)]


caste_data = pd.DataFrame(data={'Group':group, 'Caste':caste_})
for i in caste_data.columns:
    caste_data[i] = caste_data[i].str.upper()

data['Group'] = data[['Caste', 'Name']].apply(assign_group, axis=1, args=(caste_data['Caste'], caste_data['Group']))

sns.countplot(y='Group', data=data)
plt.title("Friends of "+ person.upper() +" BASED ON CASTE")
try:
    os.mkdir('Saved Item')
except FileExistsError:
    pass
try:
    os.mkdir('Saved Item/'+person)
except FileExistsError:
    pass
plt.savefig('Saved Item/'+person+'/'+person+'.png', orientation='landscape', papertype='a4', pad_inches=0.1, bbox_inches='tight')
print("\n"+  "Figure saved as:")
print(os.path.join(str(os.getcwd())+'Saved Item/'+person+'/'+person+'.png'))
plt.show()
