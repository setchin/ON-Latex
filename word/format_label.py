
import re
with open('./word/out.tex', encoding="utf8") as f:
    lines = f.readlines()

label_dict={}
for i, line in enumerate(lines):
    if line.find("\\label{")!=-1:
        pattern = re.compile(r'(?<=\\label\{).*?(?=\})')
        label_id=pattern.search(line).group(0)

        # try to find if there is a section heading in the same line
        # if so, use the section heading as the label
        # if not, use the label_id as the label
        sec_pattern = re.compile(r'(?<=section\{).*?(?=\})')
        sec_name=sec_pattern.search(line)
        if sec_name:
            label_dict[label_id]=sec_name.group(0)
        else:
            label_dict[label_id]=label_id
            print("Warning: label {} on line {} has no section heading".format(label_id,i))

# replace all \hyperref[id]{text} with \ref{id}
new_lines=[]
for i, line in enumerate(lines):
    pattern = re.compile(r'\\hyperref\[.*\]\{.*\}')
    matches = pattern.findall(line)
    if matches:
        for match in matches:
            # extract label
            label=match[match.index("[")+1:match.index("]")]
            if label in label_dict:
                line=line.replace(match,"\\ref{"+label_dict[label]+"}")
            else:
                print("Warning: label {} on line {} not found".format(label,i))
    new_lines.append(line)

new_lines="".join(new_lines)
for key, val in label_dict.items():
    new_lines=new_lines.replace("\\label{"+key+"}","\\label{"+val+"}")

with open('./word/out_ref.tex', 'w', encoding="utf8") as f:
    f.write(new_lines)
                
