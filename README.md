# 非公式Script Mapper
[公式版Script Mapper](https://github.com/hibit-at/Scriptmapper)を機能拡張したものです。基本的な使い方は公式版と同じです。

# 公式版との差分

## rotateコマンド

![](https://raw.github.com/wiki/rei05/Scriptmapper/images/rotate_sample.gif)

## rotコマンド

任意のstart点から任意のend点へ回転移動させるコマンドです。

コマンド書式: `[start],[end],rot_n_o`

`n`パラメータ：回転数を指定する。真上から見て正の数は反時計周り、負の数は時計回り。0は無効。1とすると、startからendへ反時計周りに回転移動する。2とすると、startからendへ反時計周りに回転移動した後さらに1回転する(＝endを2回通過する)。

`o`パラメータ：公式版rotateコマンドのoパラメータと同じ。



ex1) `center3,side3,rot_1_0`（center3の位置からside3の位置まで反時計周りに回転しながら移動）

ex2) `q_-3.93_2.97_0.12_28.6_90.4_0_60,q_2.12_2.46_-2.49_17.7_320.7_0_60,rot_-2_1` （qコマンドとの併用）


**制約事項および既知の問題点**

・rotコマンドとeaseコマンドは併用できません。

・カメラのRotY向きは現在の回転角によって自動決定されstart/endでのカメラ向きは無視されます。前のブックマークにnextコマンドを置いたり、次のブックマークにstopを置いたとしても"滑らかには"画面遷移できません。
