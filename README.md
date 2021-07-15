# Script Mapper

このツールは、以下のようにマッピングソフト上でブックマークに命令（スクリプト）を書いていくことにより、同じタイミングでカメラが動いてくれるようなカメラスクリプトを作成します。[デモ動画](https://www.youtube.com/watch?v=U3miXkN7Uyo)

<img width="773" alt="read0" src="https://user-images.githubusercontent.com/43929933/124960735-95817d00-e057-11eb-81b3-41cc6db394e6.png">

# 実行方法
WIP フォルダ直下にカスタムマップフォルダをコピーし、その中に Scriptmapper.exe を入れてください。

<img width="545" alt="read1" src="https://user-images.githubusercontent.com/43929933/124960738-974b4080-e057-11eb-8916-055f7e302ec6.png">

本ツールは、ブックマークの編集中にカスタムマップの譜面データを変更してしまう危険性を考慮し、**CustomWIPLevels 直下でないとエラーを起こす**ように設定しています。お手数ですが、必ずマップを CustomWIPLevels にコピーしてから作業を行ってください。

ブックマークでスクリプトを記入した dat ファイルを、Scriptmapper.exe のアイコンにドラッグ＆ドロップしてください。

<img width="555" alt="read2" src="https://user-images.githubusercontent.com/43929933/124960956-d7aabe80-e057-11eb-9c72-788a6e389339.png">

同じフォルダに `SongScript.json` が出力されていれば成功です。後は、`camerascript.cfg` の設定を `songSpecificScript=True`に指定すれば、その譜面をプレイする時には、マッピングした通りにカメラが動作してくれるはずです！

また、作業中のWIPマップと同じ名前のフォルダがカスタムマップにあった場合、そちらにも同じ内容の`SongScript.json`が生成されます。これは通常のプレイにおいても、このツールで作成したカメラスクリプトで遊べるようにするためですが、もし既存に別の`SongScript.json`がある場合は上書きされてしまうのでご注意ください。

# ログの確認方法

同時に `logs` というフォルダの中に log というテキストファイルが生成されます。

<img width="556" alt="read3" src="https://user-images.githubusercontent.com/43929933/124961134-0c1e7a80-e058-11eb-82fd-3e38eea6e412.png">

生成に失敗した場合、また成功しても、意図したカメラの動きになっていない場合、log を見れば原因がわかるかもしれません。例えば、あるコマンドを検出した後に log が途切れていれば、その後のコマンドのパラメータの設定に失敗した可能性が高いです。

<img width="746" alt="read4" src="https://user-images.githubusercontent.com/43929933/124960744-97e3d700-e057-11eb-94d8-dd6977ed66f4.png">

# スクリプトの設定方法

- スクリプトは「,」（カンマ）によって startコマンドとendコマンドに区切られます。
- スクリプトの持続期間は、そのブックマーク位置から、次のブックマーク位置までです。
- カメラの位置・角度は、startコマンドの位置からendコマンドの位置まで連続的に変化します。
- endコマンドを省略した場合には自動的に`stop`が入ります。（つまり、その区間のカメラはstartコマンドの位置で静止します）

ブックマークは、マッピングソフト上で**bキーを打つ**ことで設定できます。

# プリセットコマンド　基本編
スクリプトの先頭に以下の文字が書かれていた場合、プリセットコマンドとして認識されます。以下、位置に関わるパラメータは**メートル基準**、角度に関わるパラメータは**0～360度基準**になります（ラジアンではありません）。位置や前後左右はアバター（＝プレイヤー）が立っている位置・向いている向きを基準とします。

|名前|説明|パラメータ|例|
|---|---|---|---|
|`center`|真正面からアバターを見る、または真後ろから見下ろす位置にカメラを置きます。|前方向位置|`center1`|
|`top`|アバターの真上やや前方にカメラを置きます。まっすぐ見下ろします。|高さ|`top3`|
|`side`|真横にカメラを置きます。高さは 1.5 m（ほぼ顔と同じ位置）。|右手方向位置|`side3`|
|`diagf`|斜め前にカメラを置きます。高さは 3 m（見下ろす位置）。|右手前方向位置|`diagf3`|
|`diagb`|斜め後ろにカメラを置きます。高さは 3 m（見下ろす位置）。|右手後方向位置|`diagb3`|
|`random`|ランダムな座標にカメラを置きます。|半径|`random3`|

※当ツールのパラメータは、位置・角度ともに、基本的にUnityの座標系で**正になる**ように設定しております。

※`center`のカメラ位置は、アバターより前方ならば目線の高さに、後方ならば見下ろす位置になります

# オリジナルコマンド
デフォルトコマンドで表現が難しい場合は、自分でパラメータを指定したオリジナルコマンドを作成します。オリジナルコマンドは以下のような csv ファイルを用意し「`input.csv`」と名付けます。（それ以外の名前ではプログラムが認識しません）。雛形として`input.csv`を同梱しているので、その下に書き足していくのが便利だと思います。

<img width="461" alt="read5" src="https://user-images.githubusercontent.com/43929933/124960746-97e3d700-e057-11eb-9fa8-31dadfd102b6.png">

ヘッダー（1行目）の列名の意味は以下になります。

|列名|機能|
|---|---|
|`label`|コマンドとして認識される名前。これと同じ名前をスクリプトに記入することで、コマンドとして機能します。|
|`px`|カメラの x 位置|
|`py`|カメラの y 位置|
|`pz`|カメラの z 位置|
|`lookat`|ここを `true` にした場合、自動的にアバターを向く角度を指定します。以降に記入する角度のパラメータは無視されます。|
|`rx`|カメラの x 角度|
|`ry`|カメラの y 角度|
|`rz`|カメラの z 角度|

<img width="782" alt="read6" src="https://user-images.githubusercontent.com/43929933/124961676-ba2a2480-e058-11eb-8afe-9c738df5951a.png">

※位置・角度による見え方のプレビューには https://rotatescript.herokuapp.com/params/ が便利です

---

※これより下の内容は発展的な内容になります。

# プリセットコマンド　中級編

以下のコマンドは、直前に指定した座標に操作を加えるものです。startコマンドに入れた場合、その前のスクリプトが**動作し終わった後の**座標に対して操作を行った座標を、スクリプト開始時に返します。endコマンドに入れた場合、startコマンドに入れた座標から、それに操作を行った座標まで、スクリプトの期間中連続的に変化します。（詳細は下の※を参照）

|名前|説明|パラメータ|例|
|---|---|---|---|
|`stop`|直前の座標でカメラを止めます。|-|`stop`|
|`mirror`|直前の座標を左右方向に鏡像反転させます。|-|`mirror`|
|`zoom`|直前の座標を縮小します（つまりアバターに近づく）。縮小の中心は(0,1.5,0)です（おおよそアバターの顔の位置）。|縮小倍率|`zoom2`|
|`spin`|カメラの z 方向角度（ロール）を変化させます。|反時計周り角度|`spin-40`|
|`slide`|カメラの左右方向の位置を移動させます。|右方向位置|`slide.5`|
|`shift`|カメラの上下方向の位置を移動させます。|上方向位置|`shift.5`|
|`push`|カメラの前後方向の位置を移動させます。|前方向位置|`push1`|
|`screw`|spinとzoomをあわせたような動きをします。|縮小倍率|`spin5/4`|

※パラメータの指定はマイナス`-40`、小数点開始`.5`、分数`5/4`でも可能です。アルファベットを含めた場合、エラーが発生します。

※startとendによるカメラの座標の変化は、例えば以下のようになります。

- `stop`直前のスクリプトが動作し終わった座標で、スクリプトの期間中**ずっと固定**。
- `mirror`直前のスクリプトが動作し終わった座標を鏡像反転させた座標で、スクリプトの期間中**ずっと固定**。
- `stop,mirror`直前のスクリプトが動作し終わった座標から、それを鏡像反転させた座標まで、スクリプトの期間中**連続的に変化**。



# プリセットコマンド　上級編

以下のコマンドは単一の座標を返すのではなく、一定の連続した動きを記述するコマンドです。

## rotate

カメラがアバターを中心に回転します。後に続く文字列をそれぞれ半径、高さ※と認識します。また、半径は高さを考慮しない水平投影面での半径を示します。

ex) `rotate4,3` （半径 4m、高さ 3m の円軌道）

