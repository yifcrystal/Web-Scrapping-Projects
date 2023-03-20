from bs4 import BeautifulSoup
import requests

def main():
	try:
		url= "https://gsm.ucdavis.edu/master-science-business-analytics-msba"
		page = requests.get(url)
		# Create a beautifulsoup object 
		soup = BeautifulSoup(page.text, 'lxml')
		# find <p> that immediately follows <div> of class "col-md-6.
		list_of_contents = soup.select("div.col-md-6 > p")
		# prints the HTML content to the screen (almost only text here
		# just need to replaces "&nbsp;" with " ")
		for i in list_of_contents:
			print(i.text)
	
	except:
		print("Problem with the connection...")

if __name__ == '__main__':
	main()