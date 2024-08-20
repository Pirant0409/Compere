import os

def find_results(student_directory):
    """Recursively search for 'results.txt' file in student directories."""
    for root, dirs, files in os.walk(student_directory):
        if "results.txt" in files or "NewResults.txt" in files:
            if "results.txt" in files:
                results_txt_path = os.path.join(root, "results.txt")
            elif "NewResults.txt" in files:
                results_txt_path = os.path.join(root,"NewResults.txt")
            print("Found 'results.txt' in:", results_txt_path)
            # Process 'results.txt' file here as needed
            with open(results_txt_path,"r") as f:
                lines = f.readlines()
            lineGet = False
            for line in lines:
                if "Mutation score" in line:
                    lineGet = True
                    mutation_score = line.split(":")[2]
                    mutation_score = mutation_score.split("(")[0]
                    with open ("mutationsScores.txt",'a') as f:
                        f.write(str(root)+":"+mutation_score+"\n")
                    print(root)
            if lineGet == False:
                with open ("mutationsScores.txt",'a') as f:
                    f.write(str(root)+":+0,00% (0,00%)\n")
                print(root)

def sort_mutation_score():
    with open("mutationsScores.txt", "r") as f:
        lines = f.readlines()

    # Parse the lines and extract the percentages
    student_percentages = []
    for line in lines:
        parts = line.strip().split(":")
        name = parts[0].strip()
        percentage = float(parts[1].strip().split("%")[0].replace(",", "."))
        student_percentages.append((name, percentage))

    # Sort the student percentages based on the percentage in descending order
    sorted_percentages = sorted(student_percentages, key=lambda x: x[1], reverse=True)

    # Print the sorted lines
    sorted_students = []
    for name, percentage in sorted_percentages:
        sorted_students.append(f"{name}: {percentage:.2f}%\n")
    with open("mutationScores_sorted.txt","w") as f:
        f.writelines(sorted_students)


def split_in_groups():
    with open("mutationScores_sorted.txt", "r") as f:
        lines = f.readlines()
    odd = False
    for line in lines:
        if not odd:
            with open("group1.txt","a") as f:
                f.write(line)
            odd = True
        else:
            with open("group2.txt","a") as f:
                f.write(line)
            odd = False

def main():
    for student_directory in os.listdir("students"):
        student_full_path = os.path.join("students", student_directory)
        if os.path.isdir(student_full_path):
            find_results(student_full_path)
    sort_mutation_score()
    split_in_groups()

main()