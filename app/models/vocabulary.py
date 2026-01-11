# Data models for the application
# 應用程式資料模型

from typing import TypedDict, Optional

# 說明：定義生字本的資料結構
# Description: Define the data structure for vocabulary items
class VocabItem(TypedDict):
    char: str
    zhuyin: str
    book: str

# 說明：定義錯題本的資料結構 (繼承 VocabItem，未來可擴充 timestamp 等欄位)
# Description: Define data structure for mistake items (inherits from VocabItem)
class MistakeItem(VocabItem):
    timestamp: Optional[str]

# 說明：定義記憶卡片的資料結構
# Description: Define the data structure for memory game cards
class MemoryCard(TypedDict):
    id: int
    content: str
    type: str          # 'char' or 'zhuyin'
    pair_id: int
    is_matched: bool
    is_flipped: bool
