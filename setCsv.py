



csvfile = codecs.open('百度索引结果.csv', 'w+', 'utf_8_sig')
writer = csv.writer(csvfile)

titleCsv = ('标题','url','是否伪静态')

writer.writerow(titleCsv)

data = [
('小河', '25', '1234567'),
('小芳', '18', '789456')
]


for i in data:
    writer.writerow(i)

for i in data:
    writer.writerow(i)


    
csvfile.close()
