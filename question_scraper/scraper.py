import PyPDF2 
import sys 
import os 
import argparse
import json
import string
import random

def parse_args():
    parser = argparse.ArgumentParser(description='Pdf scraper')
    parser.add_argument('-i',
                       '--input',
                       required=True,
                       help='Input File')
    parser.add_argument('-o',
                       '--output',
                       required=True,
                       help='Output Directory')
    
    args = parser.parse_args()
    if (args.input.endswith(".pdf") == False):
        print(f"ERROR: -i is not a pdf")
        exit()

    if (os.path.isfile(args.output) == True):
        print(f"ERROR: -o is not a directory")
        exit()

    return parser.parse_args()

def parse_line(line):
    # Clean up strings     
    if ('Section:' in line):
        line = line.replace("Section: [none]","")
    if ('References:' in line):
        line = '\n' + line + '\n'
    if ('A.' in line or 'B.' in line  or 'C.' in line or 'D.' in line or 'E.' in line or 'F.' in line):
        line = '\n' + line
    return (line)

def parse_qa(question, answer):
    dict_ = {}
    dict_['question'] = question

    
    if ('Correct Answer:' in answer):
        answer = answer.replace("Correct Answer: ","")
    
    description_ = ""
    description = answer.splitlines()
    
    dict_['answer'] = description[0]
    for i in range(2, len(description)):  
        description_ = description_ + description[i]

    dict_['description'] = description_
    # print(description)
    return dict_

def parse_pages(pages, output_dir):
    question = answer = ""
    explanation_counter = question_counter = 0
    answer_flag = question_flag = False
    
    for index,line in enumerate(pages.splitlines()):
        if ('QUESTION' in line):
            if (answer_flag == True):
                explanation_counter = 0
                question_counter += 1 
                qa = parse_qa(question, answer)
                dump_qa(qa,output_dir)
                question = answer = ""
            answer_flag = False
            question_flag = True
            line = ""
            
        if ('Correct Answer:' in line):
            answer_flag = True
            question_flag = False
        line = parse_line(line)
        if ('Explanation' in line):
            if (explanation_counter == 0):
                explanation_counter += 1
                line = '\n' + line + '\n'
            else:
                line = ""
        if (answer_flag == True and question_flag == False):
            answer = answer + line 
        elif (answer_flag == False and question_flag == True and index > 1): 
            question = question + line

def parse_pdf(pdf_file):
    pdf = open(pdf_file, 'rb')
    text = PyPDF2.PdfFileReader(pdf)
    pages = ""

    i = 0 
    for page in text.pages: 
        i += 1
        if (i != 1):
            for line in page.extractText().splitlines():
                # remove garbage
                if ('https://www.gratisexam.com/' in line):
                    continue
                else: 
                    pages = pages + line + '\n'
    return (pages)

def dump_qa(qa, output_dir):
    question_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
    with open(output_dir + '\\' +  question_name + '.json', 'w') as fp:
        json.dump(qa, fp)

if __name__ == "__main__":
    args = parse_args()
    try:  
        pdf_file = args.input
        
        pages = parse_pdf(pdf_file)
        parse_pages(pages, args.output)

        print("SUCCESS: scraping complete")
    except Exception as e:
        print(e)
     