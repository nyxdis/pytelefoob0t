#  Copyright 2017 Christoph Mende
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import time

import telepot
from telepot.loop import MessageLoop

import plugin_loader

commands = {}
username = None

for i in plugin_loader.get_plugins():
    print('Loading plugin ' + i['name'])
    plugin = plugin_loader.load_plugin(i)
    commands.update(plugin.commands)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    # reject non-text messages
    if content_type != 'text':
        return

    # split message in command (first word) and args (rest)
    argv = msg['text'].strip().split(' ', 1)
    command = argv[0].lower()
    args = None
    if len(argv) == 2:
        args = argv[1]

    # reject non-commands
    if not command.startswith('/'):
        return

    # strip / from command
    command = command[1:]

    # strip username from command
    if command.endswith('@'+username):
        command = command[:-len(username)-1]

    # search for plugin handling command
    for c in commands:
        if c != command:
            continue

        # found it
        retval = commands[c](args)
        bot.sendMessage(chat_id, retval)

bot = telepot.Bot("410481893:AAFOD7G_hoWsQNMrbEiw4ARqUlb-LzvWjnY")
username = bot.getMe()['username']
MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)