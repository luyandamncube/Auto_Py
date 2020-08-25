import os 
import argparse
import json
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser(description='Batch Obfuscate Rider Mappings')
    parser.add_argument('-i',
                       '--input',
                       required=True,
                       help='Input Directory')
    parser.add_argument('-o',
                       '--output',
                       required=True,
                       help='Output Directory')
    return parser.parse_args()

def parse_files(args):
    for filename in os.listdir(args.input):
        if filename.endswith(".json"): 
            # Run obfuscation per file
            obfuscate(args,filename)
        else:
            print(f"ERROR: {filename} File is in incorrect format")
            exit()
            continue

def obfuscate(args,filename):
    input_path = os.path.join(args.input, filename)
    output_path =  os.path.join(args.output, "OBFUSCATED_"+filename)
    if os.path.exists(output_path):
        os.remove(output_path )
    num_lines = sum(1 for line in open(input_path))
    with open(input_path, 'r') as f:
        for line in tqdm(f, total=num_lines, desc="Obfuscating "+filename):
            data = json.loads(line)
            for rider in data['Riders']:
                rider['Id'] =  800-int(rider['Id'])
            # Write Obfuscated line to new file
            f = open(output_path, "a")
            f.write(json.dumps(data,separators=(',', ':'))+"\n")
            f.close()
        print(f"Obfuscation done. File saved to {output_path}")

if __name__ == "__main__":
    args = parse_args()
    if not os.path.isdir(args.input):
        print("Input is not a directory")
        exit()
    if not os.path.isdir(args.output):
        print("Output is not a directory")
        exit()

    parse_files(args)

