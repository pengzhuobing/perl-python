import win32com,os,sys,re
from win32com.client import Dispatch, constants
from win32com.client import gencache
import time
import datetime
from config import rules, body_start, body_end


def createPdf(wordPath, pdfPath):
    if os.path.exists(pdfPath):
        os.remove(pdfPath)
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = 0
    word.DisplayAlerts = 0
    doc = word.Documents.Open(wordPath)
    try:
        doc.SaveAs(pdfPath, 17) #  txt=4, html=10, docx=16， pdf=17
        doc.Close()
        word.Quit()
    except Exception as e:
        print(str(e))

if len(sys.argv) < 1:
    print("Usage: python %s [word_dir]" % sys.argv[0])
    sys.exit(2)

file_path = input("input word path:")

log_file = "%s.log.txt" % datetime.date.today().strftime('%Y-%m-%d')
with open(log_file, 'a') as fh:
    fh.write("####################################\n")
    r = [str(i) for i in range(1, len(rules)+1)]
    fh.write("#FileName\t%s\n" % ("\t".join(r)))

all_doc = []
for root, path, files in os.walk(file_path):
    for afile in files:
        if afile.endswith(".docx"):
            all_doc.append(os.path.join(root, afile))

with open('all_doc.txt', 'w', encoding="utf-8") as fh:
    for ff in all_doc:
        recode = ff.replace(u'\xa0', u'')
        fh.write(recode + "\n")

for ff in all_doc:
    w = win32com.client.Dispatch('Word.Application')
    w.Visible = 0
    w.DisplayAlerts = 0
    print("Info: relpace file name: %s" % ff.replace(u'\xa0', u''))
    pdf = ff.replace('.docx', '.pdf')
    doc2 = w.Documents.Open(ff)
    doc_map = {
        "header": w.ActiveDocument.Sections[0].Headers[0],
        "body": doc2,
        "footer": w.ActiveDocument.Sections[0].Footers[0]
    }
    status = []
    for rule in rules:
        doc_obj = doc_map.get(rule["type"])
        if rule["type"] == "body":
            the_range = doc_obj.Range(body_start, body_end)
        else:
            the_range = doc_obj.Range
        obj = re.search(rule['pattern'], str(the_range))
        if obj:
            status.append("True")
            old_text = obj.group()
            new_text = rule['replace_to']
            i = 1
            for group in obj.groups():
                new_text = new_text.replace('[%s]' % i, group)
                i += 1
            the_range.Find.Execute(old_text, False, False, False, False, False, False, 1, False, new_text, 1)
        else:
            status.append("False")
    with open(log_file, 'a', encoding="utf-8") as fh:
        record = "%s\t%s\n" % (ff, "\t".join(status))
        record = record.replace(u'\xa0', u' ')
        #record.encode('utf-8')
        fh.write(record)
    doc2.Close()
    try:
        w.Documents.Close()
        # w.Quit()
    except Exception as e:
        pass
        # print(str(e))
    # createPdf(ff, pdf)
