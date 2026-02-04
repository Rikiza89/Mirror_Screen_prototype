# ハンドコントロール デスクトップUI 🖐️

Webカメラとハンドジェスチャーで完全に操作できるコンピュータビジョンベースのデスクトップインターフェース。Python、OpenCV、MediaPipeで構築。

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/opencv-4.8+-green.svg)
![MediaPipe](https://img.shields.io/badge/mediapipe-0.10+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 機能

### 🎮 インタラクティブなデスクトップUI
- **仮想キーボード**：スペース、バックスペース、エンターキーを含む完全なQWERTYキーボード
- **Webブラウザ統合**：ブラウザを開き、Google検索を実行
- **ボールバウンスゲーム**：物理ベースのボールバウンスを備えた両手コントロールゲーム
- **カメラ背景**：カメラフィードと単色背景の切り替え
- **ハンドトラッキング可視化**：手のスケルトンオーバーレイのオン/オフ切り替え

### 🎯 ジェスチャーコントロール
- **カーソル操作**：人差し指を動かしてカーソルを制御
- **クリックジェスチャー**：親指と人差し指をつまんでクリック
- **両手バー**：ゲームモードでは、両手の手のひらの間にバーを作成

### 🎲 ボールバウンスゲーム
- 60秒のゲームプレイで20個のボール
- 両手で作成したバーでボールをバウンスさせてポイント獲得
- 連続バウンスのコンボシステム
- リアルタイム統計表示（スコア、コンボ、時間、残りボール数）
- 最終統計付きのゲームオーバー画面

## インストール

### 前提条件
- Python 3.8以上
- Webカメラ（内蔵または外付け）
- Windows、macOS、またはLinux

### セットアップ

1. リポジトリをクローン：
```bash
git clone https://github.com/Rikiza89/Mirror_Screen_prototype.git
cd Mirror_Screen_prototype
```

2. 仮想環境を作成（推奨）：
```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

3. 依存関係をインストール：
```bash
pip install -r requirements.txt
```

## 使用方法

アプリケーションを実行：
```bash
python hand_ui_prototype.py
```

### 操作方法

#### メインUIモード
- **カーソル移動**：カメラに向かって人差し指を向ける
- **クリック**：親指と人差し指をつまむ
- **Keyboardボタン**：仮想キーボードの表示切り替え
- **Browserボタン**：デフォルトのWebブラウザを開く
- **Searchボタン**：入力したテキストでGoogle検索
- **Ball Gameボタン**：ボールバウンスゲームを開始
- **Camera BGボタン**：カメラ背景のオン/オフ切り替え
- **Show Handsボタン**：ハンドランドマーク可視化のオン/オフ切り替え

#### ゲームモード
- **両手を見せる**：手のひらの間にバーを作成
- **手を動かす**：バーの位置を調整して落下するボールをバウンス
- **ミスを避ける**：ボールを逃すとコンボがリセット
- **制限時間**：60秒でできるだけ多くのポイントを獲得

### キーボードショートカット
- **Q**：アプリケーションを終了
- **Xボタン**：ウィンドウを閉じる

## 設定

コード内で以下のパラメータを調整できます：

```python
# UI設定
UI_WIDTH = 1280
UI_HEIGHT = 720
PINCH_THRESHOLD = 40  # 手のサイズに合わせて調整

# ゲーム設定
GAME_DURATION = 60  # 秒
TOTAL_BALLS = 20
BALL_SPEED = 5
BAR_THICKNESS = 20
```

## トラブルシューティング

### カーソルが動かない
- 良好な照明条件を確保
- Webカメラの権限を確認
- ピンチ検出が敏感/鈍感な場合は`PINCH_THRESHOLD`を調整

### ハンド検出の問題
- カメラから1〜2フィート（30〜60cm）の位置に立つ
- 手が明確に見えることを確認
- 乱雑な背景を避ける
- 「Show Hands」をトグルしてハンドトラッキングをデバッグ

### パフォーマンスの問題
- Webカメラを使用している他のアプリケーションを閉じる
- より良いFPSのために`UI_WIDTH`と`UI_HEIGHT`を削減
- 十分なCPUリソースを確保

### カメラが見つからない
- Webカメラの接続を確認
- カメラの権限を確認
- コード内のカメラインデックスを変更してみる：`cv2.VideoCapture(0)` → `cv2.VideoCapture(1)`

## 技術詳細

### ハンドトラッキング
- **MediaPipe Hands**：1つの手につき21個のハンドランドマーク
- **手のひら検出**：手首と指の付け根のランドマークの平均
- **ジェスチャー認識**：距離ベースのピンチ検出

### 座標マッピング
- カメラ空間 → UI空間への変換
- ミラー効果のための水平反転
- リアルタイムカーソル位置追跡

### ゲーム物理演算
- 一定速度のボール移動
- 壁の衝突検出
- バーとボールの交差テスト
- コンボ追跡システム

## プロジェクト構成

```
Mirror_Screen_prototype/
├── hand_ui_prototype.py    # メインアプリケーション
├── requirements.txt         # Python依存関係
├── README.md               # 英語版README
├── README_JP.md            # 日本語版README（このファイル）
└── LICENSE                 # MITライセンス
```

## 依存関係

- **OpenCV**：ビデオキャプチャと画像処理
- **MediaPipe**：ハンドトラッキングとランドマーク検出
- **NumPy**：数値演算
- **webbrowser**：ブラウザ統合（標準ライブラリ）

## 貢献

プルリクエストを歓迎します！

1. リポジトリをフォーク
2. 機能ブランチを作成（`git checkout -b feature/素晴らしい機能`）
3. 変更をコミット（`git commit -m '素晴らしい機能を追加'`）
4. ブランチにプッシュ（`git push origin feature/素晴らしい機能`）
5. プルリクエストを開く

## 今後の改善予定

- [ ] マルチジェスチャーサポート（スワイプ、回転、ズーム）
- [ ] カスタマイズ可能なUIテーマ
- [ ] 追加のミニゲーム
- [ ] 音声コマンド統合
- [ ] マルチユーザーサポート
- [ ] ジェスチャーの記録と再生
- [ ] より簡単な設定のための設定メニュー

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 謝辞

- ハンドトラッキングソリューションのための[MediaPipe](https://google.github.io/mediapipe/)
- コンピュータビジョンツールのための[OpenCV](https://opencv.org/)
- ジェスチャーベースのインタラクション研究に触発されました

## 作成者

プロジェクトリンク: [https://github.com/Rikiza89/Mirror_Screen_prototype](https://github.com/Rikiza89/Mirror_Screen_prototype)

---

⭐ このリポジトリが役に立ったらスターをつけてください！
