from openpyxl import load_workbook

workbook = load_workbook(filename='xc/45A.xlsx')
sheet = workbook.active
names = sheet['G']  # 景点名称
ids = sheet['G']  # 景点ID
urls = sheet['F']  # 景点url
add_params = {}
for name, jid, url in zip(names[1:30], ids[1:30], urls[1:30]):
    # add_params['j_name'] = name.value  # 景点名称
    # add_params['j_id'] = jid.value  # 景点ID
    jid = name.value # 景点url
    print(jid)