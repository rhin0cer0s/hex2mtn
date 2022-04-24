import json
import logging
import requests
import sys

from bs4 import BeautifulSoup
from hex2mtn.Color import Color
from hex2mtn.Vendor import Vendor

class Montana(Vendor):

    def __init__(self, workingFolder):
        self.name = "Montana Catalogue"
        self.rootProductPage = "https://www.montanacolors.com/en/productos/"
        self.productLine = ['mtn-94', 'hardcore', 'water-based-300', 'water-based-100', 'mega-colors', 'nitro-2g-colors']
        super().__init__(workingFolder=workingFolder, name="Montana", dataFile="montana.json")

    def _parse_data(self, html : str) :
        """Parse HTML data from the vendor's website.
        The output is an array of <class Color>.
        """

        soup = BeautifulSoup(html, 'html.parser')
        items_color = soup.find_all("div", class_="m-color_info")

        if not items_color :
            raise ValueError("No m-color_info class found.")

        data = []

        for item in items_color : 
            spans = item.find_all("span")
            mtn_name = spans[0].string
            hex_code = spans[2].string
            logging.debug("[-] {} : {}".format(hex_code, mtn_name))

            # Some of Montana's references do not have HEX information, eg : MTN 94 Jewel Silver
            if hex_code == None :
                logging.debug("[!] No HEX code found for {} !. Pass.".format(mtn_name))
            else :
                newColor = Color(mtn_name)
                newColor.from_hex(hex_code) 
                data.append(newColor)

        if not data :
            raise ValueError("No HEX code found on the product page.")

        return data

    def download_data(self) :
        logging.info("[*] Download data from Montana's Website ...")

        for product in self.productLine:
            logging.debug("[-] Product : {}".format(product))
            productUrl = "{}{}/".format(self.rootProductPage, product)
            response = requests.get(productUrl)

            if response.status_code != 200:
                logging.info("[!] Error getting {} informations.".format(product))
                continue

            html = response.text
            colorList = self._parse_data(html)
            self.data.update([(product, colorList)])

        if self.data == {} :
            raise Exception("Unable to get any information for {}. Check rootPageProduct and your internet connexion.".format(self.name))
        pass
    