import random
import csv
import os
from datetime import datetime

# ==========================================
# 設定區
# ==========================================
VOCAB_FILE = 'vocabulary.csv'      # 主要題庫
ERROR_LOG_FILE = 'review_list.csv' # 錯題紀錄
ENCODING_TYPE = 'utf-8-sig'        # 編碼設定

# 正向回饋語句庫
praises = ["太棒了！🎉", "完全正確！🌟", "你真厲害！💪", "水啦！答對了！✨", "Excellent!", "你是漢字小天才！🎓"]

# ==========================================
# 資料處理函式
# ==========================================

def load_vocabulary(filename):
    """
    通用讀取函式：可以讀取題庫，也可以讀取錯題本。
    回傳一個不重複的生字列表。
    """
    vocab_dict = {} # 使用字典來去除重複 (key=char)
    
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, mode='r', encoding=ENCODING_TYPE) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 去除前後空白
                clean_row = {k: v.strip() for k, v in row.items() if k and v}
                
                # 確保有 char 和 zhuyin 欄位
                if 'char' in clean_row and 'zhuyin' in clean_row:
                    # 使用 char 當作 key，這樣重複的字就會被覆蓋，達到去重效果
                    vocab_dict[clean_row['char']] = {
                        'char': clean_row['char'],
                        'zhuyin': clean_row['zhuyin']
                    }
        
        # 將字典轉回列表
        vocab_list = list(vocab_dict.values())
        return vocab_list
        
    except Exception as e:
        print(f"❌ 讀取檔案 {filename} 時發生錯誤: {e}")
        return []

def log_mistake(word_data):
    """將答錯的題目寫入錯題本"""
    file_exists = os.path.isfile(ERROR_LOG_FILE)
    
    try:
        with open(ERROR_LOG_FILE, mode='a', newline='', encoding=ENCODING_TYPE) as f:
            fieldnames = ['char', 'zhuyin', 'timestamp']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'char': word_data['char'],
                'zhuyin': word_data['zhuyin'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"   📝 [{word_data['char']}] 已加入複習清單！")
            
    except Exception as e:
        print(f"⚠️ 無法寫入錯題紀錄: {e}")

def get_question(db, mode):
    """產生題目與選項"""
    target = random.choice(db)
    options = [target]
    
    # 隨機選出錯誤選項 (干擾項)
    max_attempts = 100 
    attempts = 0
    while len(options) < 3 and attempts < max_attempts:
        distractor = random.choice(db)
        if distractor != target and distractor not in options:
            options.append(distractor)
        attempts += 1
    
    random.shuffle(options)
    return target, options

# ==========================================
# 遊戲主迴圈
# ==========================================
def play_quiz(vocabulary_db, mode_name):
    """
    vocabulary_db: 傳入要練習的生字列表
    mode_name: 顯示目前是什麼模式 (一般/複習)
    """
    
    # 資料檢查：至少要有 3 個字才能跑 3 選 1
    if len(vocabulary_db) < 3:
        print(f"\n⛔ {mode_name}的資料不足！")
        print("💡 原因：列表中的生字少於 3 個，無法產生干擾選項。")
        if mode_name == "錯題複習模式":
            print("👉 請先去「一般練習模式」多累積一點錯題吧！(誤)")
        else:
            print("👉 請在 CSV 檔案中至少輸入 3 組生字。")
        return

    print("===================================")
    print(f"正在進行：【 {mode_name} 】")
    print(f"總共有 {len(vocabulary_db)} 個生字在題庫中")
    print("輸入 'q' 可以隨時離開，回到主選單")
    print("===================================")

    while True:
        mode = random.choice([1, 2]) # 1=看字選注音, 2=看注音選字
        target, options = get_question(vocabulary_db, mode)
        
        # 顯示題目
        if mode == 1:
            question_text = f"請問 [{target['char']}] 的注音是什麼？"
            correct_ans_content = target['zhuyin']
        else:
            question_text = f"請問 [{target['zhuyin']}] 是哪個國字？"
            correct_ans_content = target['char']
            
        print(f"\n題目: {question_text}")
        
        # 顯示選項
        labels = ['A', 'B', 'C']
        correct_label = ""
        
        for i, opt in enumerate(options):
            content = opt['zhuyin'] if mode == 1 else opt['char']
            print(f"  {labels[i]}. {content}")
            if opt == target:
                correct_label = labels[i]

        user_input = input("請選擇 (A/B/C): ").upper().strip()

        if user_input == 'Q':
            print("\n🔙 結束練習。")
            break # 跳出 while 迴圈，結束 play_quiz，回到 main

        if user_input not in labels:
            print("⚠️ 請輸入 A, B 或 C 喔！")
            continue

        if user_input == correct_label:
            print(f"✅ {random.choice(praises)}")
        else:
            print(f"❌ 哎呀，正確答案是 {correct_label} ({correct_ans_content})。")
            log_mistake(target) # 無論哪種模式，答錯都記錄下來

# ==========================================
# 程式進入點 (Main Menu)
# ==========================================
def main():
    while True:
        print("\n###################################")
        print("   歡迎使用美洲華語生字小幫手 V3   ")
        print("###################################")
        print("1. 📖 一般練習模式 (從題庫出題)")
        print("2. 🔧 錯題複習模式 (專攻答錯的字)")
        print("0. 離開程式")
        
        choice = input("\n請選擇功能 (0-2): ").strip()
        
        if choice == '1':
            # 讀取主要題庫
            db = load_vocabulary(VOCAB_FILE)
            if not db:
                print("⚠️ 找不到題庫檔案，請確認 vocabulary.csv 存在。")
            else:
                play_quiz(db, "一般練習模式")
                
        elif choice == '2':
            # 讀取錯題紀錄
            if not os.path.exists(ERROR_LOG_FILE):
                print("\n⚠️ 目前還沒有錯題紀錄喔！請先進行一般練習。")
            else:
                db = load_vocabulary(ERROR_LOG_FILE)
                if db:
                    play_quiz(db, "錯題複習模式")
                else:
                    print("\n⚠️ 錯題檔案讀取失敗或內容為空。")
                    
        elif choice == '0':
            print("下次見！拜拜！👋")
            break
        else:
            print("無效的輸入，請重新選擇。")

if __name__ == "__main__":
    main()