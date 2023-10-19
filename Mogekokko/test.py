import subprocess
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s','--sample',nargs='?',help='Bucket26..36 or Prompt_data')
parser.add_argument('-id','--ID', nargs='+',help='Cell ID', type=int)
parser.add_argument('-e','--E',nargs='+',help='Min E and Max E',type=int)
args = parser.parse_args()
Set_ID = set(args.ID)

print(f"Data = {args.sample} CellID in {args.ID} {args.E[1]}>E>{args.E[0]}")
print(f"CellID = {args.ID}")
