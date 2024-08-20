import pandas as pd
import subprocess
import shutil, os
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)
from langchain_community.chat_models.huggingface import ChatHuggingFace
from getpass import getpass
from typing import Dict
from functools import partial


methodChecked = {}

# read the second line of the output.csv file and print it
def getAlivedMutants(path="details.csv"):
    print("GETTING ALIVE MUTANTS")
    alivedMutants = []

    df = pd.read_csv(path)
    num_lines = sum(1 for line in open(path))

    for i in range(num_lines-1):
        if str(df.iloc[i,1]) == "LIVE" or str(df.iloc[i,1]) == "UNCOV":
            alivedMutants.append(str(df.iloc[i,0]))

    print("alived/uncovered mutants:", alivedMutants)
    return alivedMutants


def getModuleInfo(alivedMutants):

    mutantsInfo = []
    print("GETTING MODULE INFO")
    for line in open('mutants.log'):
        if line.split(":")[0] in alivedMutants:
            mutantNumber = line.split(":")[0]
            classInfo =  line.split(":")[4]
            if "@" in classInfo:
                methodSignature= classInfo.split("@")[1]
                if "init" not in methodSignature:
                    methodName = methodSignature.split("(")[0]
                else :
                    methodName = classInfo.split("@")[0].split(".")[-1]
                if mutantNumber == "198":
                    print(methodName)
                className = classInfo.split("@")[0].split(".")[-1]+ ".java"
                if "|==>" in line.split(":")[6]:
                    codeSnipet = line.split(":")[6]
                else:
                    codeSnipet = line.split(":")[6] + line.split(":")[7]
                codeBefore = codeSnipet.split("|==> ")[0]
                codeAfter = line.split("|==> ")[1]
            elif os.path.exists("../MuTEd/SUT/2048/mutants/"+str(line.split(":")[0])) :
                "Mutant " + str(line.split(":")[0]) + " not a module"
                "Deleting mutant from ../MuTEd/SUT/2048/mutants/"
                #delete directory in ../MuTEd/SUT/2048/mutants/str(line.split(":")[0])
                shutil.rmtree("../MuTEd/SUT/2048/mutants/"+str(line.split(":")[0]))

            mutantsInfo.append([methodName, className,codeBefore, codeAfter,mutantNumber])
    return mutantsInfo

def setupQuerries(queryPath, className, methodName,mutantCounter, revert=False):
    print("SETTING UP QUERIES")

    if not os.path.exists("C:/Users/32491/Documents/Uni/MA2/Memoire/proto/queries/"+str(mutantCounter)+"/done.txt"):
            with open(queryPath, 'r') as file :
                filedata = file.read()
            # Replace the target string

            if not os.path.exists("C:/Users/32491/Documents/Uni/MA2/Memoire/proto/queries/"+str(mutantCounter)):
                os.mkdir("C:/Users/32491/Documents/Uni/MA2/Memoire/proto/queries/"+str(mutantCounter))
            with open("queries/"+str(mutantCounter)+"/processed.txt",'w') as f:
                f.write(filedata)
            if not revert :
                if not os.path.exists("C:/Users/32491/Documents/Uni/MA2/Memoire/proto/queries/"):
                    os.mkdir("C:/Users/32491/Documents/Uni/MA2/Memoire/proto/queries/")
                filedata = filedata.replace('$CLASS_NAME', className)
                filedata = filedata.replace('$METHOD_NAME', methodName)
                with open("queries/"+str(mutantCounter)+"/"+"getBody.ql", 'w') as f:
                    f.write(filedata)
            elif revert:
                filedata = filedata.replace(className, '$CLASS_NAME')
                filedata = filedata.replace(methodName, '$METHOD_NAME')



def getModulePath(dbPath, queryPath):

    print("GETTING MODULE PATH")
    results = {"sourcePath": "", "lineStart": "", "lineEnd": ""}
    print("RUNNING QUERY: ", queryPath)
    command = [
        "codeql",
        "query",
        "run",
        "--threads=8",
        "--database="+dbPath,
        queryPath
    ]

    result = subprocess.run(command, capture_output=True, text=True)   
    try:
        output = result.stdout.split("file://")[1]
        results["sourcePath"] = output.split(".java")[0]+".java"
        linesInfo = output.split(".java:")[1]
        results["lineStart"] = linesInfo.split(":")[0]
        results["lineEnd"] = linesInfo.split(":")[2]
    except:
        #append failed.txt
        print("QUERY FAILED")
        with open("failed.txt", 'a') as f:
            f.write(queryPath + "\n")
            f.write (str(result) + "\n")
            f.write (result.stdout + "\n")


    return results

def runQuerry():
    alivedMutants = getAlivedMutants()
    mutantsInfo = getModuleInfo(alivedMutants)
    for mutantInfo in mutantsInfo:
        worker(mutantInfo)

def worker(mutantInfo):
    templateQueriesPath = "../codeql-custom-queries-java/getBody.ql"
    mutantCounter = mutantInfo[4]
    queryPath = "queries/"+str(mutantCounter)+"/getBody.ql"
    if not os.path.exists("C:/Users/32491/Documents/Uni/MA2/Memoire/proto/queries/"+str(mutantCounter)):
        print("WORKER " + str(mutantCounter) + " INVOKED")
        methodName = mutantInfo[0]
        className = mutantInfo[1]
        lineBefore = mutantInfo[2]
        lineMutated = mutantInfo[3]
        setupQuerries(templateQueriesPath, className, methodName,mutantCounter, False)
        if methodName in methodChecked:
            results = methodChecked[methodName]
        else:
            results = getModulePath("./2048database", queryPath)
            methodChecked[methodName] = results
        if results["sourcePath"] == "":
            print("ERROR: NO SOURCE PATH FOUND")
            return
        else:
            moduleCode = getModuleCode(results["sourcePath"], results["lineStart"], results["lineEnd"])
            print("results :",results)
            callLLM(moduleCode, lineBefore, lineMutated, "queries/"+mutantCounter+"/"+methodName.split(".java")[0]+"_"+className+"_mutants"+str(mutantCounter) +".txt")
    else:
        print("WORKER " + str(mutantCounter) + " ALREADY INVOKED")

def getModuleCode(path,lineStart,lineEnd):
    file = open(path, 'r')

    content = file.readlines()

    moduleCode = content[int(lineStart)-1:int(lineEnd)]
    moduleCode = [line.replace("\t"," ").replace("\n","") for line in moduleCode]
    moduleCode = "\n".join(moduleCode)
    return moduleCode

def callLLM(codeSnipet,lineOriginal,lineMutated, outputPath):

    print("CALLING LLM")

    secondPrompt = "Act as an experimented senior program tester trying to educate CS3 students to test generation. I'm going to provide a java method along with a mutated line and it's corresponding line number. The mutant has been kept alive by some test suite. I want you to meticulously guide the student about how to generate a test suite that would kill this mutant.Do not simply explain how to kill this particular mutant, but generalize it to other mutants aswell.Don't EVER generate a code snippet.Don't EVER generate a test case.	"

    HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

    template = """System: {system}

    User: {input}
    Answer: Let's think step by step."""

    prompt = PromptTemplate.from_template(template)

    repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"


    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        **{
            "temperature": 0.2,
        },
    )
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    resp  = llm_chain.run(system=secondPrompt,input="method body : \n" + codeSnipet + "\n mutated line: " + lineMutated + "\n original line: " + lineOriginal)
    print(resp)


    print("EXPORTING RESPONSE TO : " + outputPath)
    with open(outputPath, 'w') as f:
        f.write(resp)


runQuerry()



