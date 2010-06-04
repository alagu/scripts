'''
This script allows you to download your payslips from the ascent site
'''
import httplib
import urllib

def fetch_report(year, month, selected_report) :
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language' : 'en-us,en;q=0.5',
    'Accept-Encoding' : 'gzip,deflate',
    'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive' : '115',
    'Connection' : 'keep-alive',
    'Referer' : 'https://www.ascent-online.net/AP384/index.php?action=content&section=4&home=Y&gen_rep=Y',
    'Cookie' : 'PHPSESSID=XXXXXXXX', ## <--- Replace here with your session ID You can find it in your cookies
    'Content-Type' : 'application/x-www-form-urlencoded'}

    #This is a bad way, fix this
    if selected_report == 'Consolidated_Pay_slip':
      data  = '=04&=2010&cpmonth=%02d&cpyear=%s&pmonth=04&pyear=2010&sdmonth=04&sdyear=2010&pfmonth=04pfyear=2010&tmonth=04&tyear=2010&str_mon=00&str_yer=2010&end_mon=00&end_yer=2010&super=2010&selected_report=%s&view_type=pdf' % (month, year, selected_report)
    elif selected_report == 'Payslip' :
      data  = '=04&=2010&cpmonth=04&cpyear=2010&pmonth=%02d&pyear=%s&sdmonth=04&sdyear=2010&pfmonth=04&pfyear=2010&tmonth=04&tyear=2010&str_mon=00&str_yer=2010&end_mon=00&end_yer=2010&super=2010&selected_report=%s&view_type=pdf' % (month, year, selected_report)
    elif selected_report == 'Statutory_ded' :
      data  = '=04&=2010&cpmonth=04&cpyear=2010&pmonth=04&pyear=2010&sdmonth=%02d&sdyear=%s&pfmonth=04&pfyear=2010&tmonth=04&tyear=2010&str_mon=00&str_yer=2010&end_mon=00&end_yer=2010&super=2010&selected_report=%s&view_type=pdf' % (month, year, selected_report)
    elif selected_report == 'PF_Details' :
      data  = '=04&=2010&cpmonth=04&cpyear=2010&pmonth=04&pyear=2010&sdmonth=04&sdyear=2010&pfmonth=%02d&pfyear=%s&tmonth=04&tyear=2010&str_mon=00&str_yer=2010&end_mon=00&end_yer=2010&super=2010&selected_report=%s&view_type=pdf' % (month, year, selected_report)
    elif selected_report == 'Tax_Calculator' :
      data  = '=04&=2010&cpmonth=04&cpyear=2010&pmonth=04&pyear=2010&sdmonth=04&sdyear=2010&pfmonth=04&pfyear=2010&tmonth=%02d&tyear=%s&str_mon=00&str_yer=2010&end_mon=00&end_yer=2010&super=2010&selected_report=%s&view_type=pdf' % (month, year, selected_report)

    c = httplib.HTTPSConnection("www.ascent-online.net",443)
    c.request("POST", "/AP384/index.php?action=report",data,headers)
    r = c.getresponse()
    filename = '%s_%s_%02d.pdf' % (selected_report, year, month)
    print 'fetching ' + filename
    fp = open(filename,'w')
    fp.write(r.read())
    fp.close()

year_set =  {'2007' : range(7,13), ## <--Your work experience
             '2008' : range(1,13),
             '2009' : range(1,13),
             '2010' : range(1,5) }

selected_report_list = ["Consolidated_Pay_slip", "Payslip", "Statutory_ded", "PF_Details",
"Tax_Calculator"]
for selected_report in selected_report_list:
  for year in year_set:
      for month in year_set[year]:
          fetch_report(year, month, selected_report)
