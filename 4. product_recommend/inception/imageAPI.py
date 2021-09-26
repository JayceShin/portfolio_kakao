from google_images_download import google_images_download
from inception.dbConnect import Con

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Image:
    def imageCrawling(self, keyworld, dir):
        response = google_images_download.googleimagesdownload()
        arguments = {"keywords": keyworld,
                     "limit":10,
                     "print_urls":True,
                     "no_directory":True,
                    "output_directory":dir}
        path = response.download(arguments)
        print(path)

    def getImage(self):
        con = Con()
        kang = con.selectProduct()

        for row in kang:
            productName = row
            productPath = 'clothes/' + row
            self.imageCrawling(productName, productPath)