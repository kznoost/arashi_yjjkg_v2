from django.shortcuts import render
from kanjiconv import KanjiConv
import markdown

# kanjiconvのインスタンス生成
kanjiconv = KanjiConv(separator="", use_custom_readings=True)

# 辞書のカスタム読み
kanjiconv.custom_readings = {
    "compound": {"四字": "よじ", "津津": "つつ", "津々": "つつ"}
}

def index(request):
    result = ""
    if request.method == "POST":
        yjjkg = request.POST.get("yjjkg", "").strip()

        # BANANAモード
        if yjjkg.lower() in ["banana", "バナナ"]:
            result = '''
            <b>バ～ナ～ナ🍌 ナナナナ🍌 ナナ～ナ～ナ～ナ🍌<br>
            バ～ナ🍌 ナナナナ🍌 ナナ～ナ～🍌<br>
            バ～ナ～ナ🍌 ナナナナ🍌 ナナ～ナ～ナ～ナ🍌<br>
            バ～ナ🍌 ナナナナ～🍌<br>
            <br>目まぐるしく回る <span class="banana">🍌</span></b>
            '''
        # 漢字四文字か判定
        elif render.fullmatch(r'[\u4E00-\u9FFF]{4}', yjjkg):
            first_niji = yjjkg[:2]
            last_niji = yjjkg[2:]
            first_sanji = yjjkg[:3]

            # 音節(モーラ)判定
            def is_two_mora(yojijukugo):
                head2 = yojijukugo[:2]
                hiragana = kanjiconv.to_hiragana(head2)
                mora_count = 0
                i = 0
                while i < len(hiragana):
                    if i + 1 < len(hiragana) and hiragana[i+1] in "ぁぃぅぇぉゃゅょ":
                        mora_count += 1
                        i += 2
                    else:
                        mora_count += 1
                        i += 1
                return mora_count == 2

            if is_two_mora(yjjkg):
                # 通常処理
                result = f"""
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
                """

            else:
                result = markdown.markdown("## SORRY...\n### This phrase is not suitable for A・RA・SHI")
        else:
            result = markdown.markdown("##おい")

    return render(request, "arashi_yjjkg/index.html", {"result": result})
