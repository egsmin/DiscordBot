import asyncio
import random


class SystemController:
    def __init__(self, ctx):

        self.ctx = ctx
        self.guild = ctx.guild
        self.text_channel = ctx.channel

        # Get Voice-Channel with most members in it
        voice_channels: list = self.guild.voice_channels
        copy_vcs = voice_channels.copy()
        copy_vcs.sort(key=lambda x: len(x.members), reverse=True)
        self.voice_channel = copy_vcs[0]

        self.members = self.get_members()
        self.global_points = {}
        self.current_points = {}
        self.partners = {}

        self.reset_global_points()
        self.reset_current_points()
        self.mix_the_partners()
        a=2

        self.phase = None

        self.learning = True
        self.stopped = False

    # Member Methods

    def get_members(self):
        return self.voice_channel.members

    def refresh_members(self):
        self.members = self.get_members()

    def reset_global_points(self):
        temp_dict = {}
        self.refresh_members()

        for m in self.members:
            temp_dict[m.name] = 0

        self.global_points = temp_dict

    def reset_current_points(self):
        temp_dict = {}
        self.refresh_members()

        for m in self.members:
            temp_dict[m.name] = 10

        self.current_points = temp_dict

    def mix_the_partners(self):
        mixed = random.sample([i.name for i in self.members], len(self.members))
        temp_dict = {}

        for i in range(len(self.members)):
            if i != len(self.members)-1:
                temp_dict[mixed[i]] = mixed[i+1]
            else:
                temp_dict[mixed[i]] = mixed[0]

        self.partners = temp_dict

    # Notifications


