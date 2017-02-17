import os
from datetime import datetime, date
from os import walk
import sys
import csv


def count_types(global_type_counter,file_type_counter,_type,index ,col):
    #if the column does not exis create it
    if(len(file_type_counter)<index+1):
        file_type_counter.insert(index,{_type:0})
    if(len(global_type_counter)<index+1):
        global_type_counter.insert(index,{_type:0})
        
    #if the column exist add to the type or add the type
    if(_type in file_type_counter[index]):
        file_type_counter[index][_type] += 1
    else:
        file_type_counter[index][_type] = 1
    if(_type in global_type_counter[index]):    
        global_type_counter[index][_type] += 1
    else:
        global_type_counter[index][_type] = 1

# def report(global_type_counter):
def report(list_file_counter,global_type_counter, file_names, output_file, header):
    report_file = open(output_file,"w")
    report_file.write("---------------------------------------- \n")
    report_file.write("GLOBAL STATS: \n")
    for i,pos in enumerate(global_type_counter):
        total = 0
        if(header != None and len(header)>i):
            report_file.write("Coluna: "+str(i)+' '+header[i]+'\n')
        else:
            report_file.write("Coluna: "+str(i)+'\n')
        for key, value in global_type_counter[i].items():
            total += value
        for key, value in global_type_counter[i].items():
            # report_file.write("  "+"Type: "+ key+ " Pecentage: "+ str(round(value/total,2))+ " Total: "+ str(total)+' \n')
            report_file.write("  "+"Tipo: "+ key+ " Porcentagem: "+ str(round(value/total,3))+' \n')
    for index,position in enumerate(list_file_counter):
        report_file.write("---------------------------------------- \n")
        report_file.write("FILE: "+file_names[index]+' \n')
        for col,_file in enumerate(list_file_counter[index]):
            total = 0
            if(header != None and len(header)>col):
                report_file.write("Coluna: "+str(col)+' '+header[col]+'\n')
            else:
                report_file.write("Coluna: "+str(col)+'\n')
            for key, value in _file.items():
                total += value
            for key, value in _file.items():
                report_file.write("  "+"Tipo: "+key+ " Porcentagem: "+str(round(value/total,3)) + ' \n')

def process(list_file_counter, global_type_counter, file_names, dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            file_type_counter = []
            print("file:", name)
            file_names.append(name)
            with open(dir_path+name) as csvfile:
                data_reader = csv.reader(csvfile, delimiter=';')
                count = 0
                for line in data_reader:
                    if(count%50000 == 0):
                        print(count)
                    count = count + 1
                    for index,col in enumerate(line):
                        # try:
                        #     col = datetime.strptime(col,'%Y%m%d')
                        #     # print(col)
                        #     count_types(file_type_counter, "date", index, col)
                        #     continue
                        # except:
                        #     pass
                        
                        try:
                            col = int(col)
                            count_types(global_type_counter,file_type_counter, "int", index, col)
                            continue
                        except:
                            pass
                        if(col != ''):
                            count_types(global_type_counter,file_type_counter, "string", index, col)
                        else:
                            count_types(global_type_counter,file_type_counter, "na", index, col)
                        
                print('Lines:', count)
        # print(file_type_counter)
            list_file_counter.append(file_type_counter)
    print(global_type_counter)
    print(len(global_type_counter))
    # for i in range(7):
    #     print(len(list_file_counter[i]))
            
    
def main(argv):
    if(len(argv) <= 1):
        print("Usage: csv_stats.py directory_path report_path [header_file_path]")
        return
    
    header = None
    #get the header file path if exists
    if(len(argv) > 2):
       header_file = argv[2]
       print(header_file)
       with open(header_file) as csvfile:
            data_reader = csv.reader(csvfile, delimiter=',')
            header = next(data_reader)
            # print(header)
            
            
    # global counter for all columns of the CSVs in the directory
    global_type_counter = []
    # list with lists of the column type counter
    list_file_counter = []
    count = 0
    # get the directory 
    dir_path = argv[0]
    
    output_file = argv[1]
    
    file_names = []
    process(list_file_counter, global_type_counter, file_names, dir_path)
    report(list_file_counter, global_type_counter, file_names, output_file, header)
                        
if __name__ == "__main__":
    main(sys.argv[1:])

