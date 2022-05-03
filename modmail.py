import discord
import json
import db, ticket_embed

with open('./config.json', 'r') as config_json:
    config = json.load(config_json)

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    modmail_channel = discord.utils.get(client.get_all_channels(), id=config['channel'])
    message_member = client.get_guild(config['guild']).get_member(message.author.id)

    await ticket_embed.channel_embed(modmail_channel, message, message_member)
    await ticket_embed.user_embed(channel, message)

    if isinstance(channel, discord.channel.DMChannel):
        if message.content == 'New':
            await channel.send(db.open_ticket(message_member.id))
        elif message.content == 'Get':
            await channel.send(db.get_ticket_by_user(message_member.id))
        elif message.content == 'Close':
            ticket_id = db.get_ticket_by_user(message_member.id)
            await channel.send(db.close_ticket(ticket_id))


def ready():
    if db.init():
        print('Database sucessfully initialized!')
    else:
        print('Error while initializing database!')
    
    if "channel" not in config:
        print('Failed to find Modmail text channel from provided ID.')
    
    if "guild" not in config:
        print('Failed to find Guild from provided ID.')

ready()

client.run(config['token'])