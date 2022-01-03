import favicon
import requests
from PIL import Image
import re
import tldextract


def downloadico(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}
    try:
        icons = favicon.get(url, headers=headers)
    except Exception as e:
        print(e)
        return None

    for icon in icons:

        # We'll look for the actual tab icon from all pictures in the page
        if icon.format == "ico" and "ico" in icon.url:
            try:
                icoresponse = requests.get(icon.url, stream=True)
            except Exception as e:
                print(e)
                return None

            # This changes scheme in case download was not successful
            if icoresponse.status_code != 200:
                try:
                    icoresponse = requests.get(icon.url.replace("http", "https"), stream=True)
                except Exception as e:
                    print(e)
                    return None

            if icoresponse.status_code != 200:
                return None, None, None
            # Produce name for file saving later
            iconloc = "Icons/{}.ico".format(tldextract.extract(url).domain)

            # remove chars which are not allowed by windows for filenames
            iconloc = re.sub(r'[?|$|!]', '', iconloc)

            # Download icon and save it
            try:
                with open(iconloc, 'wb') as image:
                    for chunk in icoresponse.iter_content(1024):
                        image.write(chunk)
            except Exception as e:
                print(e)
                return None

def main():
    with open("Resources/top500urls.txt", "r") as urlfile:
        urlist = urlfile.read().splitlines()

    for url in urlist[300:]:
        print(url)
        downloadico(url)


if __name__ == "__main__":
    main()