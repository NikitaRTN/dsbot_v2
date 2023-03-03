import discord
from discord.ext import commands,tasks
import random
import time
import openai
import nacl
openai.api_key = "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"
bot = commands.Bot(command_prefix='$', intents = discord.Intents.all())

import nest_asyncio
nest_asyncio.apply()
#---------------------
@bot.event  # Создание голосового канала
async def on_voice_state_update(member, before, after):
  if after.channel != None:
      if after.channel.id == 913022726275465216:
        category = await member.guild.create_category(f'{member.display_name}')
        channel3 = await member.guild.create_voice_channel(
          name=f' Канал {member.display_name}', category=category)
        await member.move_to(channel3)
        channel4 = await member.guild.create_text_channel(
          name=f' Чат-{member.display_name}', category=category)
        #await category.set_permissions(member.guild.default_role, view_channel=False)
        await category.set_permissions(member, view_channel=True, kick_members=True)
        print("Создан голосовой канал: ", {member})
        embed = discord.Embed(
            title=('Создание канала'),
            description=f'{member.mention} создал Голосовой чат - Канал {member.display_name}',
            color=0xffaf00)
        await channel4.send(embed=embed)
        def check(x, y, z):
          return len(channel3.members) == 0
        await bot.wait_for('voice_state_update', check=check)
        await channel3.delete()
        await channel4.delete()
        await category.delete()
@bot.event

async def on_raw_reaction_add(payload):
  if payload.guild_id == 1045795259214467142:
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if message.author.id == bot.user.id:
      reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
      inter_totale = ["✅", "❌", "👍", "👎"]
      if str(payload.emoji) in inter_totale:
          user = await bot.fetch_user(payload.user_id)
          if str(payload.emoji) == "✅" or str(payload.emoji) == "👍":
              await channel.send(f"Спасибо за отзыв, {user.name}. Я рад что вас устроил мой ответ!")
          elif str(payload.emoji) == "❌" or str(payload.emoji) == "👎":
              await channel.send(f"Спасибо за отзыв, {user.name}. Я попробую через месяц не повторять тех же ошибок!")
          await reaction.remove(payload.member)

async def on_voice_state_update(member, before, after):
  if after.channel != None:
      if after.channel.id == 913022726275465216:
        category = await member.guild.create_category(f'{member.display_name}')
        channel3 = await member.guild.create_voice_channel(
          name=f' Канал {member.display_name}', category=category)
        await member.move_to(channel3)
        channel4 = await member.guild.create_text_channel(name=f' Чат-{member.display_name}', category=category)
        await category.set_permissions(member.guild.default_role, view_channel=True)
        await category.set_permissions(member, view_channel=True, kick_members=True)
        print("Создан голосовой канал", {member})
        embed = discord.Embed(
            title=('Создание канала'),
            description=f'{member.mention} создал Голосовой чат - Канал {member.display_name}',
            color=0xffaf00)
        await channel4.send(embed=embed)
        def check(x, y, z):
          return len(channel3.members) == 0
        await bot.wait_for('voice_state_update', check=check)
        await channel3.delete()
        await channel4.delete()
        await category.delete()
        
        
@bot.command()  # Очистка чата
async def clear(ctx, amount=None, administrator=True):
    amounts = int(amount)
    amount = int(amount) + 1
    await ctx.channel.purge(limit=int(amount))
    author = ctx.message.author
    if amounts == 1:
        embed = discord.Embed(
            title=('Очистка чата'),
            description=f'{author.mention} очистил чат на {amounts} сообщение',
            color=0xffaf00)
    if 1 < amounts < 5:
        embed = discord.Embed(
            title=('Очистка чата'),
            description=f'{author.mention} очистил чат на {amounts} сообщения',
            color=0xffaf00)
    if amounts > 4:
        embed = discord.Embed(
            title=('Очистка чата'),
            description=f'{author.mention} очистил чат на {amounts} сообщений',
            color=0xffaf00)
    await ctx.send(embed=embed)
@bot.command()
async def rand(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel
    author = ctx.message.author
    await ctx.send("Введите первое число:")
    msg1 = await bot.wait_for("message", check=check)
    await ctx.send("Введите второе число:")
    msg2 = await bot.wait_for("message", check=check)
    x = int(msg1.content)
    y = int(msg2.content)
    num = random.randint(x, y)
    await ctx.channel.purge(limit=int(5))
    embed=discord.Embed(title="$rand", color=0xffaf00)
    embed.add_field(name=(f'Генератор числа'), value=(f'от {x} до {y}'), inline=False)
    embed.add_field(name="Ваше число:", value=(f'{num}'), inline=False)
    embed.add_field(name="Команду выполнил:", value=(f'{author.mention}'), inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def rnd(ctx):
    author = ctx.message.author
    x = int(1)
    y = int(6)
    num1 = random.randint(x, y)
    num2 = random.randint(x, y)
    embed=discord.Embed(title="$rnd", color=0xffaf00)
    embed.add_field(name="Кубик 1:", value=(f'{num1}'), inline=True)
    embed.add_field(name="Кубик 2:", value=(f'{num2}'), inline=True)
    embed.add_field(name="Команду выполнил:", value=(f'{author.mention}'), inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def ai(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    if (ctx.channel.id == 1046043688658292776):
      await ctx.send("Введите запрос: ")
      msg1 = await bot.wait_for("message", check=check)
      arg = str(msg1.content)
      prompt = arg+":"
      response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=1500, temperature=0.3, top_p=1, frequency_penalty=0, presence_penalty=0)
      msg = await ctx.send(response.choices[0].text)
      print(response.choices[0].text)
    if (ctx.channel.id != 1046043688658292776):
      if (ctx.channel.id != 1045891526506594324):
        if (ctx.channel.id != 1046033620328009748):
          if (ctx.channel.id != 1046845450893918238):
            await ctx.send('Эта комманда работает только в https://discord.gg/8pCVsBNMKP')
bot.run('OTM4NDQ3OTM1ODAzMzkyMDQx.GoJbQ1.MSrEWhkLyumenoP5ZRg4MDF96s1feR-0z9S-iM')
