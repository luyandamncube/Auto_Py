import PyPDF2 
import sys 
import os 
import argparse
import json
import string
import random
import re
import platform

if (platform.system() == 'Windows' ):
    escapeCharacter = '\\' 
else:
    escapeCharacter = '//' 


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
    if ('885CB989129A5F974833949052CFB2F2' in line):
        line = line.replace("885CB989129A5F974833949052CFB2F2","")   
    if ('IT Exam Dumps' in line):
        line = line.replace("IT Exam Dumps","")   
    if ('Learn Anything' in line):
            line = line.replace("Learn Anything","")  
    if ('VCEup' in line):
            line = line.replace("VCEup","")  
    if (' | ' in line):
            line = line.replace(" | ","")  
    
    if ('\u2013 ' in line):
            line = line.replace("\u2013 ","")  

    if ('Section:' in line):
        line = line.replace("Section: [none]","")
        line = line.replace("Section: (none)","")
    if ('References:' in line):
        line = '\n' + line + '\n'
    if ('A.' in line or 'B.' in line  or 'C.' in line or 'D.' in line or 'E.' in line or 'F.' in line):
        line = '\n' + line
    if ('HOTSPOT' in line or 'SIMULATION' in line  or 'DRAG DROP'):
        line = line + '\n'
    return (line)

def parse_qa(question, answer):
    dict_ = {}
    
    # | VCEup. com

    if ('Note: ' in question):
        question = question.replace("Use the following login credentials as needed:Azure Username: xxxxxAzure Password: xxxxxThe following information is for technical support purposes only:Lab Instance:","")
        question = question.replace("Note: This question is part of a series of questions that present the same scenario. Each question in the series contains a unique solution that mightmeet the stated goals. Some question","")
        question = question.replace("sets might have more than one correct solution, while others might not have a correct solution.After you answer a question in this ","")
        question = question.replace(" scenario, ","")
        question = question.replace("s section, ","")
        question = question.replace("you will NOT be able to return to it. As a result, these questions will not appear in the review screen.","")
        question = question.replace("Note: This question is a part of series of questions that present the same scenario. Each question in the series contains a unique solution. Determinewhether the solution meets the stated goals.","") 
        # print(question)
    rx = r"\.(?=\S)"
    dict_['question'] = re.sub(rx, ". ", question)

    if ('Correct Answer:' in answer):
        answer = answer.replace("Correct Answer: ","")

    description_ = ""
    description = answer.splitlines()
    
    dict_['answer'] = re.sub(rx, ". ", description[0])
    for i in range(2, len(description)):  
        description_ = description_ + description[i]

    dict_['description'] = re.sub(rx, ". ", description_)
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
    with open(output_dir + escapeCharacter +  question_name + '.json', 'w') as fp:
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
     