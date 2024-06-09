from bs4 import BeautifulSoup
import urllib.request
import requests
def save_signed_video(w):
        url = 'https://www.signingsavvy.com/search/' + w.lower()
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        if soup.find_all('video') == []:
            new_url = "???"
            # name/fingerspelling
            if str(soup).find("(as in ") != -1:
                new_url = 'https://www.signingsavvy.com/' + [x for x in soup.find_all('a') if str(x).find('sign/') != -1][0].attrs['href']
            # multiple meanings #TODO: context
            elif str(soup).find("No direct match on") != -1:
                new_url = 'https://www.signingsavvy.com/' + f"sign/{w}/0/fingerspell"
            r = requests.get(new_url)
            soup = BeautifulSoup(r.content, 'html.parser')
        new_list = [x for x in soup.find_all('video')[0].contents if str(x).find('src') != -1]
        video_url = new_list[0].attrs['src']
        urllib.request.urlretrieve(video_url, f'videos/{w}.mp4')
        return video_url, url

f = open("subtitles-1.txt", "r")
text = f.read()
text = text.replace(";", " ")
list_of_words = text.lower().split(" ")

for word in list_of_words:
    save_signed_video(word)