import re, requests, bs4, os
import logging
from datetime import datetime
import string, unicodedata
import glob


class WebCrawler():



  def get_urls_from_content(self, content):
      soup = bs4.BeautifulSoup(content, 'html.parser')
      anchors = soup.select('a')
      return (a["href"] for a in anchors if a.has_attr("href") and self.url_pattern.match(a["href"]))


  def slugify(self, value):
      validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
      cleaned = unicodedata.normalize('NFKD', value).encode('ASCII', 'ignore').decode("ascii")
      return ''.join(c if c in validFilenameChars else '-' for c in cleaned)



  def create_file_name(self, href):
      groups = self.url_pattern.search(href)
      try:
        parts = (groups.group(i) for i in range(groups.lastindex + 1)[1:])
        return self.target_dir + self.slugify(" - ".join(parts)) + ".html"
      except:
        raise Exception("Invalid url: ", href)


  def write_to_file(self, filename, text):
      with open(filename, "wb") as f:
          f.write(text)
	

  def download_content(self, url):
      status =  content = None
      try:
          res = requests.get(url)
          status = "success" if res.status_code == 200 else "error"
          content = res.content
      except requests.exceptions.RequestException as error:
        status, content = "error", error
      return (status, content)


  def is_downloaded(self, url):
  	file_name = self.create_file_name(url)
  	return os.path.isfile(file_name)



  def log_download_status(self, url, status, filename):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    msg = "{0}, {1}, {2}, {3}".format(now, url, status, filename)
    print(msg)
    with open(self.target_dir + "status.csv", "a") as f:
      f.write(msg + "\n")

  

  def crawl(self, url, force = False):
    filename = self.create_file_name(url)
    if force or not self.is_downloaded(url):
      status, content = self.download_content(url)
      if status == "success":
        self.write_to_file(filename, content)
        self.process_content(content)  
      self.log_download_status(url, status, filename)


  def process_content(content):
    for url in self.get_urls_from_content(content):
      self.crawl(href)
      

  def load_from_files(self, path):
    for file in glob.glob(path):
      with open(file) as f:
        self.process_content(f.read())



  def load_from_url(self, urls):
    for url in urls:
      self.crawl(url, force = True)



  def __init__(self, pattern, home_urls, target_dir):
    self.url_pattern = re.compile(pattern)
    self.target_dir = target_dir
    self.load_from_url(home_urls)
    self.load_from_files(target_dir + "*.html")


source = {"time.com" : {
  "regex" : [{r"^http://time.com/(\d+)/(\S+)/\S+", "content"},
             {r"^http://time.com/(\d+)/(\S+)/\S+", "content"}],
  "home" : ["http://time.com/","http://time.com/magazine/us/"],
  "target_dir": "/data/time.com/"
},"bbc.com" : {
  "regex" : r"^http://www.bbc.com/news/()/",
  "home" : ["http://time.com/","http://time.com/magazine/us/"],
  "target_dir": "/data/time.com/"
}}



if __name__ == "__main__":
  time_com = source["time.com"]
  WebCrawler(time_com["regex"], time_com["home"], time_com["target_dir"])
  #WebCrawler(time_com["regex"], time_com["home"], time_com["target_dir"])
