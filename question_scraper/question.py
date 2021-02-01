import sys 
import os 
import argparse
import json 
import random

def parse_args():
    parser = argparse.ArgumentParser(description='JSON question bank reader')
    parser.add_argument('-i',
                       '--input',
                       required=True,
                       help='Input Directory')
    
    args = parser.parse_args()

    if (os.path.isfile(args.input) == True):
        print(f"ERROR: -i is not a directory")
        exit()

    return parser.parse_args()

def parse_files(input_dir): 
    num_questions = 0
    questions = []
    hotspot_questions = []
    drag_questions = []
    sim_questions = []
    points_total = 0
    for json_question in os.listdir(input_dir):
        if json_question.endswith(".json"): 
            num_questions += 1 
            with open(input_dir+'\\'+json_question) as json_file:
                data = json.load(json_file)
            if ('HOTSPOT' in data['question']):
                hotspot_questions.append(json_question)
            elif ('DRAG DROP' in data['question']):
                drag_questions.append(json_question)
            elif ('SIMULATION' in data['question']):
                sim_questions.append(json_question)
                # SIMULATION
            else:
                questions.append(json_question)
                points_total += len(data['answer'])
                # print(f'{points_total} {data["answer"]}')
            # print('=====================================================')
    # print('Start questions ')
    # print(f'No of questions {num_questions}')
    # print(f'hotspot questions {hotspot_questions}')
    # print(f'drag and drop questions {drag_questions}')
    # invalid_questions = hotspot_questions + drag_questions
    return(points_total,questions)

def questioner(questions,input_dir):
    total = len(questions)
    mark = 0
    print(f'No of questions {total}\n')
    random.shuffle(questions)
    for index, question in enumerate(questions):
        with open(input_dir+'\\'+question) as json_file:
            data = json.load(json_file)
            print(f'{index} of {total} ----------------------------------------------------------------')
            print(data['question'])
        try:
            value = input("Your answer:\n").upper()
            matched_characters = len(set(value) & set(data['answer']))
            # print(f'MATCHED:  {matched_characters}')
            if (matched_characters > 0):
                print(f'CORRECT: {data["answer"]}\n')
                mark += matched_characters
            else:
                print(f'WRONG: {data["answer"]}\n')
            print(data["description"]+ '\n')
        except KeyboardInterrupt:
            return (mark)
    return (mark)

if __name__ == "__main__":
    args = parse_args()
    try:
        print('Loading questions')
        points_total, questions = parse_files(args.input)
        print('Beginning quiz')
        mark = questioner(questions, args.input)
        final = (mark/points_total) * 100 
        print('=================================================================')
        print(f'{mark} out of {points_total}')
        print(f'Your mark: {final}')

    except KeyboardInterrupt as e:
        print(e)
     