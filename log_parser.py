import argparse
import re
import json




def parse_json(inp_filename, out_filename):
    #list to store elements from each log line
    log_elements = []
    with open(inp_filename, 'r') as file:
        for line in file.readlines():
            #ignoring log lines without any entry or exit action
            if (line.find('ENTER') == -1 and line.find('EXIT') == -1):
                continue
            else:
                #element stores the 4 components of each log line
                element = dict()
                operation = re.search('](.+?):', line)
                if operation:
                    element['operation'] = operation.group(1)
                if (element['operation'] == 'ENTER'):
                    element['operation'] = 'ENTRY'
                filename = re.search(':\s+(.+?):', line)
                if filename:
                    element['filename'] = filename.group(1)
                line_no = re.search('.go:(.+?)\s+', line)
                if line_no:
                    element['line number'] = line_no.group(1)
                name = line.split(" ")
                element['name'] = name[len(name) - 1].strip()
                if (element['name'].isdigit()):
                    element['name'] = 'anonymous'
                log_elements.append(element)

    #create json string from the list
    jsonString = json.dumps(log_elements)
    json_object = json.loads(jsonString)

    json_formatted_str = json.dumps(json_object, indent=2)

    print(json_formatted_str)
    with open(out_filename, 'w') as outfile:
        json.dump(jsonString, outfile)




if __name__ == '__main__':
    #main class
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=None, help="Input file name")
    parser.add_argument("-o", "--output", type=str, help="Output file name")
    args = parser.parse_args()

    outFileName = args.output

    #calling parse json function
    parse_json(args.input, args.output)