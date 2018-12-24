"""NOTE: Not currently included in Lion.
Written by Hayden Inghem.
"""
import discord

COMMAND = "gulag"

listToPrint = list()
#!gulag @dankpotato4304 being a dick 

async def command_gulag(client,message):
    try:
        cmd = parse_command(message.content)

        userToGulag  = cmd['UserName']
        
        reason = ' '.join((cmd['Reason']))
        
        listToPrint.append(message.author)
        
        listToPrint.append(userToGulag)
        
        listToPrint.append(reason)
        
    
        await print_gulag(client, message, listToPrint)
        
        
    except Exception as error:
        await client.send_message(message.channel, str(error))    


async def print_gulag(client, message, listToPrint):
    # this needs to be formatted to have some cool colors otherwise it wont be as funny
    gulag = "{} would like to send {} to the gulag for the reason of:{}".format(listToPrint[0],listToPrint[1],listToPrint[2])
                                         
    await client.send_message(message.channel, gulag)
    
    await client.delete_message(message)
    
def create_user_mention(user):
    return '<@{}>'.format(user.id)        
    
def parse_command(message):
    parts = message.split(' ')
    if len(parts) <= 1:
        raise Exception(
            'Roles sub-command not given. Run `!roles help` for usage details')

    return {
        'UserName': parts[1],
        'Reason': parts[2:],
    }
