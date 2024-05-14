import os
import nbformat

def list_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if not filename.startswith('.'):
                files.append(os.path.join(root, filename))

    return files

def print_files(path, files):
    rootlen = len(path)
    out = ""
    for idx, file in enumerate(files):
        out += f"{idx + 1}. {file[rootlen:]}\n"

    return out

def get_content(path, files):
    rootlen = len(path)
    content = []
    for file in files:
        if file.endswith(".csv"):
            f = open(file)
            data = f"## {file[rootlen:]}\n\n{f.readline()}"
            f.close()
            content.append(data)
        elif file.endswith(".ipynb"):
            f = open(file)
            nb = nbformat.read(f, as_version=4) 
            py_code = ""
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    py_code += cell.source + '\n\n'
            
            data = f"## {file[rootlen:]}\n\n{py_code}"
            content.append(data)
        else:
            f = open(file)
            data = f"## {file[rootlen:]}\n\n{f.read()}"
            f.close()
            content.append(data)

    return content

def get_report():
    f = open("report.tex", "r")
    report = f.read()
    f.close()

    report = "## Report.tex :\n" + report + "\n\n" 
    return report


if __name__ == "__main__":
    path = input("Enter directory path for the code: ")
    files = list_files(path)

    names = print_files(path, files)
    print(names)

    content = get_content(path, files)

    report = get_report()

    task = '''Based on the input files provided and the Latex document for the Report, Create a latex report in the specified format and fill in all the necessary details as needed from the code. Output the content of the `.tex` file. User proper LaTex syntax for all the text. For the bullet points use:
\\begin{itemize}
    \\item Point1
    \\item Point2
\\end{itemize}

IN A CODE BLOCK STRICTLY OUTPUT ONLY VALID LATEX CODE!! NO MARKDOWN IS ALLOWED !!

'''

    additional = input("Enter any additional information to keep in mind: ")

    prompt = "I have a made a project. Below are all the files of the project :\n" + names + "\n\n" + "The content of all the files is given below with the file name specified with `## ` User the file content to make a project report in the specified format.\n\n" + "\n\n".join(content) + "\n" + report + task + additional

    file = open("output.txt", "w")
    file.write(prompt)
    file.close()

