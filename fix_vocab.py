import csv
import os

filename = 'vocabulary.csv'
temp_filename = 'vocabulary_fixed.csv'

# Define the fixes: char -> correct_zhuyin
fixes = {
    '冷': 'ㄌㄥˇ',
    '娘': 'ㄋㄧㄤˊ',
    '扯': 'ㄔㄜˇ',
    '拔': 'ㄅㄚˊ',
    '損': 'ㄙㄨㄣˇ',
    '擦': 'ㄘㄚ',
    '暫': 'ㄗㄢˋ',
    '租': 'ㄗㄨ',
    '聊': 'ㄌㄧㄠˊ',
    '腿': 'ㄊㄨㄟˇ',
    '衣': 'ㄧ',
    '速': 'ㄙㄨˋ',
    '骨': 'ㄍㄨˇ',
    '麼': 'ㄇㄜ˙'
}

try:
    with open(filename, mode='r', encoding='utf-8-sig') as infile, \
         open(temp_filename, mode='w', encoding='utf-8-sig', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        count = 0
        for row in reader:
            char = row['char'].strip()
            if char in fixes:
                row['zhuyin'] = fixes[char]
                count += 1
            writer.writerow(row)
            
    # Replace original file
    os.replace(temp_filename, filename)
    print(f"Successfully fixed {count} errors.")

except Exception as e:
    print(f"Error: {e}")
