from openpyxl import load_workbook

workbook = load_workbook(filename='../4A5A汇总.xlsx')
sheet = workbook.active
names = sheet['C']  # 景点名称
ids = sheet['G']  # 景点ID
urls = sheet['F']  # 景点url
add_params = {}
for name, jid, url in zip(names[1:30], ids[1:30], urls[1:30]):
    add_params['j_name'] = name.value  # 景点名称
    add_params['j_id'] = jid.value  # 景点ID
    j_url = url.value  # 景点url
    print(j_url,add_params)