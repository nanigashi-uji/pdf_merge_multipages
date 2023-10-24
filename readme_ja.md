# Pdf_merge_multipage

PDFファイルの複数ページを余白なしで1ページにまとめるレイアウト変更のためのスクリプト。

## 動作要件

  1. pdf_merge_multipages3.py
    - Python: 3.11 で動作確認
    - pypdf: https://pypi.org/project/pypdf/
      - version 3.16.2  で動作確認

  2. pdf_merge_multipages.py
    - Python: 2.7で動作確認
    - PyPDF2: https://pythonhosted.org/PyPDF2/
      - version 1.26.0 で動作確認

## 使い方

```
usage: pdf_merge_multipages3.py [-h] [-output filename] [-columns n_h] [-lines n_v] [-page-order opt]
                                [-rotation opt] [-valign opt] [-align opt] [-metainfo opt] [-title text]
                                input-file [input-file ...]

usage: pdf_merge_multipages.py [-h] [-output filename] [-columns n_h] [-lines n_v] [-page-order opt]
                               [-rotation opt] [-valign opt] [-align opt] [-metainfo opt] [-title text]
                               input-file [input-file ...]

Merge multiple mages in PDF files w/o gap.

positional arguments:
  input-file        Input PDF file(s)

optional arguments:
  -h, --help        show this help message and exit
  -output filename  Output file
  -columns n_h      # of columns of merged pages (default = 2)
  -lines n_v        # of lines of merged pages (default = 1)
  -page-order opt   Page order (choices=left2right[default], left2bottom, right2left, right2bottom)
  -rotation opt     Page orientation (choices=none[default], flip, right, left, auto, rauto)
  -valign opt       Page fitting (choices=resize, none[default], top, bottom, center, fit)
  -align opt        Page fitting (choices=resize, none[default], right, left, center, fit)
  -metainfo opt     Meta data for marged file (choices=full[default], none, partial, short)
  -title text       set title in meta data for marged file (Default: output file name)
```

## オプション引数

  - `-output filename`: 出力ファイルの名前。指定しない場合のデフォルトは、`a.out.pdf`
  - `-columns nh`, `-lines n_v`: レイアウトの指定: 入力PDFファイルのpageを、横n_h列×縦n_v行に配置する。指定しない場合のデフォルトは、2x1 ("2up")
  - `-page-order option`: ページをレイアウトする配置する順番の指定。
    - `left2right`: 入力ファイルの最初のページを左上に配置。入力ファイルの続くページを右に順次配置していき、右端に到達したら、直下の段の左端または次ページの左上から右へ順次配置していく。(デフォルト)
    - `left2bottom`: 入力ファイルの最初のページを左上に配置。入力ファイルの続くページを下に順次配置していき、下端に到達したら、右隣の列の上端または次ページの左上から下へ配置していく。
    - `left2top`: 入力ファイルの最初のページを左下に配置。入力ファイルの続くページを上に順次配置していき、上端に到達したら、右隣の列の下端または次ページの左下から上へ配置していく。
    - `right2left`: 入力ファイルの最初のページを右上に配置。入力ファイルの続くページを左に順次配置していき、左端に到達したら、直下の段の右端または次ページの右上から左へ順次配置していく。
    - `right2bottom`:入力ファイルの最初のページを右上に配置。入力ファイルの続くページを下に順次配置していき、下端に到達したら、左隣の列の上端または次ページの右上から下へ配置していく。
    - `right2top`: 入力ファイルの最初のページを右下に配置。入力ファイルの続くページを上に順次配置していき、上端に到達したら、左隣の列の下端または次ページの右下から上へ配置していく。
  - `-rotation option`: ページの回転
    - `none`:  配置される入力ファイルの各ページを回転しない。(デフォルト)
    - `flip`:  配置される入力ファイルの各ページを上下反転する。
    - `right`: 配置される入力ファイルの各ページを右に90度回転する。
    - `left`:  配置される入力ファイルの各ページを左に90度回転する。
    - `auto`:  出力ページの先頭に配置される入力ファイルの各ページが縦置き(横置き)の場合、出力ファイルの同じページに配置される他の入力ファイルの各ページが横置き(縦置き)の場合には左に90度回転して配置し、そうでない場合には回転せずに配置する。
    - `rauto`:　出力ページの先頭に配置される入力ファイルのページが縦置き(横置き)の場合、出力ファイルの同じページに配置される他の入力ファイルの各ページが横置き(縦置き)の場合には右に90度回転して配置し、そうでない場合には回転せずに配置する。
  - `-valign opttion`: 配置されるページの縦方向位置調整の指定
    - `none`,`bottom`: 下揃え (デフォルト)
    - `center`:        上下中央揃え
    - `top`: 上揃え
    - `resize`: 出力ページの先頭に配置される入力ファイルのページの縦方向のサイズに合わせて縮小する。`-algin resize`または`-algin fit`と同時に指定された場合には、より縮小率の小さくなる可能性があるが、その場合でもレイアウト間隔は、出力ページの先頭に配置される入力ファイルのページの縦方向のサイズとなる。
    - `fit`: 出力ページの先頭に配置される入力ファイルのページの縦方向のサイズに合わせて縮小する。`-algin resize`または`-algin fit`と同時に指定された場合には、より縮小率の小さくなり、レイアウト間隔も出力ページの先頭に配置される入力ファイルのページの縦方向のサイズより小さくなることがある。

  - `-align opttion`: 配置されるページの横方向位置調整の指定
    - `none`,`left`: 右揃え (デフォルト)
    - `center`: 左右中央揃え
    - `right`: 右揃え
    - `resize`: 出力ページの先頭に配置される入力ファイルのページの横方向のサイズに合わせて縮小する。`-valgin resize`または`-valgin fit`と同時に指定された場合には、より縮小率の小さくなる可能性があるが、その場合でもレイアウト間隔は、出力ページの先頭に配置される入力ファイルのページの横方向のサイズとなる。
    - `fit`: 出力ページの先頭に配置される入力ファイルのページの横方向のサイズに合わせて縮小する。`-valgin resize`または`-valgin fit`と同時に指定された場合には、より縮小率の小さくなり、レイアウト間隔も出力ページの先頭に配置される入力ファイルのページの横方向のサイズより小さくなることがある。
  - `-metainfo options`: 出力ファイルのメタ情報の指定
     - `full`: 入力ファイルのメタ情報を結合したものに追記して生成。(デフォルト)
     - `partial`: 入力ファイルのメタ情報を結合したものの一部に追記して生成
     - `short`: '/Title'、'/Creater', '/Producer'のみ生成
     - `none`: 出力ファイルのメタ情報を生成しない.(PyPDF2のデフォルト値が指定される。)
  - `-title text`: 入力ファイルのメタ情報のタイトルを指定する。(デフォルトは出力ファイル名)


## Author
  Nanigashi Uji (53845049+nanigashi-uji@users.noreply.github.com)
 
