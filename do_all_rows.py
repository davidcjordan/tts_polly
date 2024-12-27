#!/usr/bin/env python3
"""
This program reads a csv file that has columns: number,file name,words

For each row, it sends the 'words' text to Polly, gets a MP3 back, and names the MP3 file as per the file name column.

"""

import csv
import sys
import os
import argparse
from pathlib import Path
from make_mp3 import make_mp3_file

if __name__ == "__main__":

   phrases_file= None

   argParser = argparse.ArgumentParser()
   argParser.add_argument("input", type=str, help="input csv filename")

   args = argParser.parse_args()
   # print(f'\n\t{args.input= } {args.auth_path= }\n\t{args.dont_email= } {args.parse_only= }')

   if args.input is None:
      use_boomer_wav_csv = input("Do you want to generate MP3s from 'boomer_wav_files.csv' (Y/N): ")
      if use_boomer_wav_csv.lower() == 'y':
         phrases_file = "boomer_wav_files.csv"
      else:
         use_boomer_wav_csv = input("Do you want to generate MP3s from 'demo_announcements.csv' (Y/N): ")
         if use_boomer_wav_csv.lower() == 'y':
            phrases_file = "demo_announcements.csv"
         else:
            print("Quiting because a file was not selected.")
            sys.exit(1)
   elif Path(args.input).is_file():
      phrases_file = args.input
   else:
      sys.exit("file selected is not a file.")

   with open(phrases_file) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
         print(f"{row['file name']}  words: {row['words']}")
         base_filename= row['file name'][:-4]
         return_tuple= make_mp3_file(base_filename, row['words'])
         if return_tuple[0]:
               print(f"added file '{base_filename}.mp3' with tts for '{row['words']}'")
         else:
               print(f"{return_tuple[1]}")

