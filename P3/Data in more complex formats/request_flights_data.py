import requests
from bs4 import BeautifulSoup

s = requests.Session()

r = s.get("http://www.transtat.bts.gov/Data_Elements.aspx?Data=2")
soup = BeautifulSoup(r.text)
viewstate_element = soup.find(id="__VIEWSTATE")
viewstate = viewstate_element['value']
eventvalidation_element = soup.find(id="__EVENTVALIDATION")
eventvalidation = eventvalidation_element['value']

r = s.post("http://transtat.bts.gov/Data_Elements.aspx?Data=2",
				data = (
					("__EVENTVALIDATE", "")
					("__EVENTARGUMENT", ""),
					("__VEIWSTATE", viewstate)
					("__VIEWSTATEGENERATOR", viewstategenerator),
					("__EVENTVALIDATION", eventvalidation),
					("CarrierList", "VX"), 
					("AirportList", "BOS")
					("Submit", "Submit")
					))