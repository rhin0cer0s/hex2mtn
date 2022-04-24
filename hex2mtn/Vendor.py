
import json
import logging
import sys

from hex2mtn.Color import Color
from hex2mtn.Color import ColorJsonEncoder

class Vendor() :
    def __init__(self, workingFolder, name, dataFile) :
        global WORKING_FOLDER
        self.name = name
        self.dataFile = dataFile
        self.dataPath = f"{workingFolder}/{self.dataFile}"
        self.data = {}

    def pretty_print(self) :
        print("=== {} ===".format(self.name))
        print("")
        for productLineName, colors in self.data.items() :
            print("* {}".format(productLineName))
            for color in colors :
               print(color)
            print("")
        print("")

    def _parse_data(self, html : str) :
        raise NotImplementedError
    
    def download_data(self) :
        raise NotImplementedError
    
    def save_data(self) :
        if not self.data :
            logging.error(f"[!] {self.name} data is empty. Nothing to save.")
            raise ValueError(f"{self.name}.data is empty")

        logging.debug(f"[*] Save {self.name} to {self.dataPath}")
        logging.debug(f"[.] Opening {self.dataPath} for writing ...")
        with open(self.dataPath, "w") as vendorSaveFile :
            logging.debug("[+] OK !")
            logging.debug(f"[.] Dumping current {self.name} data ...")

            json.dump(self.data, vendorSaveFile, cls=VendorDataJsonEncode, indent=4)
            logging.debug("[+] OK !")

    def load_data(self) :
        if self.data :
            logging.warning(f"[!] {self.name} data is not empty and will be erased.")
        
        logging.debug(f"[*] Load {self.name} from {self.dataPath}")
        logging.debug(f"[*] Opening {self.dataPath} for reading ...")
        with open(self.dataPath, 'r') as vendorSaveFile :
            logging.debug("[+] OK!")
            logging.debug(f"[.] Reading {self.name} data ...")

            self.data = json.load(vendorSaveFile, object_hook=self.decode_json)
            logging.debug("[+] OK !")

    def decode_json(self, dict) :
        objKeys = dict.keys()
        colorKeys = ('name', 'red', 'green', 'blue')

        if all(objKey in colorKeys for objKey in objKeys) :
            return Color(**dict)
        elif all(objKey in self.productLine for objKey in objKeys) :
            return dict
        raise ValueError()

    def similar_colors(self, color : Color) -> list :
        similarColors = {}

        for productLineName, vendorColors in self.data.items() :
            colorDifference = sys.maxsize
            closestColors = []

            for vendorColor in vendorColors :
                tmpColorDifference = color.distance(vendorColor)
                if tmpColorDifference < colorDifference :
                    colorDifference = tmpColorDifference
                    closestColors = [vendorColor]
                elif tmpColorDifference == colorDifference :
                    closestColors.append(vendorColor)

            similarColors.update([(productLineName, closestColors)])

        return similarColors

class VendorDataJsonEncode(json.JSONEncoder) :

    def default(self, object ) :
        if isinstance(object, Color) :
            return ColorJsonEncoder.default(self, object) 
        return super().default(o)