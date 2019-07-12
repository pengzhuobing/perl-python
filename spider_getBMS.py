from bs4 import BeautifulSoup
import requests
import sys

SHOW_TABLE_URL = "http://192.168.224.217/bms/request/item/showssample.jsp"

def get_bms_table(itemid):
    url = "%s?itemid=%s" % (SHOW_TABLE_URL, itemid)
    response = requests.request("GET", url)
    response.encoding = 'utf-8'
    return response.text

def param_bms_table(html_str):
    b = BeautifulSoup(html_str, "html.parser")
    t = b.table
    trs = t.find_all("tr")
    trs = trs[1:]
    is_head = True
    bms_table = {
        "header": [],
        "content": []
    }
    for tr in trs:
        tds = tr.find_all("td")
        content_line = []
        for td in tds:
            text = td.text
            if is_head:
                bms_table["header"].append(text)
            else:
                content_line.append(text)
        is_head = False
        if len(content_line) > 0:
            bms_table["content"].append(content_line)
    return bms_table
# for i in b.children:
#     print(i)

if len(sys.argv) < 2:
    print("python getbms.py <itemid>")
    sys.exit(0)

item_id = sys.argv[1]
html_str = get_bms_table(item_id)
bms_table = param_bms_table(html_str)
print("\t".join(bms_table["header"]))
for item in bms_table["content"]:
    print("\t".join(item))
