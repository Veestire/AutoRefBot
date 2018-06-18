from discord.ext import commands
from .utils.chat_formatting import box
from .utils.dataIO import dataIO
from .utils import checks
from __main__ import user_allowed, send_cmd_help
from copy import copy
import os
import discord


class ircintegration:
	def __init__(self, bot):
		self.bot = bot

	#empty cog for future development

def setup(bot):
	bot.add_cog(ircintegration(bot))