※カメラの見え方のプレビューには https://rotatescript.herokuapp.com/params/ が便利です。

※正確には、パラメータを最大5個まで設定できます。パラメータの対応関係は、リンク先の`r`,`h`,`a`,`o`,`s`（半径、高さ、ターゲット高さ、オフセット位置、z軸回転）にあたります。しかし、煩雑になるので、慣れない内は半径と高さだけ指定して、後はデフォルト値のままにすることをおすすめします。

## vibro
カメラがランダムに移動します。パラメータは周期となり、短い周期を指定すれば振動、長い周期を指定すれば手ブレのような動きになります。

ex) `vibro1/6`

---

※これより下の内容は更にマニアックになります

# 特殊コマンド

以下はスクリプトそのものを対象とする、発展的な特殊コマンドです。ある程度ツールの操作に慣れた上で、操作を省略するためのものです。

## copy

スクリプトをある範囲で一括コピーします。マップの展開が同じ部分で、以前書いたブックマークを使い回す時に便利です。つまり、以下の画像はプログラム上では同じものとして認識されます。

<img width="779" alt="read9" src="https://user-images.githubusercontent.com/43929933/124960756-9adec780-e057-11eb-8262-4774fe4e8892.png">
<img width="794" alt="reada" src="https://user-images.githubusercontent.com/43929933/124960762-9c0ff480-e057-11eb-8e5f-0c5ec166018c.png">

