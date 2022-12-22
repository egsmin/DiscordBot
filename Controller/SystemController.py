import asyncio
import datetime
import random
from Controller.MessageController import MessageController


class SystemController:
    def __init__(self, ctx):

        self.ctx = ctx

        self.message_controller = MessageController(ctx, self)

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
        self.ready_members = []

        self.bunch(after_learning=False)

        self.phase = None

        self.learning = True
        self.stopped = False

        self.learning_duration = 30
        self.pause_duration = 5
        self.mute = False

    async def start(self):
        await self.message_controller.initialize()

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

    # Settings Methods

    async def mute_members(self):
        for member in self.members:
            await member.edit(mute=True)

    async def unmute_members(self):
        for member in self.members:
            await member.edit(mute=False)

    # Learning Session

    async def learning_session(self):
        async def learn_phase():
            timestamp_now = int(datetime.datetime.now().timestamp())
            timestamp_end = timestamp_now + self.learning_duration * 60

            time_to_wait = (self.learning_duration * 60) / 10

            for i in range(10):
                if not self.stopped:
                    await self.message_controller.show_learning(i, timestamp_end)
                    await asyncio.sleep(time_to_wait)
                else:
                    break

        async def pause_phase():
            timestamp_now = int(datetime.datetime.now().timestamp())
            timestamp_end = timestamp_now + self.pause_duration * 60

            time_to_wait = (self.pause_duration * 60) / 10

            for i in range(10):
                if not self.stopped:
                    await self.message_controller.show_pause(i, timestamp_end, self.global_points)
                    await asyncio.sleep(time_to_wait)
                else:
                    break

        self.stopped = False

        while True:
            if not self.stopped:
                if self.learning:
                    try:
                        if self.mute:
                            await self.mute_members()

                        self.phase = asyncio.create_task(learn_phase())
                        await self.phase
                    except asyncio.CancelledError:
                        pass
                    finally:
                        await self.unmute_members()
                        self.bunch(after_learning=True)
                        self.learning = False

                else:
                    print(self.global_points)
                    try:
                        self.phase = asyncio.create_task(pause_phase())
                        await self.phase
                    except asyncio.CancelledError:
                        pass
                    finally:
                        self.learning = True

            else:
                break

    async def skip_phase(self):
        self.phase.cancel()

    async def stop_session(self):
        self.stopped = True
        self.phase.cancel()
        await self.message_controller.show_start_menu()

    # Notification Methods

    # # Start Menu Bundle

    async def start_menu_button_start(self):
        await self.message_controller.show_pre(self.ready_members)

    async def start_menu_button_intro(self):
        await self.message_controller.show_intro()

    async def start_menu_button_konfiguration(self):
        await self.message_controller.show_conf()

    async def start_menu_button_beenden(self):
        await self.message_controller.show_end()

    # # Conf Bundle

    async def conf_select_lerndauer(self, selected):
        self.learning_duration = int(selected)

    async def conf_select_pausedauer(self, selected):
        self.pause_duration = int(selected)

    async def conf_select_stummen_nicht_stummen(self, mute_members):
        self.mute = mute_members

    async def conf_button_zurueck(self):
        await self.message_controller.show_start_menu()

    # # Intro Bundle

    async def intro_button_zurueck(self):
        await self.message_controller.show_start_menu()

    async def intro_button_tutorial(self):
        pass
        # TODO: TUTORIAL

    # # Pre Bundle

    async def pre_button_bereit(self, presser):
        if presser.name not in [i.name for i in self.ready_members]:
            self.ready_members.append(presser)

        if all([i.name in [j.name for j in self.ready_members] for i in self.members]):
            await self.learning_session()
        else:
            await self.message_controller.show_pre(self.ready_members)
        # TODO: READY LOGIC

    # # Learn Bundle

    async def learn_button_stop(self):
        await self.stop_session()

    async def learn_button_phase_ueberspringen(self):
        await self.skip_phase()

    async def learn_button_melden(self, reporter):
        name_of_reporter = reporter.name
        name_of_partner = self.partners[name_of_reporter]

        if self.current_points[name_of_partner] > 0:
            self.current_points[name_of_partner] -= 1

    # # Pause Bundle

    async def pause_button_stop(self):
        await self.stop_session()

    async def pause_button_phase_ueberspringen(self):
        await self.skip_phase()

    async def pause_button_melden(self):
        pass

    async def pause_select_stummen_nicht_stummen(self, mute_members):
        self.mute = mute_members
