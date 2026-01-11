# Service for Game Logic
# 遊戲邏輯服務

import random
from typing import List, Dict, Tuple, Optional
from app.core import config
from app.models.vocabulary import VocabItem, MemoryCard

def get_question(db: List[VocabItem], full_db: Optional[List[VocabItem]]) -> Tuple[Optional[VocabItem], Optional[List[VocabItem]], Optional[int]]:
    """
    從題庫中隨機產生題目。
    Generate a random question from the database.
    
    Args:
        db: Current working database
        full_db: Full database for distractor generation
        
    Returns:
        (target, options, mode) tuple
    """
    if not db:
        return None, None, None

    target = random.choice(db)
    options = [target]
    
    # Randomly select distractors
    attempts = 0
    source_db = db
    
    # If current db is too small, use full_db for distractors
    if len(db) < config.NUM_OPTIONS and full_db and len(full_db) >= config.NUM_OPTIONS:
        source_db = full_db

    while len(options) < config.NUM_OPTIONS and attempts < config.MAX_DISTRACTOR_ATTEMPTS:
        distractor = random.choice(source_db)
        if distractor['char'] != target['char'] and distractor not in options:
            options.append(distractor)
        attempts += 1
    
    random.shuffle(options)
    
    # Mode: 1=Char->Zhuyin, 2=Zhuyin->Char
    mode = random.choice([1, 2]) 
    
    return target, options, mode

def init_memory_game_cards(db: List[VocabItem]) -> List[MemoryCard]:
    """
    初始化記憶配對遊戲卡片。
    Initialize memory game cards.
    """
    num_pairs = config.MEMORY_GAME_PAIRS
    
    if len(db) < num_pairs:
        selected_words = db
        # Optional: Duplicate if needed, but for now just use available
    else:
        selected_words = random.sample(db, num_pairs)
    
    cards: List[MemoryCard] = []
    for i, word in enumerate(selected_words):
        # Card 1: Char
        cards.append({
            'id': i * 2,
            'content': word['char'],
            'type': 'char',
            'pair_id': i,
            'is_matched': False,
            'is_flipped': False
        })
        # Card 2: Zhuyin
        cards.append({
            'id': i * 2 + 1,
            'content': word['zhuyin'],
            'type': 'zhuyin',
            'pair_id': i,
            'is_matched': False,
            'is_flipped': False
        })
    
    random.shuffle(cards)
    return cards

def check_memory_match(cards: List[MemoryCard], flipped_indices: List[int]) -> bool:
    """
    檢查兩張翻開的卡片是否配對。
    Check if two flipped cards match.
    """
    if len(flipped_indices) != 2:
        return False
        
    idx1, idx2 = flipped_indices
    card1 = cards[idx1]
    card2 = cards[idx2]
    
    return card1['pair_id'] == card2['pair_id']
