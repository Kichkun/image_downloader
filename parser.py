import argparse

from download_google import main

parser = argparse.ArgumentParser(description='Search parameters')

parser.add_argument('-s', dest='search_phrase', default='sth', help='Phrase for search')
parser.add_argument('-c', dest='chromedriver', default='/usr/local/bin/chromedriver', help='path to chromedriver')
parser.add_argument('-d', dest='detect_face', default=False, help='save images with faces only')
parser.add_argument('-o', dest='output_folder', default='.', help='location for output results')
parser.add_argument('-b', dest='headless', default=False, help='launch google chrome to be able to see and control or do in background')

args = parser.parse_args()

main(args.search_phrase, args.chromedriver, args.detect_face, args.output_folder, args.headless)