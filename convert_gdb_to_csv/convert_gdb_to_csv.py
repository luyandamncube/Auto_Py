# [1] 20:50
# [2] 21:05
import sys 
import argparse
import platform
import subprocess, shlex
import os

if (platform.system() == 'Windows' ):
    escapeCharacter = '\\' 
else:
    escapeCharacter = '//' 

def parse_args():
    parser = argparse.ArgumentParser(description='JSON question bank reader')
    parser.add_argument('-i',
                       '--input',
                       required=True,
                       help='Input Directory')
    parser.add_argument('-o',
                       '--output',
                       required=True,
                       help='Output Directory')    
    args = parser.parse_args()

    # if (os.path.isfile(args.input) == True):
    #     print(f"ERROR: -i is not a directory")
    #     exit()

    return parser.parse_args()

def convert_gdb_to_csv(args):
    extract_layers = 'wVCAP'
    #Use gdal's ogr2ogr to convert the gdb files to CSV's
    command =f'''
        ogr2ogr 
        -f "CSV" 
        {args.output}/wVCAP_2023.csv
        {args.input}
        {extract_layers} 
        -progress
        -lco GEOMETRY=AS_WKT
        -lco GEOMETRY_NAME=geometry
        -overwrite
        -nlt CONVERT_TO_LINEAR
    '''

    print(command)
    command = shlex.split(command)

    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)
    print(error)

if __name__ == "__main__":
    args = parse_args()
    convert_gdb_to_csv(args)