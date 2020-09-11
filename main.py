#!usr/bin/env python3

import os
import sys
import discord
import datetime
import asyncio
import csv
import copy
import random



TOKEN = ''#botのトークンを入れるところ
startChannel = ''#ログイン時やシステム再起動時にメッセージを吐くところ。専用チャンネルを作るのが望ましい。


client = discord.Client()




#Elements
global check_flag
check_flag = False
global first_take
first_take = False
global second_take
second_take = False
global init
init = False
global database
database = []



async def tick():
    print("in tick")
    check = 0
    chk = 0
    if init == False:
        channel = client.get_channel(int(startChannel))
    else:
        None
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    now_e = datetime.datetime.strftime(now,'%Y-%m-%d %H:%M')
    now_r  = datetime.datetime.strptime(now_e,'%Y-%m-%d %H:%M')
    if second_take == False:
        if os.path.isfile('database.csv') == True:
            with open('database.csv') as db_r:
                reader = csv.reader(db_r)
                database = [row for row in reader] 
        second_take == True
    while len(database) > check:
        tra_tmp = database[check][1]
        tra = tra_tmp.strip("'")
        date = datetime.datetime.strptime(tra,'%Y-%m-%d %H:%M')
        if now_r == date:
            await channel.send("この予定の時間になりました！皆さん心してかかりましょう！")
            await channel.send("予定：{}".format(database[check][0]))
            await channel.send("日時：{}".format(database[check][1]))
            await channel.send("コメント↓↓↓")
            await channel.send(database[check][2])
            del database[check]
            with open('database.csv','w')as db:
                whiter = csv.writer(db)
                whiter.writerows(database)
        elif now_r  != date:
            check = check + 1



async def scheduler(interval=58):
  global check_flag
  print(check_flag)
  while check_flag == True:
    print("in scheduler")
    await asyncio.sleep(interval)
    print("ZZzzzz.....")
    await tick()
        


@client.event
async def on_ready():
    global check_flag
    global database
    print(f'Logged in as: {client.user.name}')
    print(f'With ID: {client.user.id}')
    await client.change_presence(activity=discord.Game(name="!helpでHELPメッセージを表示",type=1))
    await client.wait_until_ready()
    channel = client.get_channel(int(startChannel))
    await channel.send("```Kept You Waiting, Huh?```")
    if os.path.isfile('database.csv') == True:
        check_flag = True
        await scheduler()
    else:
        with open("database.csv",'x'):
            pass

    



