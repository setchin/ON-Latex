import re
with open('./word/out.tex', encoding="utf8") as f:
    lines = f.readlines()

longtable_start = []
longtable_end = []
for i, line in enumerate(lines):
    if line.startswith('\\begin{longtable}'):
        longtable_start.append(i)
    if line.startswith('\\end{longtable}'):
        longtable_end.append(i)
new_lines = []
last_end = 0
for begin, end in zip(longtable_start, longtable_end):
    contents = "".join(lines[begin:end+1])
    # process headers

    # find first contents between []{@{} and @{}}
    pattern = re.compile(r'(?<=\[\]\{@\{\}).*?(?=@\{\})', re.DOTALL)
    match = pattern.search(contents)
    # count number of columns
    num_cols = match.group(0).count('>')
    # replace []{@{} ... @{}} with {l...l}
    contents = pattern.sub('l'*num_cols, contents)

    # find "[]{}" in \begin{longtable}[]{}
    pattern = re.compile(
        r'(?<=\\begin{longtable})\[\]\{@\{\}.*?(@\{\}\})', re.DOTALL)
    match = pattern.search(contents)
    # replace []{@{} ... @{}} with {l...l}
    contents = pattern.sub('{'+'l'*num_cols+'}', contents)

    contents = contents.replace("\\noalign{}", "")
    contents = contents.replace("\\endlastfoot", "\\endfoot")

    # find the content between \toprule and \midrule which contains \multicolumn{num}{text}
    # replace text with l*num
    pattern = re.compile(r'(?<=\\toprule\n).*(?=\\midrule)', re.DOTALL)
    match = pattern.search(contents)
    if match:
        match_text = match.group(0)
        match_text_copy = match_text
        # remove all the \n except the last one
        match_text = match_text.replace("\n", "", match_text.count("\n")-1)
        # remove all the \begin{minipage}[b]{\linewidth}\raggedright
        match_text = match_text.replace(
            "\\begin{minipage}[b]{\\linewidth}\\raggedright", "")
        # remove all the \end{minipage}
        match_text = match_text.replace("\\end{minipage}", "")

        # check if there is \multicolumn
        multi_col_pattern = re.compile(
            r'(?<=\\multicolumn\{\d\}\{).*?(?=\}\{)')
        multi_col_match = re.findall(multi_col_pattern, match_text)
        if multi_col_match:
            for _ in multi_col_match:
                match_text = match_text.replace(_, "c")
        match_text = match_text.replace("%", "")
        contents = contents.replace(match_text_copy, match_text)

    new_lines.extend(lines[last_end:begin]+contents.splitlines(True))
    last_end = end+1

with open('./word/out_new.tex', 'w', encoding="utf8") as f:
    f.writelines(new_lines)
