import csv
from pypinyin import pinyin, Style, load_phrases_dict

# Load the vocabulary file
filename = 'vocabulary.csv'
errors = []

try:
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        line_num = 1 # Header is line 1
        for row in reader:
            line_num += 1
            char = row['char'].strip()
            file_zhuyin = row['zhuyin'].strip()
            
            if not char or not file_zhuyin:
                continue

            # Get all possible zhuyin for the character
            # Style.BOPOMOFO returns standard zhuyin with tone marks
            possible_zhuyins_list = pinyin(char, style=Style.BOPOMOFO, heteronym=True)
            
            if not possible_zhuyins_list:
                errors.append(f"Line {line_num}: [{char}] - No pinyin found")
                continue
                
            # pinyin returns a list of lists (one list per character in the input string)
            # Since we expect single characters, we take the first item.
            possible_zhuyins = possible_zhuyins_list[0]
            
            # Normalize for comparison
            # 1. Handle neutral tone: pypinyin might use '˙' or nothing or space.
            #    The file uses '˙' at the end usually for light tone? No, looking at file:
            #    Line 22: 了,ㄌㄜ˙ (dot at end)
            #    Line 69: 個,ㄍㄜ˙
            #    pypinyin might put dot at start or end.
            
            match_found = False
            for py_zhuyin in possible_zhuyins:
                # Normalize both to compare
                # Remove spaces
                norm_file = file_zhuyin.replace(" ", "")
                norm_py = py_zhuyin.replace(" ", "")
                
                # Handle light tone dot position differences if any
                # Some systems use ˙ at start, some at end.
                if '˙' in norm_file:
                     norm_file = norm_file.replace('˙', '')
                     # If file has light tone, we expect pypinyin to have it too (or be neutral)
                
                if '˙' in norm_py:
                    norm_py = norm_py.replace('˙', '')

                if norm_file == norm_py:
                    match_found = True
                    break
            
            if not match_found:
                # Double check specific common variations or if it's just a different valid pronunciation
                # that pypinyin doesn't list by default (though heteronym=True should cover most)
                errors.append(f"Line {line_num}: [{char}] File says: {file_zhuyin} | Possible: {', '.join(possible_zhuyins)}")

    if errors:
        print(f"Found {len(errors)} potential mismatches:")
        for e in errors:
            print(e)
    else:
        print("No obvious mismatches found!")

except Exception as e:
    print(f"Error: {e}")
