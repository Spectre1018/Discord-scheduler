#!usr/bin/env python3

import os
import sys
import discord
import datetime
import asyncio



TOKEN = ''#Botのトークンを入力
startChannel = ''#ログインした通知を出すチャンネルを入力

client = discord.Client()



#Elements
global check_flag
check_flag = False
global first_take
first_take = False

database = []



async def tick():
    check = 0
    chk = 0
    now = datetime.datetime.now()
    now_e = datetime.datetime.strftime(now,'%Y-%m-%d %H:%M')
    now_r  = datetime.datetime.strptime(now_e,'%Y-%m-%d %H:%M')
    while len(database) > check:
        tra = database[check][1]
        date = datetime.datetime.strptime(tra,'%Y-%m-%d %H:%M')
        if now_r == date:
            await channel.send("この予定の時間になりました！皆さん心してかかりましょう！")
            await channel.send("予定：{}".format(database[check][0]))
            await channel.send("日時：{}".format(database[check][1]))
            await channel.send("コメント↓↓↓")
            await channel.send(database[check][2])
            del database[check]
        elif now_r  != date:
            check = check + 1



async def scheduler(interval=58):
  global check_flag
  while check_flag == True:
    await asyncio.sleep(interval)
    await tick()
        


@client.event
async def on_ready():
    print(f'Logged in as: {client.user.name}')
    print(f'With ID: {client.user.id}')
    await client.change_presence(activity=discord.Game(name="/helpでHELPメッセージを表示",type=1))
    await client.wait_until_ready()
    channel = client.get_channel(int(startChannel))
    await channel.send("```ログインしました。```")
    



@client.event
async def on_message(message):
    global first_take
    global check_flag
    if message.content.startswith("!set"):
        global channel
        channel = message.channel
        count = 0
        await message.channel.send("予定を設定します！\nBotの指示に従って入力を完了じてください。\nその予定はいつの予定ですか？（YYYY-MM-DD HH:MM）")
        def check(msg):
            return msg.author == message.author
        indate = await client.wait_for("message", check=check)
        await message.channel.send("その予定の名称を設定してください！")
        inname = await client.wait_for("message", check=check)
        await message.channel.send("{0}にコメントを追加します！\nコメントでもURLでもなんでも書いちゃって！".format(inname.content))
        incomment = await client.wait_for("message",check=check)
        await message.channel.send("名称を{0}に設定しました。".format(inname.content))
        await message.channel.send("予定の日時は{0}".format(indate.content))
        await message.channel.send("{0}の予定にコメントを追加しました！↓↓↓".format(inname.content))
        await message.channel.send(incomment.content)
        save = ""
        await message.channel.send("この予定で保存しますか？['y''Y' / 'n''N']")
        save = await client.wait_for("message",check=check)
        if save.content == "Y" or "y":
            d = (inname.content,indate.content,incomment.content)
            database.append(d)
            num = len(database)
            num = num -1 
            await message.channel.send(database[num])
            await message.channel.send("この内容で保存しました!")
            check_flag = True
            if first_take == False:
                await scheduler()
                first_take = True
        else:
            await message.channel.send("再度入力してください。")
    

    if message.content.startswith("!list"):
        cnt = 0
        await message.channel.send("予定の一覧を表示するよ!")
        while len(database) > cnt:
            await message.channel.send(database[cnt])
            cnt = cnt + 1

    if message.content.startswith("!del"):
        def check_1(msg):
            return msg.author == message.author
        await message.channel.send("予定の削除を実行します！\n上から何番目かを入力してください。")
        await message.channel.send(database)
        del_msg = await client.wait_for("message", check=check_1)
        del_msg = int(del_msg.content)
        del_msg = del_msg - 1 
        await message.channel.send("以下の予定を削除します。よろしいですか？['y''Y' / 'n''N']")
        await message.channel.send(database[del_msg])
        yn = await client.wait_for("message",check=check_1)
        if yn.content == "y" or "Y":
            await message.channel.send("予定を削除しました。")
            del database[del_msg]
        else:
            await message.channel.send("もう一度最初からやり直してください。")
        




    if message.content.startswith("!help"):
        help_mes = discord.Embed(title="コマンド一覧を表示します。",color=discord.Colour.from_rgb(166,242,0))
        help_mes.add_field(name="!set",value="新規の予定を設定します。\nBotの指示に従って入力してください。\nコメントは一行でお願いします。",inline=False)
        help_mes.add_field(name="!del",value="登録されている予定の削除を行います。",inline=False)
        help_mes.add_field(name="!list",value="登録されているリストの一覧を表示します。",inline=False)
        await message.channel.send(embed=help_mes)










client.run(TOKEN)