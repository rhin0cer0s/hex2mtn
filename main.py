#! /usr/bin/env/python3
import argparse
import configparser
import logging
import pprint

from hex2mtn.ColorChart import ColorChart
from hex2mtn.ColorPalette import ColorPalette
from hex2mtn.MolotowVendor import Molotow
from hex2mtn.MontanaVendor import Montana
from hex2mtn.Color import Color

_SCRIPT_NAME = "hex2mtn"
_SCRIPT_VERSION = 0.2
WORKING_FOLDER = "./"
_CONF_PATH = ""

pp = pprint.PrettyPrinter(indent=4)

def _output_dict(o : dict = None, depth : int = 0) :
    for key, value in o :
        print(f"{key} : {value}")
"""
returns: 
"""
def get_options_from_conf_file() :
    # Parse args options for "-c/--conf" arguments
    # If no "-c/--conf" given, it will default to the global _CONF_PATH value
    args_parser = argparse.ArgumentParser(add_help=False)
    args_parser.add_argument(
            "-c", 
            "--conf",
            action='store',
            dest='conf_path',
            default=_CONF_PATH,
            help="Specify config file - commandline arguments will overwrite")
    conf_arg, remaining_args = args_parser.parse_known_args()

    # Parse the configuration file
    conf_file_parser = configparser.ConfigParser()
    conf_file_parser.read([conf_arg.conf_path])

    # Aggregate nicely all the options into a dict
    # { 'section_option' : value, ... }
    options_from_conf_file = {}

    for section, options in conf_file_parser._sections.items() :
        for key, value in options.items() :
            try :
                options_from_conf_file[f"{section}_{key}"] = conf_file_parser[section].getboolean(key)
            except :
                options_from_conf_file[f"{section}_{key}"] = value

    return options_from_conf_file, remaining_args

def get_options_from_command_line(file_options, remaining_args) :
    # Parse the remaining arguments
    remaining_args_parser = argparse.ArgumentParser()
    remaining_args_parser.set_defaults(**file_options)
    remaining_args_parser.add_argument('--version', 
            action='version', 
            version=f"{_SCRIPT_NAME} {_SCRIPT_VERSION}")

    remaining_args_parser.add_argument('--debug',
        action='store_true',
        dest='main_debug',
        help='Enable log tracing')

    remaining_args_parser.add_argument('--sync', 
            action='store_true', 
            dest='main_sync', 
            help='Refresh information from Montana website')

    remaining_args_parser.add_argument('--save-vendor', 
            action='store_true', 
            dest='vendor_save',
            help='Save vendor data to --vendor-path. Defaults to current folder if not set.')

    remaining_args_parser.add_argument('--vendor-path',
            action='store', 
            type=str,
            dest='vendor_path')

    remaining_args_parser.add_argument('--rgb',
            action='store_true',
            dest='output_rgb', 
            help='use RGB values instead of hexadecimal')

    remaining_args_parser.add_argument('--chart',
            action='store_true',
            dest='output_chart',
            help='Create a .PNG file containing color suggestions. Uses [--chart-path] value.')

    remaining_args_parser.add_argument('--chart-file',
            action='store',
            type=str,
            dest='output_chart_path',
            help='Filepath for the --chart option (default : /tmp/[--name].png)')

    remaining_args_parser.add_argument('--name',
            action='store',
            type=str,
            dest='main_name',
            help='Palette name (default : "unknown")')

    remaining_args_parser.add_argument('colors',
            action='store',
            nargs='+',
            metavar='color',
            type=str,
            help='Color (as hexadecimal value)')

    command_line_args = remaining_args_parser.parse_args(remaining_args)

    # Aggregate nicely all the options into a dict
    options_from_command_line = command_line_args.__dict__

    return options_from_command_line

def handle_conf() :
    file_options, remaining_args = get_options_from_conf_file()
    definitive_options = get_options_from_command_line(file_options, remaining_args)

    return definitive_options

def main() :
    conf = handle_conf()

    if conf['main_debug'] :
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('[+] Enable debug')
        logging.debug("[*] Configuration :")
        pp.pprint(conf)
    else:
        logging.basicConfig(level=logging.INFO)

    return conf

if "__main__" == __name__:

    conf = main()

    # vendorData = Molotow(WORKING_FOLDER)
    vendorData = Montana(WORKING_FOLDER)
    
    if conf['main_sync'] :
        vendorData.download_data()

        if conf['vendor_save'] :
            vendorData.save_data()
    else :
        try :
            vendorData.load_data()
        except Exception as e:
            logging.debug("[!] Error while opening local data. Did you run with the --sync argument first ?")
            raise Exception from e

    palette = ColorPalette(conf['main_name'], nb_similar_colors=3)
    palette.vendors.append(vendorData)

    for idx, inputHexColorCode in enumerate(conf['colors']) :

        tmpColor = Color("unknown_{}".format(idx))
        tmpColor.from_hex(inputHexColorCode)

        palette.add(tmpColor)

    palette.find_similar_colors()
    palette.pretty_print()

    colorChart = ColorChart(palette)
    colorChart.draw("aaa")
    ## palette.color_chart(f"output_{vendorData.name}.jpg")
