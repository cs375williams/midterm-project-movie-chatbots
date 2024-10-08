"""
The REPL loop file. 

You do not need to modify anything in this file. 
"""
import argparse
import cmd
import logging
import sys

logging.basicConfig()
logger = logging.getLogger(__name__)

# Uncomment me to see which REPL commands are being run!
# logger.setLevel(logging.DEBUG)

from chatbot import Chatbot

# Modular ASCII font from http://patorjk.com/software/taag/
HEADER = """Welcome to Willimas College CS 375's                                  
 _______  __   __  _______  _______  _______  _______  _______ 
|       ||  | |  ||   _   ||       ||  _    ||       ||       |
|       ||  |_|  ||  |_|  ||_     _|| |_|   ||   _   ||_     _|
|       ||       ||       |  |   |  |       ||  | |  |  |   |  
|      _||       ||       |  |   |  |  _   | |  |_|  |  |   |  
|     |_ |   _   ||   _   |  |   |  | |_|   ||       |  |   |  
|_______||__| |__||__| |__|  |___|  |_______||_______|  |___|  
"""

description = 'Simple Read-Eval-Print-Loop that handles the input/output ' \
              'part of the conversational agent '


class REPL(cmd.Cmd):
    """Simple REPL to handle the conversation with the chatbot."""
    prompt = '> '
    doc_header = ''
    misc_header = ''
    undoc_header = ''
    ruler = '-'

    def __init__(self):
        super().__init__()

        self.chatbot = Chatbot()
        self.name = self.chatbot.name
        self.bot_prompt = '\001\033[96m\002%s> \001\033[0m\002' % self.name

        self.greeting = self.chatbot.greeting()
        self.intro = self.chatbot.intro() + '\n' + self.bot_prompt + \
                     self.greeting
        self.debug = False
        self.debug_chatbot = False

    def cmdloop(self, intro=None):
        logger.debug('cmdloop(%s)', intro)
        return super().cmdloop(intro)

    def preloop(self):
        logger.debug('preloop(); Chatbot %s created and loaded', self.chatbot)
        print(HEADER)
        self.debug_chatbot = False

    def postloop(self):
        goodbye = self.chatbot.goodbye()
        print(self.bot_says(goodbye))

    def onecmd(self, s):
        logger.debug('onecmd(%s)', s)
        if s:
            return super().onecmd(s)
        else:
            return False  # Continue processing special commands.

    def emptyline(self):
        logger.debug('emptyline()')
        return super().emptyline()

    def default(self, line):
        logger.debug('default(%s)', line)
        # Stop processing commands if the user enters :quit
        if line == ":quit":
            return True
        else:
            response = self.chatbot.process(line)
            print(self.bot_says(response))

    def precmd(self, line):
        logger.debug('precmd(%s)', line)
        return super().precmd(line)

    def postcmd(self, stop, line):
        logger.debug('postcmd(%s, %s)', stop, line)

        if line == ':quit':
            return True
        elif line.lower() == 'who are you?':
            self.do_secret(line)
        elif ':debug on' in line.lower():
            print('enabling debug...')
            self.debug_chatbot = True
        elif ':debug off' in line.lower():
            print('disabling debug...')
            self.debug_chatbot = False

        # Debugging the chatbot
        if self.debug_chatbot:
            print(self.chatbot.debug(line))

        return super().postcmd(stop, line)

    def bot_says(self, response):
        return self.bot_prompt + response

    def do_prompt(self, line):
        """Set the interactive prompt."""
        self.prompt = line + ': '

    def do_secret(self, line):
        """Could it be... a secret message?"""
        story = """A long time ago, in a remote land, a young developer named 
        Alberto Caso managed to build an ingenious and mysterious chatbot... 
        Now it's your turn! """
        print(story)


if __name__ == '__main__':
    #########################
    # ADDED FOR TESTING     #
    #########################
    class Tee(object):
        # Modified from
        # https://stackoverflow.com/questions/34366763/input-redirection-with-python
        def __init__(self, input_handle, output_handle):
            self.input = input_handle
            self.output = output_handle

        def readline(self):
            result = self.input.readline()
            self.output.write(result)
            self.output.write('\n')
            self.output.flush()

            return result

        # Forward all other attribute references to the input object.
        def __getattr__(self, attr):
            return getattr(self.input, attr)


    if not sys.stdin.isatty():
        sys.stdin = Tee(input_handle=sys.stdin, output_handle=sys.stdout)

    #########################
    # END TESTING CODE      #
    #########################
    repl = REPL()
    repl.cmdloop()