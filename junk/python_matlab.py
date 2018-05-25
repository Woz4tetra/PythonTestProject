import numpy as np
import matplotlib.pyplot as plt

import xlrd

def cell_to_float(cell):
    return cell.value

cell_to_float = np.vectorize(cell_to_float)

def to_numpy_array(workbook):
    sheet = workbook.sheet_by_index(0)
    data = np.zeros((sheet.nrows, sheet.ncols))
    for col in xrange(sheet.ncols):
        column = cell_to_float(np.array(sheet.col_slice(col)))
        data[:, col] = column
    return data

data1_workbook = xlrd.open_workbook('Data1.xlsx')

data1 = to_numpy_array(data1_workbook)

#strain1_workbook = xlrd.open_workbook('Stress Strain1.xls')
#strain2_workbook = xlrd.open_workbook('Stress Strain2.xls')
#strain3_workbook = xlrd.open_workbook('Stress Strain3.xls')

#def f(t):
#    return np.exp(-t) * np.cos(2*np.pi*t)
#
#t1 = np.arange(0.0, 5.0, 0.1)
#t2 = np.arange(0.0, 5.0, 0.02)

plt.figure(1)
plt.subplot(211)
plt.plot(data1[:, 0], data1[:, 1], 'bo')
#plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

#plt.subplot(212)
#plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
plt.show()
