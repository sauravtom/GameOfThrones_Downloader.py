import sys
import urllib2
from bs4 import BeautifulSoup

url="http://www.wgofo.com/season/3"

arr=[]

def scrape_wgofo():
	soup = BeautifulSoup( urllib2.urlopen(url).read() )

	for i in soup.find_all('div',{'class' : 'item'}):
		link = i.a.get('href')
		link = 'http://www.wgofo.com'+link
		title = link[27:]
		arr.append([title,link])
		#print arr
		#print title,link
		#break

def scrape_flvs():
	for i in arr:
		soup = BeautifulSoup( urllib2.urlopen(i[1]).read() )

		for j in soup.find_all('div', {"style": "width:650px; float:left;"}):
			a = j.embed.get('flashvars')
			complete_link = a[a.find('=')+1:a.find('&')]
			#print complete_link
		i.append(complete_link)
	#print arr

def download_files():

	'''
		progress bar code taken from here http://blog.radevic.com/2012/07/python-download-url-to-file-with.html
	'''

	file_size_dl = 0
	block_sz = 192

	for i in arr[::-1]:
		#print 'Now downloading '+i[0]
		u = urllib2.urlopen(i[2])
		#data = u.read()
		f=open(i[0]+".flv", "wb")
		#f.write(data)
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print "Downloading: {0} Bytes: {1}".format(i[0], file_size)
		while True:
		    buffer = u.read(block_sz)
		    if not buffer:
		        break
		    file_size_dl += len(buffer)
		    f.write(buffer)
		    p = float(file_size_dl) / file_size
		    status = r"{0}  [{1:.2%}]".format(file_size_dl, p)
		    status = status + chr(8)*(len(status)+1)
		    sys.stdout.write(status)

		f.close()



if __name__ == '__main__':
	print 'Generating array of flv files to be downloaded'
	scrape_wgofo()
	scrape_flvs()
	download_files()
