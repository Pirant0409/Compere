import os
import zipfile
import tarfile
import shutil

def extract_archive(file_path, extract_to):
    """Extracts an archive file to a given directory."""
    print("extract ",file_path, " to ", extract_to )
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif file_path.endswith('.tar.gz'):
        with tarfile.open(file_path, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
    # You can add more conditions for other archive formats like .rar

def process_directory(directory,processedItem):
    """Recursively processes a directory."""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item_path not in processedItem:
            processedItem.append(item_path)
            if os.path.isfile(item_path):
                if item.endswith('.zip') or item.endswith('.tar.gz'):
                    if item.endswith(".zip"):
                        extractTo = os.path.abspath(item_path.split(".zip")[0]+"/..")
                    elif item.endswith(".tar.gz"):
                        extractTo = os.path.abspath(item_path.split(".tar.gz")[0]+"/..")
                    extract_archive(item_path, extractTo)
                    process_directory(extractTo,processedItem)
                    if os.path.exists(item_path):
                        os.remove(item_path)
                elif "results.txt" in item.lower() or "newresults.txt" in item.lower():
                    with open(item_path, "r") as f:
                        lines = f.readlines()
                    linesToWrite = []
                    found_analysis = False
                    get_next_line = False
                    if len(lines) > 0 and lines[0]!= "ok":
                        linesToWrite.append("ok")
                        for i in range(len(lines)):
                            line = lines[i]
                            if get_next_line:
                                linesToWrite.append(line)
                                get_next_line = False
                            if "Mutants retained: 252" in line:
                                get_next_line = True
                            if "Summary:" in line:
                                found_analysis = True
                            if found_analysis:
                                if "------------------------------------------------------------" in line:
                                    break
                                linesToWrite.append(line)
                        with open(item_path, "w") as f:
                            f.writelines(linesToWrite)
                else:
                    with open("./resultsNotFound.txt","a") as f:
                        f.write(str(item)+"\n")
            elif os.path.isdir(item_path):
                current_name = item_path.split("/")[-1]
                new_path = item_path
                new_name = current_name
                if "assignsubmission" in current_name and "_" in current_name and "MACOSX" not in current_name:
                    new_name = current_name.split("_")[0]
                    new_path = os.path.abspath(item_path+"/..")
                    new_path = new_path+"/"+new_name
                    os.rename(item_path,new_path)
                process_directory(new_path,processedItem)
            

def delete_dubles(path):
    allDirs = os.listdir(path)
    existingDir = []
    allDirs.sort()
    print(allDirs)
    for i in range(len(allDirs)):
        if i == 0:
            existingDir.append(allDirs[i])
        elif allDirs[i] not in existingDir and str(allDirs[i-1]) not in str(allDirs[i]):
            existingDir.append(allDirs[i])
        else:
            print("deleting ", path+"/"+allDirs[i])
            shutil.rmtree(path+"/"+allDirs[i])


    
            
def main():
    start_directory = "students/"
    alreadyProcessed = []
    process_directory(start_directory,[])
    delete_dubles(start_directory)
    print("Extraction completed.")

main()
            