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

        self.bunch(after_learning=False)

        self.phase = None

        self.learning = True
        self.stopped = False

        self.learning_duration = 30
        self.pause_duration = 5

    # Member Methods

    def get_members(self):
        return self.voice_channel.members

    def refresh_members(self):
        self.members = self.get_members()

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
            if i != len(self.members) - 1:
                temp_dict[mixed[i]] = mixed[i + 1]
            else:
                temp_dict[mixed[i]] = mixed[0]

        self.partners = temp_dict

    def calculate_points(self):
        if all([points == 10 for points in self.current_points.values()]):
            for key_iter in self.global_points.keys():
                self.global_points[key_iter] += 20

        else:
            for key_iter in self.current_points.keys():
                if self.current_points[key_iter] == 10:
                    self.global_points[key_iter] += 15
                else:
                    self.global_points[key_iter] += self.current_points[key_iter]

    def refresh_global_points(self):
        self.refresh_members()

        # Check if someone new has joined
        for m in self.members:
            if m.name not in self.global_points.keys():
                self.global_points[m.name] = 0

        # Check if someone has left
        cop_dict = self.global_points.copy()
        for m in cop_dict.keys():
            if m not in [i.name for i in self.members]:
                self.global_points.pop(m)

    def bunch(self, after_learning=False):
        self.refresh_members()

        if after_learning:
            self.calculate_points()

        self.refresh_global_points()
        self.reset_current_points()
        self.mix_the_partners()

    # Notification Methods

    # # Start Menu Bundle

    def start_menu_button_start(self):
        pass

    def start_menu_button_intro(self):
        pass

    def start_menu_button_konfiguration(self):
        pass

    def start_menu_button_beenden(self):
        pass

    # # Conf Bundle

    def conf_select_lerndauer(self):
        pass

    def conf_select_pausedauer(self):
        pass

    def conf_select_stummen_nicht_stummen(self):
        pass

    def conf_button_zurueck(self):
        pass

    # # Intro Bundle

    def intro_button_zurueck(self):
        pass

    def intro_button_tutorial(self):
        pass

    # # Pre Bundle

    def pre_button_bereit(self):
        pass

    # # Learn Bundle

    def learn_button_stop(self):
        pass

    def learn_button_phase_ueberspringen(self):
        pass

    def learn_button_melden(self):
        pass

    # # Pause Bundle

    def pause_button_stop(self):
        pass

    def pause_button_phase_ueberspringen(self):
        pass

    def pause_button_melden(self):
        pass

    def pause_select_stummen_nicht_stummen(self):
        pass
    