from openpyxl import load_workbook

workbook = load_workbook(filename=r'C:\Users\windows\Desktop\xcw\45A.xlsx')
sheet = workbook.active
names = sheet['C']  # 景点名称
ids = sheet['G']  # 景点ID
urls = sheet['F']  # 景点url
add_params = {}
num = 0
for name, jid, url in zip(names[1:], ids[1:], urls[1:]):
    print(name.value,jid.value)
    num += 1
print(num)

# dd = {'a': 'a', 'b': 'b'}
# print(list(dd.values()))
