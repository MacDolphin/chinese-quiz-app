import csv
import os

VOCAB_FILE = 'vocabulary.csv'
TEMP_FILE = 'vocabulary_updated.csv'

# User provided list for Book 1
book1_chars_str = "一二三四五六七八九十百千上中下大小手力工又不左右有尖山火水土木林月天生日卡早也紅雲花雨白少多的石風沙明子足玩人來米沒田是我星在坐去肚和肉目舌牙耳心好正雪地竹你他看見哭笑叫唱走巴了比李刀位呀草象交朋友只校女男姓言立江禾這那哪"
book1_chars = set(book1_chars_str.replace("第一冊：", "").replace(" ", "").strip())

# User provided list for Book 2
book2_chars_str = "牛馬鳥魚名字媽兒分把又合朵想要青吃羊言請找黃就說爸可以怕午很太奶還包真個前門猜兩們都誰老哥弟問每給來送回家高過書快果開信河什麽入流海從到得里歌里新年春幾告訴冬外再知道只爬跑跳跟起蛙遊黑飛怎會妹長本如先拿共畫筆為才毛後話洞學愛同久出力貝進用住"
book2_chars = set(book2_chars_str.replace("第二冊：", "").replace(" ", "").strip())

# User provided list for Book 3
book3_chars_str = "王文許川半站寫咬表示收點事秋晚井只面亮掉拉最放擡頭興公豆種成玉等東西瓜南直現空期邊非常具動物洋世界美忘原食台北國電片衣記今絲巾金色買定路身穿比對能陽吹於冷熱累自己樂樣做飯氣完車帶全奇怪吋次像房囪窗戶方錢打元數存賣銀行謝眼鏡樓廚院客洗間椅桌發時候床平升落活城市農村場州民洲化亞"
book3_chars = set(book3_chars_str.replace("第三冊：", "").replace(" ", "").strip())

# User provided list for Book 4
book4_chars_str = "第考試張因法帽弓反式冒孝更照溫使運員充滿者永遠病願安樹感恩節參加喜歡各其英遊通抱著細虎錯認師答變胖而且忽然聲忍假餃皮冰箱菜湯煮鍋味忙幸香覺處聽夜機剪倒肥料首唐教聞但句念特別藥求醫神治餓麥品聽意思光糖閃極指靠近排球些顆清趣理古代取夏季舉已經始賽追緊舟油結軍祝向桃休息睡醒吵當連鬧音急便抓逃重"
book4_chars = set(book4_chars_str.replace("第四冊：", "").replace(" ", "").strip())

# User provided list for Book 5
book5_chars_str = "父母親班夠語論將展容易惜並影童注談整報紙視底之故此爺實任何肯功習萬聖園內服裝課扮嚇被紀應該布單主室詩霜背望彽鄉獎圖松采深難識題禮準備冊券超級造幫痛順作破廢效司部陪體剛類燒炒骨零幹面付推健康管辦短營迎參政府練投傳接隊網棒決專勇敢仗退兵受傷性官華讓件總統福雖觀歷博館科建印越史保祖留移選票量演趕由輪騎慢妖鬼消提步盡除需情改"
book5_chars = set(book5_chars_str.replace("第五冊：", "").replace(" ", "").strip())

# User provided list for Book 6
book6_chars_str = "導講義夾程規則換遲固座置貴號育必修另附度業腦利查資郵討按鍵昨盤驚軟拼技版社研究遍相費希暑般彈鋼琴鼓響團揮奏器免錄圍曲掌突拖眾呆暖途停努似例尺倍懂糟簡貪無章或楚達亡補牢讀夫角形較辛苦剩遇麻煩解兄財產商算乘減借計替墻堆烤塊轉碰嘴群彎漸卻互酸腿曾殺死領困協精豐富凡迷偶材施貼欲勿典尊敬稱呼翻譯關粉贈乎及助扇偉離危險終佛旅詳介紹區俗慣靈港岸船航"
book6_chars = set(book6_chars_str.replace("第六冊：", "").replace(" ", "").strip())

# User provided list for Book 7
book7_chars_str = "招待養喝漿餅醬蛋店含善務炸切雞西紅柿臭腐辣丸周陸播藝幕標繁偏旁概狀條周抽符普省漂況約既強掃占丟末舊貨售登負責杯瓶逛庫凈搬價折藍舍藏良護宇宙刻寶巖穴綠紫彩輕麗幹鉆士止戰爭頂災賞聯寄漢蒙苗族舞蹈插詞抄享吉祥娘壯峰驗斷嫁吸煙系敏毒系警禁臟肺血腎肝腸胃害癌癥鴉戒勸阻擔姨針診眠弱寒調增疫至飲適咳舒蒸梨熟副撞臂刺覆療束令派括餐鐵廣牌刊差濟往密尚議申評堅持環境"
book7_chars = set(book7_chars_str.replace("第七冊：", "").replace(" ", "").strip())