例えば、100グリッド目で`copy40`と書いたとします。その次のブックマークが120だった場合、コピーを**貼り付ける**範囲は100～120になります。この長さは20です。そしてコピーの**元となる**範囲は40から始まり、同じ長さを持つ部分になります。つまり、40～60の部分が100～120の範囲に転写されます。この時、終点となる60や120丁度のグリッドは転写範囲に**含まれない**ことに注意してください。※

ex) `copy40`

※開始地点から「終了地点までの」範囲ではなく、「次の範囲の開始地点の直前まで」と考えます。例えば、64グリッド目から更に32グリッド分を含む範囲は95グリッドまでですが、64+32=96グリッド目の「直前まで」と考えた方が計算としてはわかりやすいです。

## fill

スクリプトを反復複製します。例えば、`random3`をある区間何回も繰り返す場合、それらをすべて書くのは面倒です。そのような場合、例えば`fill1/4,random3`と書くことで、同じ記述を反復することができます。つまり、以下の画像はプログラム上では同じものとして認識されます。

<img width="725" alt="read7" src="https://user-images.githubusercontent.com/43929933/124960751-99150400-e057-11eb-8430-2fa2d2da73e4.png">
<img width="776" alt="read8" src="https://user-images.githubusercontent.com/43929933/124960754-99ad9a80-e057-11eb-9ffe-87f9825b8ea5.png">

fill の後に続く文字列をスパン、カンマで区切られた後の文字列をパターンとして認識します。つまり`fill1/4,random3`は次のブックマークまで、マッパー上のグリッドの 1/4 間隔で`random3`というブックマークを記入し続けます。

ex) `fill1/4,random3,zoom2`（グリッド 1/4 間隔で`random3,zoom2`を記入し続ける）

ex) `fill2,mirror`（グリッド 2 間隔で`mirror`を記入し続ける）

## copyとfillの併用

copy範囲に他のスクリプトを含めることはできません（そうなった場合、挟まれたコマンドがcopyの終点になってしまいます）。しかし、fill内にcopyを含めることはできます。

ex) `fill2,copy40` fillの終点まで、グリッド40~42の内容が反復されることになります
