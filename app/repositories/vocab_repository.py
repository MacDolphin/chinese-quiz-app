# Repository for vocabulary data access
# 生字資料存取層

import csv
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
import streamlit as st

from app.core import config
from app.models.vocabulary import VocabItem, MistakeItem

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quiz_app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def load_vocabulary(filename: str) -> List[VocabItem]:
    """
    載入生字檔案 (CSV)。
    Load vocabulary file (CSV).

    Args:
        filename: CSV file path

    Returns:
        List of unique VocabItem
    """
    vocab_dict: Dict[str, VocabItem] = {}
    
    if not os.path.exists(filename):
        logging.warning(f"File not found: {filename}")
        return []

    try:
        with open(filename, mode='r', encoding=config.ENCODING_TYPE) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 去除前後空白
                clean_row = {k: v.strip() for k, v in row.items() if k and v}
                
                # 確保有 char 和 zhuyin 欄位
                if 'char' in clean_row and 'zhuyin' in clean_row:
                    vocab_dict[clean_row['char']] = {
                        'char': clean_row['char'],
                        'zhuyin': clean_row['zhuyin'],
                        'book': clean_row.get('book', '未分類')
                    }
        
        return list(vocab_dict.values())
        
    except Exception as e:
        logging.error(f"Error loading {filename}: {e}")
        st.error(f"❌ 讀取檔案 {filename} 時發生錯誤: {e}")
        return []

def log_mistake(word_data: VocabItem) -> None:
    """
    將答錯的題目寫入錯題本。
    Log mistaken word to file.

    Args:
        word_data: The vocabulary item that was answered incorrectly
    """
    file_exists = os.path.isfile(config.ERROR_LOG_FILE)
    
    try:
        with open(config.ERROR_LOG_FILE, mode='a', newline='', encoding=config.ENCODING_TYPE) as f:
            fieldnames = ['char', 'zhuyin', 'timestamp']
            # 說明：使用 extrasaction='ignore' 避免因為 word_data 包含 'book' 而報錯
            # Description: Use extrasaction='ignore' to prevent errors when word_data contains 'book'
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'char': word_data['char'],
                'zhuyin': word_data['zhuyin'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
    except Exception as e:
        logging.error(f"Error logging mistake: {e}")
        st.error("❌ 錯題記錄失敗，請檢查檔案權限")

def remove_mistake_from_file(target: VocabItem) -> None:
    """
    從錯題本檔案中移除答對的字。
    Remove corrected word from mistake file.
    """
    if not os.path.exists(config.ERROR_LOG_FILE):
        return

    try:
        # 讀取現有錯題
        rows = []
        with open(config.ERROR_LOG_FILE, mode='r', encoding=config.ENCODING_TYPE) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['char'] != target['char']:
                    rows.append(row)
        
        # 寫回檔案
        with open(config.ERROR_LOG_FILE, mode='w', encoding=config.ENCODING_TYPE, newline='') as csvfile:
            # 說明：包含 timestamp 以避免 DictWriter 因為多出欄位而報錯
            # Description: Include timestamp to prevent DictWriter from erroring on extra fields
            fieldnames = ['char', 'zhuyin', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
            
    except Exception as e:
        logging.error(f"Error removing mistake {target['char']}: {e}")
        # 說明：這裡不再直接呼叫 st.error，由 UI 層決定如何顯示
        # Description: Avoid calling st.error directly here to keep repository clean
        raise e

def save_mistakes_cache(cache: List[VocabItem]) -> None:
    """
    將錯題本快取整批寫回檔案。
    Save mistake cache to file in batch.
    """
    try:
        with open(config.ERROR_LOG_FILE, mode='w', encoding=config.ENCODING_TYPE, newline='') as csvfile:
            fieldnames = ['char', 'zhuyin', 'timestamp']
            # 說明：加入 extrasaction='ignore' 避免 DictWriter 因為多出欄位而報錯
            # Description: Add extrasaction='ignore' to prevent errors on extra fields
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for mistake in cache:
                writer.writerow({
                    'char': mistake['char'],
                    'zhuyin': mistake['zhuyin'],
                    'timestamp': mistake.get('timestamp', '')
                })
        logging.info(f"Mistakes saved: {len(cache)} items")
    except Exception as e:
        logging.error(f"Error saving mistakes: {e}")
        st.error("❌ 儲存錯題本失敗")
