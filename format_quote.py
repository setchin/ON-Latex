fp = "Reading/reading-4.tex"
file = open(fp, encoding='utf-8')
str = file.read()
new_str = ""
cnt = 0
for ch in str:
    if ch == '"':
        cnt += 1
        if cnt % 2 == 1:
            new_str += '``'
            continue
    new_str += ch
file.close()

with open(fp, 'w', encoding='utf-8') as f:
    f.write(new_str)
