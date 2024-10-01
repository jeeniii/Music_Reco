import pandas as pd

data1= [[1,2,3],[4,5,6],[7,8,9]]
df1 = pd.DataFrame(data = data1, index = ['row1', 'row2', 'row3'], columns=['col1','col2','col3'])
print(df1)

data2 = [[1,2,3,4]]
df2 = pd.DataFrame(data =data2, index = ['row1'], columns=['col1','col2','col3','col4'])
print(df2)

print(df1.shape)
print(df2.shape)