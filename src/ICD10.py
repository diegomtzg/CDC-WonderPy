import bs4 as bs

columns = bs.BeautifulSoup(open("..\\resources\\allICD10Codes.html"), "html.parser").find_all((lambda tag: tag.name == 'td' 
                                   and tag.get('class') == ['line-number']
                                   and int(tag.get('value')) > 1550
                                   and int(tag.get('value')) < 11153))
for col in columns:
	td = col.parent.find_all('td')[1]
	print(td.find('span', {'class': "html-attribute-value"}).text)
	print(td.text)

#print(columns)