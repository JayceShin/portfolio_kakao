import urllib.request
import os


class Down:

    def downloader(self, path, fileName):

        # file path and file name to download
        outpath = "/Users/shinkangsik/django/imageT/down/"
        outfile = fileName

        # Create when directory does not exist
        if not os.path.isdir(outpath):
            os.makedirs(outpath)

        # download
        urllib.request.urlretrieve(path, outpath+outfile)
        print("complete!")