@client.event
async def on_message(message):
    global first_take
    global check_flag
    global database
    database_n = []
    if message.content.startswith("!set"):
        global channel
        init = True
        channel = message.channel
        if os.path.isfile('database.csv') == True:
            with open('database.csv') as db_n:
                reader = csv.reader(db_n)
                database_n = [row for row in reader]
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
        grudge = save.content
        if 'y' in grudge or 'Y' in grudge or 'ｙ' in grudge or 'Ｙ' in grudge:
            d = (inname.content,indate.content,incomment.content)
            database_n.append(d)
            with open('database.csv','w') as db_up:
                whiter = csv.writer(db_up)
                whiter.writerows(database_n)
                database = copy.deepcopy(database_n)
            num = len(database)
            num = num -1 
            await message.channel.send(database[num])
            await message.channel.send("この内容で保存しました!")
            check_flag = True
            if first_take == False:
                await scheduler()
                first_take = True
        elif 'y' not in grudge or 'Y' not in grudge or 'ｙ' not in  grudge or 'Ｙ' not in grudge:
            await message.channel.send("再度入力してください。")


    if message.content.startswith("!list"):
        init = True
        cnt = 0
        channel = message.channel
        if os.path.isfile('database.csv') == True:
            with open('database.csv') as db_r:
                reader = csv.reader(db_r)
                database = [row for row in reader] 
        if len(database) > 0:
            await message.channel.send("予定の一覧を表示するよ!")
            while len(database) > cnt:
                list_mes = discord.Embed(title=database[cnt][0]+" : "+database[cnt][1],description= database[cnt][2],color = discord.Colour.from_rgb(65,105,225))
                await channel.send(embed = list_mes)
                cnt = cnt + 1
        else:
            await message.channel.send("データベースに予定は設定されていません。")

    if message.content.startswith("!del"):
        init = True
        cntt= 0
        channel = message.channel
        def check_1(msg):
            return msg.author == message.author
        await message.channel.send("予定の削除を実行します！\n上から何番目かを入力してください。")
        with open('database.csv') as db_r:
            reader = csv.reader(db_r)
            database_d = [row for row in reader] 
        while len(database_d) > cntt:
            del_mes = discord.Embed(title=database[cntt][0]+" : "+database[cntt][1],description= database[cntt][2],color = discord.Colour.from_rgb(222,33,36))
            await channel.send(embed = del_mes)
            cntt = cntt + 1
        del_msg = await client.wait_for("message", check=check_1)
        del_msg = int(del_msg.content)
        del_msg = del_msg - 1 
        await message.channel.send("以下の予定を削除します。よろしいですか？['y''Y' / 'n''N']")
        await message.channel.send(database_d[del_msg])
        yn = await client.wait_for("message",check=check_1)
        yn_c = yn.content
        if "y" in yn_c or "Y" in yn_c or 'ｙ' in yn_c or 'Ｙ' in yn_c:
            await message.channel.send("予定を削除しました。")
            del database_d[del_msg]
            with open('database.csv','w')as db_d:
                whiter = csv.writer(db_d)
                whiter.writerows(database_d)
        elif 'y' not in yn_c or 'Y' not in yn_c or 'ｙ' not in yn_c or 'Ｙ' not in yn_c:
            await message.channel.send("もう一度最初からやり直してください。")        


    if message.content.startswith("!edit"):
        init = True
        cnntt= 0
        channel = message.channel
        def check_2(msg):
            return msg.author == message.author
        await message.channel.send("予定の再設定を実行します！\n上から何番目かを入力してください。")
        with open('database.csv') as db_r:
            reader = csv.reader(db_r)
            database_e = [row for row in reader]
            print("database_e")
            print(database_e)
        while len(database_e) > cnntt:
            edit_mes = discord.Embed(title=database_e[cnntt][0]+" : "+database_e[cnntt][1],description= database_e[cnntt][2],color = discord.Colour.from_rgb(47,32,66))
            await channel.send(embed = edit_mes)
            cnntt = cnntt + 1
        edit_msg = await client.wait_for("message", check=check_2)
        edit_msg = int(edit_msg.content)
        edit_msg = edit_msg - 1 
        await message.channel.send("以下の予定を変更します。よろしいですか？['y''Y' / 'n''N']")
        await message.channel.send(database_e[edit_msg])
        ye = await client.wait_for("message",check=check_2)
        ye_c = ye.content
        if 'y' in ye_c or 'Y' in ye_c or 'ｙ' in ye_c or 'Ｙ' in ye_c:
            del database_e[edit_msg]
            await message.channel.send("予定を再度入力してください。")
            await message.channel.send("予定の名称を再設定します。入力してください。")
            title = await client.wait_for("message",check=check_2)
            await message.channel.send("予定の時刻を再設定します。入力してください。")
            time = await client.wait_for("message",check=check_2)
            await message.channel.send("予定のコメントを再設定します。入力してください。")
            comm = await client.wait_for("message",check=check_2)
            e = (title.content,time.content,comm.content)
            database_e.append(e)
            last = len(database_e)
            last = last -1 
            await message.channel.send("予定を再設定しました。5秒後にlistコマンドを自動実行します。")
            await message.channel.send(database_e[last])
            with open('database.csv','w') as db_e:
                whiter = csv.writer(db_e)
                whiter.writerows(database_e)
            await asyncio.sleep(5)
            cnt = 0
            channel = message.channel
            await message.channel.send("listコマンドを実行します。")
            if os.path.isfile('database.csv') == True:
                with open('database.csv') as db_r:
                    reader = csv.reader(db_r)
                    database = [row for row in reader] 
            while len(database) > cnt:
                list_mes = discord.Embed(title=database[cnt][0]+" : "+database[cnt][1],description= database[cnt][2],color = discord.Colour.from_rgb(65,105,225))
                await channel.send(embed = list_mes)
                cnt = cnt + 1
        elif 'y' not in ye_c or 'Y' not in ye_c or 'ｙ' not in ye_c or 'Ｙ' not in ye_c:
            await message.channel.send("もう一度最初からやり直してください。")   

    if message.content.startswith("!allclear"):
        init = True
        channel = message.channel
        def check_5(msg):
            return msg.author == message.author
        await message.channel.send("CSVに登録されている予定を全削除しますよろしいですか？['y''Y' / 'n''N']")
        ych = await client.wait_for("message",check=check_5)
        ye_r = ych.content
        if 'y' in ye_r or 'Y' in ye_r or 'ｙ' in ye_r or 'Ｙ' in ye_r:
            os.remove("database.csv")
            with open("database.csv",'x'):
                pass
            await message.channel.send("CSVファイルを削除しました。")
        elif 'y' not in ye_r or 'Y' not in ye_r or 'ｙ' not in ye_r or 'Ｙ' not in ye_r:
            await message.channel.send("もう一度最初からやり直してください。")  

    #幸せになれるコマンド。気分で追加した。後悔はしていない。
    #これもオススメ:YouTube{https://www.youtube.com/watch?v=nDtj-2qnTXk}
    if message.content.startswith("!BOSS"):
        channel = message.channel
        sel = random.randint(0,10)
        print(sel)
        if sel == 0:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url='https://thumbs.gfycat.com/OldfashionedWindyBlackwidowspider-size_restricted.gif')
            await channel.send(embed=boss)
        elif sel == 1:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url='https://media1.tenor.com/images/af3cc3f2250b19e53f61c7fb08f159b8/tenor.gif?itemid=8522272')            
            await channel.send(embed=boss)
        elif sel == 2:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url='https://i.pinimg.com/originals/9b/42/9e/9b429ee4e8247db39f7c160072e62b36.gif')
            await channel.send(embed=boss)
        elif sel == 3:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url='https://37.media.tumblr.com/d0b238b5b4ac08b0b8c6fe68901a550e/tumblr_n3ot1cmvQs1sd4mmco1_250.gif')
            await channel.send(embed=boss)
        elif sel == 4:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url='https://64.media.tumblr.com/f488d44c8caa4027ca6d99735c907081/tumblr_mvqt23cF6N1rigjtfo1_500.gif')
            await channel.send(embed=boss)
        elif sel == 5:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url= 'https://i.imgur.com/eO73wGT.gif')
            await channel.send(embed=boss)
        elif sel == 6:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url='https://thumbs.gfycat.com/PoorGenerousHamster-size_restricted.gif')
            await channel.send(embed=boss)
        elif sel ==7:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url='https://thumbs.gfycat.com/EmbarrassedThunderousArmyant-max-1mb.gif')
            await channel.send(embed=boss)
        elif sel == 8:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url='https://2.bp.blogspot.com/-iqZgNDTUR5U/WWfj0hPEeuI/AAAAAAAABuc/gSqYmbBrgPc7mTIrbnKyKfHMnYVqljceACLcBGAs/s640/30Th%2BBrithday%2BMGSFOB.gif')
            await channel.send(embed=boss)
        elif sel == 9:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url='https://media.tenor.com/images/f3ebbd7be8a26a7dc2ef9e371dd81e47/tenor.gif')
            await channel.send(embed=boss)
        elif sel ==10:
            boss = discord.Embed(name="",description="",color=discord.Color.from_rgb(0,0,0))
            boss.set_image(url='https://thumbs.gfycat.com/IlliterateYellowishAmericanlobster-size_restricted.gif')
            await channel.send(embed=boss)




    if message.content.startswith("!help"):
        channel = message.channel
        init = True
        help_mes = discord.Embed(title="コマンド一覧を表示します。",color=discord.Colour.from_rgb(166,242,0))
        help_mes.add_field(name="!set",value="新規の予定を設定します。\n日時のみを設定したい場合は時刻は0：0と入力してください\nコメントは一行で何もない場合はNoneと入力をお願いします。",inline=False)
        help_mes.add_field(name="!del",value="登録されている予定の削除を行います。",inline=False)
        help_mes.add_field(name="!edit",value="登録されている予定の再登録を行います。",inline=False)
        help_mes.add_field(name="!list",value="登録されている予定の一覧を表示します。",inline=False)
        help_mes.add_field(name="!allclear",value="登録されている予定を全削除します。",inline=False)
        await message.channel.send(embed=help_mes)










client.run(TOKEN)