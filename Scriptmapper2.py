import sys
from ScriptMapperClass import ScriptMapper

mapper = ScriptMapper()

# ファイルパスの取得
file_path = sys.argv[1]
mapper.set_file_path(file_path)

# WIP の下にあるか確認
mapper.confirm_WIP()

# BPM計測
mapper.check_bpm()

# オリジナルコマンドを追加
mapper.make_manual_commands()

# bookmarkの抽出（raw_b）
mapper.make_raw_b()

# fillの処理（filled_b）
mapper.make_filled_b()

# copyの処理（copied_b）
mapper.make_copied_b()

# durationを計算
mapper.calc_duration()

# 最終的なブックマーク
mapper.show_bookmarks()

# ブックマークをパース
mapper.parse_bookmarks()

# レンダリング
mapper.render_json()

# ファイルの書き出し
mapper.create_file()
