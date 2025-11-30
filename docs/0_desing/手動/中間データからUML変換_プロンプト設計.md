# 中間データからUML変換_プロンプト設計

## (1) インフラ系（CloudFormation / Terraform / K8s）→ コンポーネント図

次の JSON は、インフラ/アプリケーション構成の要素と関係を表しています。
この JSON をもとに、PlantUML のコンポーネント図を生成してください。

条件:
- 出力は ```plantuml 〜 ``` のコードブロックのみ
- @startuml から @enduml までを含める
- AWS リソースや K8s オブジェクトごとに stereotype を付与する
  - 例: [WebApp] <<EC2>>、[DB] <<RDS>>、[api-service] <<Deployment>>
- relations.kind に応じて、矢印の種類・ラベルを工夫する
  - uses: -->、in-subnet: -down-、attached-to: ..> など

構造 JSON:

```json
(ここにさっき ChatGPT に作らせた JSON)
```

## (2) クラス図用 PlantUML

```text
次の JSON はクラス構造を表しています。
これをもとに、PlantUML のクラス図を生成してください。

条件:
- 出力は ```plantuml 〜 ``` のコードブロックのみ
- 主要なクラスのフィールド・メソッド名を数個ずつ含める（すべては不要）
- depends_on をクラス間の関連として矢印で表現する

JSON:

```json
(クラス構造の JSON)
```

## (3) シーケンス図用 PlantUML

ソースコードや仕様書からユースケースを抽象化して書かせます。

```text
以下の説明とコード片から、「ユーザーが〇〇を実行する」ユースケースの処理シーケンスを抽象化してください。
その上で、PlantUML のシーケンス図を生成してください。

条件:
- 出力は ```plantuml 〜 ``` のコードブロックのみ
- ライフラインは 5〜10 個程度にまとめる（Controller / Service / Repository / 外部API / DB など）
- 細かい内部処理よりもコンポーネント間のやり取りを重視する

(仕様やコードの説明をここにペースト)
