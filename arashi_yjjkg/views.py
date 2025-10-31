from django.shortcuts import render
from kanjiconv import KanjiConv
import markdown
import re

# kanjiconv のインスタンス生成
kanjiconv = KanjiConv(separator="", use_custom_readings=True)
kanjiconv.custom_readings = {
    "compound": {"四字": "よじ", "津津": "つつ", "津々": "つつ"}
}

def index(request):
    result = ""
    if request.method == "POST":
        yjjkg = request.POST.get("yjjkg", "").strip()  # 入力取得
        # 入力の先頭・末尾空白を取り、内部の空白も除去（必要なら）
        normalized = re.sub(r'\s+', '', yjjkg)

        # 「純粋に漢字（と々）だけでちょうど4文字」かを先に判定する
        # ^[\u4E00-\u9FFF々]{4}$ は「漢字または々 がちょうど4文字並んでいる」ことを意味する
        if normalized.lower() in ["banana", "バナナ"]:
            result = '''
<b>バ～ナ～ナ🍌 ナナナナ🍌 ナナ～ナ～ナ～ナ🍌<br>
バ～ナ🍌 ナナナナ🍌 ナナ～ナ～🍌<br>
バ～ナ～ナ🍌 ナナナナ🍌 ナナ～ナ～ナ～ナ🍌<br>
バ～ナ🍌 ナナナナ～🍌<br>
<br>目まぐるしく回る <span class="banana">🍌</span></b>
'''
        elif not re.match(r'^[\u4E00-\u9FFF々]{4}$', normalized):
            # 漢字4字の厳密一致でない場合は四字熟語ではない
            result = markdown.markdown("## This phrase is not 四字熟語")
        else:
            # ここでは normalized が漢字/々 のみでちょうど4文字である保証がある
            # 「々」を展開して実際の漢字列を作る（読み変換のため）
            expanded = re.sub(r'(.)々', r'\1\1', normalized)
            kanji_chars = re.findall(r'[\u4E00-\u9FFF]', expanded)

            # モーラ判定（先頭2文字の読みが2モーラかどうか）
            def is_two_mora(yojijukugo_head2):
                hiragana = kanjiconv.to_hiragana(yojijukugo_head2)
                mora_count = 0
                i = 0
                while i < len(hiragana):
                    # 小書き仮名が続く場合は1モーラとして扱う
                    if i + 1 < len(hiragana) and hiragana[i + 1] in "ぁぃぅぇぉゃゅょ":
                        mora_count += 1
                        i += 2
                    else:
                        mora_count += 1
                        i += 1
                return mora_count == 2

            # 先頭2文字（展開後）を渡す
            first_niji = normalized[:2]
            last_niji = normalized[2:]
            first_sanji = normalized[:3]

            if is_two_mora(first_niji):
                # Markdown で歌詞を作成し HTML に変換
                lyrics_md = f'''
### {first_niji}{last_niji}... 
### {first_niji}{last_niji}...
### {first_niji} {first_niji} {last_niji}...
### {first_sanji}ｵｫﾝ!!
### let's get on!!
## はじけりゃYeah!　素直にGood!　だからちょいと重いのはBoo!
## That's alright　それでも時代を極める　そうさボクらは Super Boy!
## We are "COOL"　やな事あってもどっかでカッコつける
## やるだけやるけどいいでしょ?　夢だけ持ったっていいでしょ?
# You are my SOUL! SOUL!　いつもすぐそばにある♪
# ゆずれないよ♪　誰もじゃまできない♪
# 体中に風を集めて♪　巻きおこせ♪
# A·RA·SHI♪　A·RA·SHI♪　for dream♪
'''
                result = markdown.markdown(lyrics_md)
            else:
                result = markdown.markdown("## SORRY...\n### This phrase is not suitable for A・RA・SHI")

    return render(request, "arashi_yjjkg/index.html", {"result": result})
