import sys
import os

class FileSearch:

    @staticmethod
    def search(query, target_dir='/home/keith/Digital_alexandria'):
        results = []
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if query.lower() in file.lower():
                    results.append(os.path.join(root, file))
        if results:
            for i, result in enumerate(results):
                data  = result.split("/")[4:]
                print(i+1, ": ", end='')
                for section in data[:-1]:
                    print(section, ": ", end='')
                print(data[-1])
                #if len(data) < 3:
                 #   print(i+1, " : ", data[0], " : ", data[1])
                #else:
                 #   print(i+1, " : ", data[0],  ":" , data[1],  ":", data[2])
            choice = input('Enter choice: ')
            choice = results[int(choice)-1]
            return choice
        return None


