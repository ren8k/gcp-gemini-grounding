# Gemini Chat Application with Google Search Integration

本アプリケーションは，Google VertexAI の [Grounding for Google Search](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/ground-gemini?hl=ja#generative-ai-gemini-grounding-python_vertex_ai_sdk) を利用したした対話型チャットボットです．Streamlit を使用して Web インターフェースを提供し，ユーザーからの質問に対して信頼性の高い情報源を基に回答を生成します．

## 機能

- Gemini 1.5 Flash を利用
- Google 検索による情報の裏付け
- 検索結果の出典表示

## 必要条件

- Python 3.12 以上
- Google Cloud アカウント
- Vertex AI API の有効化
- 必要な認証情報（サービスアカウントキー）

## 必要なパッケージ

```bash
pip install streamlit
pip install google-cloud-aiplatform
```

## セットアップ

1. Google Cloud でプロジェクトを作成し，Vertex AI API を有効化します．

2. サービスアカウントを作成し，キーファイルをダウンロードします．

   - キーファイルは `vertexai-credentials.json` として保存し，`src` ディレクトリに配置します．

## 使用方法

1. アプリケーションの起動:

```bash
streamlit run main.py
```

2. ブラウザで表示されるインターフェースにアクセスし，チャットボックスに質問を入力します．

3. アプリケーションは以下の情報を含む回答を生成します：
   - 質問に対する回答
   - 参考にしたウェブページの URL 一覧
   - 使用された検索キーワード

## 参考

- https://zenn.dev/google_cloud_jp/articles/c1b037dd6e888e
- https://zenn.dev/makochan/articles/b3b81b83ae1a37
