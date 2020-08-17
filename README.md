## 作成方針
### 作りたいシステム
- 学生証の bio, img から学生同士の類似度を計算する
- 使用するライブラリ、API
  - Word2Vec
  - OpenCV
  - [Microsoft Face API](https://azure.microsoft.com/ja-jp/services/cognitive-services/face/)
  - MeCab
  - Django
### GitHub の運用方法
- Pull Request の出し方
  - メソッドかクラスが完成したら Pull Request を出す
    - 行き詰ったら Issue で相談する（Question ラベルをつける）
- ブランチの命名規則
  - `development-[class_name, method_name]`

## 班員情報 (GitHub アカウント名, 学籍番号, 班員氏名, 役割)
  - homomaid, 183334, 佐藤陸, リーダー・ライター・設計
  - Bill4869, 183384, KHAMPASITH CHANVONGNARAZ, ベース・設計・コーダー
  - naoki7090624, 183347, 高橋直暉, コーダー
  - kkbys, 183327, 小林康太, コーダー
  - yamadayuitoTUT, 183381, 山田唯人, コーダー
  - y161853, 161853, 松本優希, デザイン・コーダー

## 使用方法など
### 準備
Anacondaがインストールされている前提で必要なものをインストールする．
~~~sh
(base) $ sudo apt-get update
(base) $ sudo apt-get install mecab mecab-ipadic-utf8 libmecab-dev swig
(base) $ conda create -n py35_sw4a python=3.5.2 django numpy requests nltk gensim
(base) $ conda activate py35_sw4a
(py35_sw4a) $ conda install -c conda-forge django-crispy-forms opencv
(py35_sw4a) $ pip install mecab-python3==0.7 django-stdimage
~~~

### 実行
下記コマンドを実行し，ブラウザから[http://localhost:8000/](http://localhost:8000/)にアクセスする
~~~sh
(py35_sw4a) $ python ./web/manage.py runserver
~~~