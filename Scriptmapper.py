from cgi import print_arguments
import sys
from ScriptMapperClass import ScriptMapper


def mapping(file_path):
    mapper = ScriptMapper()
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

    # nextの計算
    mapper.next_calc()

    # easeの処理
    mapper.ease_calc()

    # rotの処理
    mapper.rot_calc()

    # vibの処理
    mapper.vib_calc()

    # レンダリング
    mapper.render_json()

    # ファイルの書き出し
    mapper.create_file()


if __name__ == "__main__":
    # ファイルパスの取得
    if len(sys.argv) == 1:
        print('Script Mapper は単独では開けません。譜面の dat ファイルをドラッグ＆ドロップしてください。')
        input()
        exit()
    file_path = sys.argv[1]
    mapping(file_path)