# User provided list for Book 8
book8_chars_str = "購珠鞋櫃扣寬閒扶架耐碎裙款制褲釘圓街撿宜值格袋鮮踢扯鈴拋溜範睛迫板繩圈蓋朝卷弄松基腳拍頁陰晴狂暴速降巨浪居滑坡閉局預創際廟拜慶燈篇隨脫秀歐克致巧維命磅島藍硬甜酒異德氧辨集歲奮閱挺灰模糊腫壓潔梅獨盛征支根磨勁暗妙啟拔靜擦糕默沿橫貫繼續繞雇窮挖鋪勞怨段野夕載歸畢與戲供爆幼挑封注組碟姿劇池牽織搭橋召份聚訂"
book8_chars = set(book8_chars_str.replace("第八冊：", "").replace(" ", "").strip())

# User provided list for Book 9
book9_chars_str = "築薪雜寓租艙甚貿術婆銷制慮揚勤濃厚優缺列擇填績淚夥伴敞廳證檢簽托沈輸套頓腔忱朗聊禍延誤承委辯武喊初引庭竟尿炎噴鼻涕染嚴脾珍益募帳操防慰抗貢獻依項顧鹹陳椒胡采烈叔醋祭恭源守輩鹽堡攻渡據譜孫忠編婚誦限冠志否荒涼悔沮喪緒散悲佳襯寂寞暫淡弦序悠若帝宿舍遺控確躁剔潑羞幽焦憤怒疑察析亂榮競誠訓權損失"
book9_chars = set(book9_chars_str.replace("第九冊：", "").replace(" ", "").strip())

def update_vocabulary():
    if not os.path.exists(VOCAB_FILE):
        print(f"Error: {VOCAB_FILE} not found.")
        return

    updated_rows = []
    fieldnames = []

    with open(VOCAB_FILE, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        
        # Ensure 'book' is in fieldnames
        if 'book' not in fieldnames:
            fieldnames.append('book')

        for row in reader:
            char = row['char'].strip()
            
            # Determine book
            current_book = row.get('book', '未分類')
            
            # Priority: Book 1 > Book 2 > Book 3 (or whatever order makes sense if duplicates exist)
            # Usually a word appears first in Book 1, then maybe reviewed? 
            # But here we just want to tag them.
            
            if char in book1_chars:
                row['book'] = '第一冊'
            elif char in book2_chars:
                row['book'] = '第二冊'
            elif char in book3_chars:
                row['book'] = '第三冊'
            elif char in book4_chars:
                row['book'] = '第四冊'
            elif char in book5_chars:
                row['book'] = '第五冊'
            elif char in book6_chars:
                row['book'] = '第六冊'
            elif char in book7_chars:
                row['book'] = '第七冊'
            elif char in book8_chars:
                row['book'] = '第八冊'
            elif char in book9_chars:
                row['book'] = '第九冊'
            elif current_book == '未分類' or current_book is None:
                row['book'] = '未分類'
            
            updated_rows.append(row)

    # Write back
    with open(TEMP_FILE, mode='w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    os.replace(TEMP_FILE, VOCAB_FILE)
    print(f"Updated {len(updated_rows)} words.")
    print(f"Book 1: {len([r for r in updated_rows if r['book'] == '第一冊'])}")
    print(f"Book 2: {len([r for r in updated_rows if r['book'] == '第二冊'])}")
    print(f"Book 3: {len([r for r in updated_rows if r['book'] == '第三冊'])}")
    print(f"Book 4: {len([r for r in updated_rows if r['book'] == '第四冊'])}")
    print(f"Book 5: {len([r for r in updated_rows if r['book'] == '第五冊'])}")
    print(f"Book 6: {len([r for r in updated_rows if r['book'] == '第六冊'])}")
    print(f"Book 7: {len([r for r in updated_rows if r['book'] == '第七冊'])}")
    print(f"Book 8: {len([r for r in updated_rows if r['book'] == '第八冊'])}")
    print(f"Book 9: {len([r for r in updated_rows if r['book'] == '第九冊'])}")

if __name__ == "__main__":
    update_vocabulary()
