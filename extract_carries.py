from bs4 import BeautifulSoup

def options (soup, id):
	option_values = []
	options = soup.find(id=id)
	for option in options.find_all('option'):
		option_values.append(option['value'])
	return options_values

def print_list(label, codes):
	print "\n{0}:".format(label)
	for c in codes:
		print c

def main():
	soup = BeautifulSoup(open('Data Elements.html'))

	codes = options(soup, 'CarrierList')
	print_list ("Carriers", codes)

	codes = options (soup, 'AirportList')
	print_list ("Airports", codes)