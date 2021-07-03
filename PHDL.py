import requests
import json
import os


s = requests.Session()


def download(url, iterator, amount, path):
    print(f"Downloading {url} ({iterator}/{amount})")
    img = s.get(url).content
    with open(f"{path}", "wb+") as file:
        file.write(img)


class PHDL:
    json_url = "https://www.pornhub.com/album/show_album_json?album="
    album_id = ""
    large_img_urls = []

    def __init__(self, url):
        """
        Populates self.largeImgUrls and sets self.album_id

        Parameters:
            url (string): The URL to the pornhub album to download images from
        """
        if url is None:
            print("You must set a URL to a pornhub album")
            exit()

        self.album_id = url.split('/')[-1]
        album_url = self.json_url + self.album_id

        json_response = s.get(album_url).text
        json_object = json.loads(json_response)

        for child in json_object:
            is_fan_only = json_object[child]["isFanOnly"]
            large_image_url = json_object[child]["img_large"]

            if is_fan_only is False:
                self.large_img_urls.append(large_image_url)

            else:
                print(f"{large_image_url} is fan only. Skipping.")

    def print_urls(self, show_counter=False):
        """
        Prints all image URL's

            Parameters:
                show_counter (bool): Specifies whether or not to show a counter for each URL (e.g. (1/219)).
                                    Default is False
        """
        if len(self.large_img_urls) == 0:
            return "No images to download"

        for i, url in enumerate(self.large_img_urls, start=1):
            if show_counter:
                print(f"{url} ({i}/{len(self.large_img_urls)})")
            else:
                print(url)

    def download_images(self, folder_name="", overwrite=False, stop_after=-1):
        """
        Downloads all "img_large" images from a pornhub photo album

            Parameters:
                folder_name (string): The folder to download images to. Default is the album ID.
                overwrite (bool): Specifies whether or not to overwrite existing files. Default is False.
                stop_after (int): Stop downloading images after x amount of images have been downloaded.
                                 default is -1 (all)
        """
        amount_of_imgs: int = len(self.large_img_urls)

        if amount_of_imgs == 0:
            return "No images to download"

        if stop_after == -1:
            stop_after = len(self.large_img_urls)

        if folder_name == "":
            folder_name = self.album_id

        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        for i, url in enumerate(self.large_img_urls, start=1):
            extension = url.split('.')[-1]
            full_path = f"{folder_name}/{i}.{extension}"
            if i - 1 == stop_after:
                break

            if overwrite:
                download(url, i, amount_of_imgs, full_path)
            else:
                if not os.path.exists(full_path):
                    download(url, i, amount_of_imgs, full_path)
                else:
                    print(f"{full_path} already exists. Skipping. ({i}/{amount_of_imgs})")
