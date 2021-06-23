import requests
import json
import os

s = requests.Session()


class _Internal:
    def Download(url, iterator, amount, path):
        print(f"Downloading {url} ({iterator}/{amount})")
        img = s.get(url).content
        with open(f"{path}", "wb+") as file:
            file.write(img)

class PHDL():
    jsonUrl = "https://www.pornhub.com/album/show_album_json?album="
    albumId = ""
    largeImgUrls = []

    def __init__(self, url):
        '''
        Populates self.largeImgUrls and sets self.ablumId

        Parameters:
            url (string): The URL to the pornhub album to download images from
        '''
        if (url == None):
            return "You must set a URL to a pornhub album"

        self.albumId = url.split('/')[-1]
        albumUrl = self.jsonUrl + self.albumId

        jsonResponse = s.get(albumUrl).text
        jsonObject = json.loads(jsonResponse)

        for object in jsonObject:
            isFanOnly = jsonObject[object]["isFanOnly"]
            largeImageUrl = jsonObject[object]["img_large"]

            if isFanOnly == False:
                self.largeImgUrls.append(largeImageUrl)

            else:
                print(f"{largeImageUrl} is fan only. Skipping.")



    def PrintURLs(self, showCounter = False):
        '''
        Prints all image URL's

            Parameters:
                showCounter (bool): Specifies whether or not to show a counter for each URL (e.g. (1/219)).
                                    Default is False
        '''
        if len(self.largeImgUrls) == 0:
            return "No images to download"

        for i, url in enumerate(self.largeImgUrls, start=1):
            if showCounter:
                print(f"{url} ({i}/{len(self.largeImgUrls)})")
            else:
                print(url)



    def DownloadImages(self, folderName = "", overwrite = False, stopAfter = -1):
        '''
        Downloads all "img_large" images from a pornhub photo album

            Parameters:
                folderName (string): The folder to download images to. Default is the album ID.
                overwrite (bool): Specifies whether or not to overwrite existing files. Default is False.
                stopAfter (int): Stop downloading images after x amount of images have been downloaded.
                                 default is -1 (all)
        '''
        amountOfImgs = len(self.largeImgUrls)

        if (amountOfImgs == 0):
            return "No images to download"

        if (stopAfter == -1):
            stopAfter = len(self.largeImgUrls)

        if folderName == "":
            folderName = self.albumId

        if (not os.path.isdir(folderName)):
            os.mkdir(folderName)


        for i, url in enumerate(self.largeImgUrls, start=1):
            extension = url.split('.')[-1]
            fullPath = f"{folderName}\{i}.{extension}"
            if (i - 1 == stopAfter):
                break

            if overwrite:
                _Internal.Download(url, i, amountOfImgs, fullPath)
            else:
                if not os.path.exists(fullPath):
                    _Internal.Download(url, i, amountOfImgs, fullPath)
                else:
                    print(f"{fullPath} already exists. Skipping. ({i}/{amountOfImgs})")
