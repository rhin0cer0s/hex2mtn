#! /usr/bin/env/python3
import argparse
import logging
from hex2mtn.ColorPalette import ColorPalette
from hex2mtn.MolotowVendor import Molotow
from hex2mtn.MontanaVendor import Montana
from hex2mtn.Color import Color

SCRIPT_VERSION = 0.1
WORKING_FOLDER = "./"

if "__main__" == __name__:

    parser = argparse.ArgumentParser("Montana Hexadecimal color finder")

    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(SCRIPT_VERSION))
    parser.add_argument('colors', action='store', nargs='+', metavar='color', type=str, help='color (as hexadecimal value)')
    parser.add_argument('--sync', action='store_true', dest='flagSync', default=False, help='refresh information from Montana website')
    parser.add_argument('--no-save', action='store_false', dest='flagNoSave', default=False, help='')
    parser.add_argument('--data-file', nargs=1, action='store', type=str, dest='dataFilePath', default='./montana_data.json')
    parser.add_argument('--rgb', action='store_true', dest='flagRGB', default=False, help='use RGB values instead of hexadecimal')
    parser.add_argument('--verbose', '--debug', action='store_true', dest='flagDebug', default=False, help='Enable log tracing')
    parser.add_argument('--color-chart', action='store_true', dest='flagColorChart', default=False, help='Create ')
    parser.add_argument('--color-chart-file', nargs=1, action='store', type=str, dest='colorChartFile', help='Filepath for the --color-chart option (default : /tmp/${PALETTE_NAME}.png)')
    parser.add_argument('--scheme-name', nargs=1, action='store', type=str, dest='schemeName', help='Name of the color scheme.')
    parser.add_argument('--productLine')
    
    args = parser.parse_args()

    if args.flagDebug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('[+] Enable debug')
        logging.debug("[*] Arguments :\n{}".format(args))
    else:
        logging.basicConfig(level=logging.INFO)

    # vendorData = Molotow(WORKING_FOLDER)
    vendorData = Montana(WORKING_FOLDER)
    
    if args.flagSync :
        vendorData.download_data()

        # Do not save if --no-save is specified
        if not args.flagNoSave :
            vendorData.save_data()
    else :
        try :
            vendorData.load_data()
        except Exception as e:
            logging.debug("[!] Error while opening local data. Did you run with the --sync argument first ?")
            raise Exception from e

    palette = ColorPalette()
    palette.vendors.append(vendorData)

    for idx, inputHexColorCode in enumerate(args.colors) :

        tmpColor = Color("unknown_{}".format(idx))
        tmpColor.from_hex(inputHexColorCode)

        palette.add(tmpColor)

    palette.find_similar_colors()
    palette.pretty_print()
    ## palette.color_chart(f"output_{vendorData.name}.jpg")
