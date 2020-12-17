import bs4 as bs
import re
from fuzzywuzzy import fuzz
import requests
import pickle
import os

# python script for getting all ICD10 codes out of HTML files (it also replaces the labels on those that are cut off)

if not os.path.isfile('..\\ICD10CodeToLabels.pickle'):
    columns = bs.BeautifulSoup(open("allICD10Codes.html"), "html.parser").find_all((lambda tag: tag.name == 'td' \
                                                                                and tag.get('class') == ['line-number'] \
                                                                                and int(tag.get('value')) > 1550 \
                                                                                and int(tag.get('value')) < 11153))

    codeToLabels = dict()

    print("get All codes...")
    icdWeb = bs.BeautifulSoup(open("ICD10Codes.html"), "html.parser").find_all('a', {'class':'ygtvlabel'})
    codeToDescript = dict()
    for webObj in icdWeb:
        text = webObj.get_text(separator="\n").strip().split('\n')
        if(len(text) == 3):
            codeToDescript[webObj.get("data-id")] = text[2]

    for col in columns:
        td = col.parent.find_all('td')[1]
        codeSpan = td.find('span', {'class': "html-attribute-value"})
        if(codeSpan != None):
            code = codeSpan.text
            if("..." in td.text):
                if code in codeToDescript:
                    label = codeToDescript[code]
                else:
                    oldLine = re.findall('\((.*)\)', td.text)[0]
                    maxRatio = 0
                    maxLine = None
                    maxKey = None
                    for (k, v) in codeToDescript.items():
                        ratio = fuzz.token_set_ratio(oldLine, v)
                        if(ratio > maxRatio):
                            maxRatio = ratio
                            maxLine = v
                            maxKey = k

                    label = maxLine
            else:
                label = re.findall('\((.*)\)', td.text)[0]
            codeToLabels[code] = label

    with open('..\\ICD10CodeToLabels.pickle', 'wb') as handle:
        pickle.dump(codeToLabels, handle)

else:
    with open('..\\ICD10CodeToLabels.pickle', 'rb') as handle:
        codeToLabels = pickle.load(handle)

for (k, v) in codeToLabels.items():
        print(k+" : "+v)