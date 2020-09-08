# 使い方
- Discordで予定管理ができるBotです。基本的には非同期処理で動くのでコマンドを実行中でも別のコマンドを実行することができますが、あまりおすすめしません。（一応実証実験は行っていますが、もしかしたらまだバグがあるやもしれません。）

## コマンド一覧
|コマンド|コマンドの詳細|
|:---------:|:---------:|
|!help|ヘルプメッセージを表示します。|
|!set|予定を設定します。画面の指示に従って入力を完了してください。|
|!del|予定の削除を行います。画面の指示に従って操作を完了してください。|
|!list|全予定のlistを出力します。|
|!edit|予定の再登録をします。|

## 注意点
- もし!setで間違った日時を設定してしまった場合は一度!listを行い予定を確認してから!delを行うことを強くオススメします。
- !delコマンドではlistの何番目かと聞かれますが、初期値は０ではなく１です。# Discord-scheduler
