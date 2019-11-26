from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import PeerChannel,InputPeerChannel
from config import api_id,api_hash,phone
import sys
import csv
import traceback
import time

 
client = TelegramClient(phone, api_id, api_hash)
 
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))
 
users_add = []
with open("members.csv", encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user_ad = {}
        user_ad['username'] = row[0]
        user_ad['id'] = int(row[1])
        user_ad['access_hash'] = int(row[2])
        user_ad['name'] = row[3]
        users_add.append(user_ad)
 
get_dialogs = GetDialogsRequest(
    offset_date=None,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=30,
    hash =0
)
dialogs = client(get_dialogs)

counts = {}

users = {}
chats = {}
data = []

for u in dialogs.users:
    users[u.id] = u

for c in dialogs.chats:
    chats[c.id] = c

for d in dialogs.dialogs:
    peer = d.peer
    if isinstance(peer, PeerChannel):
        id = peer.channel_id
        channel = chats[id]
        access_hash = channel.access_hash
        name = channel.title
        data.append({"channel_name":name,"access_hash":access_hash,"channel_id":id})

print('=====>Choose a group to add members you must be admin of this group<=====')
i=0
for group in data:
    namee = group['channel_name']
    print(str(i) + '- ' + namee)
    i+=1   
g_index = input("Enter a Number: ")
target_group=data[int(g_index)]
 
target_group_entity = InputPeerChannel(target_group['channel_id'],target_group["access_hash"])
 
mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
 
for user in users_add:
    try:
        print ("Adding {}".format(user['id']))
        time.sleep(1)
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        print("Waiting 2 Seconds...")
        time.sleep(3)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue



