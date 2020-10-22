# 使い方
- Discordで予定管理ができるBotです。初回に!helpを実行することを強くおすすめします。基本的には非同期処理で動くのでコマンドを実行中でも別のコマンドを実行することができますが、おそらく出力がバグるのでオススメしません。また時刻を入力するときには0000-00-00 00：00の書式に準ずるようお願いします。

## コマンド一覧
|コマンド|コマンドの詳細|
|:---------:|:---------:|
|!help|ヘルプメッセージを表示します。|
|!set|予定を設定します。画面の指示に従って入力を完了してください。|
|!del|予定の削除を行います。画面の指示に従って操作を完了してください。|
|!list|全予定のlistを出力します。|
|!edit|予定の再登録をします。|
|!allclear|CSV上に保持されているデータを全削除した後CSVファイルを再作成します。|


## 注意点
- 動作が重いときがあります。ご了承ください。
- !delコマンドではlistの何番目かと聞かれますが、初期値は０ではなく１です。
- CSVファイルがデータ保持のため作成されます。 

###Codeを見るといいことあるかも。
