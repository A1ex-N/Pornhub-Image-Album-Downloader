from PHDL import PHDL
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to pornhub album")
    parser.add_argument("-f", "--folder", default="", help="Folder to download images to", required=False)
    parser.add_argument("-o", "--overwrite", default=False, action=argparse.BooleanOptionalAction, help="Overwrite existing files")
    parser.add_argument("-s", "--stopAfter", default=-1, type=int, help="Stop after X amount of files downloaded")
    args = parser.parse_args()

    phdl = PHDL(args.url)
    phdl.DownloadImages(args.folder, overwrite=args.overwrite, stopAfter=args.stopAfter)

if __name__ == "__main__":
    main()

