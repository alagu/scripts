import sys
import mechanize
import BeautifulSoup

lccp_pnrno1 = sys.argv[1][:-7]
lccp_pnrno2 = sys.argv[1][3:]

br = mechanize.Browser()
br.open('http://www.indianrail.gov.in/pnr_stat.html')
br.select_form(name='pnr_stat')
br['lccp_pnrno1'] = lccp_pnrno1
br['lccp_pnrno2'] = lccp_pnrno2
response2 = br.submit()
responseBody = response2.read()

print response2.geturl()
print response2.info()
print responseBody

f = open('test.txt','r')
responseBody  = f.read()
f.close()
