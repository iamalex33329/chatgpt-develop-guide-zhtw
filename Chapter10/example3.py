from googlesearch import search

import discord
import openai
import ApiKey
import re

openai.api_key = ApiKey.OPENAI_API_KEY

hist = []
backtrace = 2


def get_reply(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = response["choices"][0]["message"]["content"]
    except openai.OpenAIError as err:
        reply = f"An {err.error.type} error occurred\n{err.error.message}"
    return reply


def chat(sys_msg, user_msg, use_web):
    web_res = []
    if use_web:
        content = "The following are established facts:\n"
        for res in search(user_msg, advanced=True, num_results=5):
            content += f"Title: {res.title}\nSummary: {res.description}\n\n"
        content += "Please answer the following questions based on the above facts:\n"
        web_res = [{"role": "user", "content": content}]

    web_res.append({"role": "user", "content": user_msg})
    while len(hist) >= 2 * backtrace:
        hist.pop(0)
    reply = get_reply(hist + web_res + [{"role": "system", "content": sys_msg}])
    hist.append({"role": "user", "content": user_msg})
    while len(hist) >= 2 * backtrace:
        hist.pop(0)
    hist.append({"role": "assistant", "content": reply})
    if use_web:
        reply = f"The following reply is based on internet information:\n\n{reply}"
    return reply


prompt_for_check_web = """
{}
```
{}
```
If needed, please clearly reply with "Y"; if not, clearly reply with "N", do not add any extra words.
"""


def check_tool(prompt, msg):
    reply = get_reply(
        [{"role": "user", "content": prompt_for_check_web.format(prompt, msg)}]
    )
    print(reply)
    return reply == "Y"


token = ApiKey.DISCORD_BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
pattern_mention = re.compile(r"\s{0,1}<@\d+>\s")


@client.event
async def on_ready():
    print(f"{client.user} is logged in")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not client.user in message.mentions:
        return

    msg = re.sub(pattern_mention, "", message.content)
    draw_pict = check_tool(
        "Confirm whether drawing a picture is required for the following:", msg
    )
    if draw_pict:
        response = openai.Image.create(prompt=msg, n=1, size="1024x1024")
        image_url = response["data"][0]["url"]
        await message.channel.send(image_url)
        return

    use_web = check_tool(
        "If I want to know the following, confirm if internet search is needed:", msg
    )
    reply_msg = chat("Assistant", msg, use_web)
    await message.channel.send(f"{message.author.mention} {reply_msg}")


client.run(token)
