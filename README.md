# Montreal Force Aligner の使い方まとめ

## 環境構築

### 仮想環境の構築とライブラリのインストール

Montréal Forced Aligner（以降MFA）は，pip ではインストールできないため， conda でインストールする必要があるようです．

alignerという名前の環境を作ります．

なお，`conda install`などで異常に時間がかかる場合は anaconda の更新が必要なので，必要に応じて管理者に問い合わせてください．

```
conda create -n aligner python=3.11
conda activate aligner
conda config --add channels conda-forge
conda install montreal-forced-aligner
```

日本語を扱うときは下記も必要です．

```
conda install -c conda-forge spacy sudachipy sudachidict-core
```

### 日本語モデルのダウンロード

```
mfa model download dictionary japanese_mfa
mfa model download acoustic japanese_mfa
```

場合によっては，GitHubの制限にかかってしまい，ダウンロードができないことがあります．
その場合は，[Developer Settings](https://github.com/settings/apps)から個人用アクセストークンを取得し，下記の要領で実行してください．

```
mfa model download dictionary japanese_mfa --github_token アクセストークン
mfa model download acoustic japanese_mfa --github_token アクセストークン
```

各種ファイルは，`~/Documents/MFA`以下にダウンロードされます．

## 実行

### 入力データ

MFAは，音声ファイルとそれに対応するテキストファイルが同じディレクトリにあることを前提としています．

また，ディレクトリ内にある全てのファイルを一度に処理する（バッチ処理をする）ことを前提にしています．

例えば，以下のようなディレクトリ構造を想定しています．

```
data/
    - file1.wav
    - file1.txt
    - file2.wav
    - file2.txt
    - ...
```

### 実行

`mfa align`コマンドを使用して，アライメントを取ります．

```
mfa align ./data japanese_mfa japanese_mfa ./data_aligned
```

- `./data`: 入力データがあるディレクトリ
- `japanese_mfa`: 使用するモデル（辞書と音響モデル．今回は同じ名前）
- `./data_aligned`: 出力データを保存するディレクトリ

### 結果

アライメントの結果は，`./data_aligned` に保存されます．

例えば `file1.wav` に対してアライメントを取った場合，`file1.TextGrid` などのファイル（TextGrid形式）が生成されます．

## 実行例: JSUTコーパス

### データの準備

JSUTコーパスの最初の100文（BASIC5000_0001〜BASIC5000_0000）を使用してアライメントを取る例を考えます．

JSUTのBASIC5000のディレクトリが，環境変数`JSUT_BASIC5000_DIR`に設定されていると仮定します．

```
export JSUT_BASIC5000_DIR=/path/to/jsut/basic5000
```

MFAに与えるディレクトリは， `./data` であるとします．

まず wav ファイルをコピーします．

```
mkdir -p data
for i in $(seq -f "%04g" 1 100); do
    cp $JSUT_BASIC5000_DIR/wav/BASIC5000_$i.wav data/
done
```

次に，トランスクリプトファイル（$JSUT_BASIC5000_DIR/transcript_utf8.txt）から，対応するテキストファイルを生成します（pythonスクリプトを使用します）．

```
python make_transcript.py $JSUT_BASIC5000_DIR/transcript_utf8.txt 1 100 data/
```

### アライメントの実行

`./data`の中のデータに対してアライメントを実行し，結果を `./data_aligned` に保存します．

```
mfa align ./data japanese_mfa japanese_mfa ./data_aligned
```

### 実行結果

実行結果は`./data_aligned` に，
`BASIC5000_0001.TextGrid` などのファイル（TextGrid形式）が生成されます．

## TextGrid ファイルの変換

TextGrid ファイルは，Praatで利用されるファイル形式で，実体はテキストファイルですがそのままでは少々扱いにくいため，下記のようなCSVファイルに変換するスクリプト（`textgrid2csv.py`）を用意しました．

```plain text
type,label,start_time,end_time
word,,0.0,0.29
word,水,0.29,0.55
word,を,0.55,0.66
word,マレーシア,0.66,1.23
word,から,1.23,1.43
word,買わなくて,1.43,1.99
word,は,1.99,2.1
word,ならない,2.1,2.52
word,の,2.52,2.61
word,です,2.61,3.0
word,,3.0,3.19
phone,,0.0,0.29
phone,mʲ,0.29,0.34
phone,i,0.34,0.43
phone,z,0.43,0.5
phone,ɨ,0.5,0.55
...
```

- type: `word`（単語）または `phone`（音素）
- label: 単語または音素の内容
- start_time: 開始時刻（秒）
- end_time: 終了時刻（秒）

`textgrid2csv.py`を使用すると，TextGridファイルをCSVファイルに変換できます．

```bash
python textgrid2csv.py data_aligned/BASIC5000_0001.TextGrid BASIC5000_0001.csv
```

出力ファイル名を`-`にすると，標準出力に出力されます．

```bash
python textgrid2csv.py data_aligned/BASIC5000_0001.TextGrid -
```

## 音素体系

日本語の音素体系については，[こちら](https://mfa-models.readthedocs.io/en/latest/mfa_phone_set.html#japanese)を参照してください．

音素記号が複雑なため，モーラ単位のアラインメントに変換するのは少し手間がかかるかもしれません．