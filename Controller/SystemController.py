import asyncio
import datetime
import random
from Controller.MessageController import MessageController


class SystemController:
    def __init__(self, ctx):

        # Kontext der Nachricht (Referenz zur Umgebung in Discord)
        self.ctx = ctx

        # MessageController dient zur zentralen Steuerung der Ansicht der Nachricht
        self.message_controller = MessageController(ctx, self)

        # Referenz zum aktuellen Server
        self.guild = ctx.guild

        # Referenz zum Textkanal
        self.text_channel = ctx.channel

        # Bestimme Sprachkanal mit den meisten Members
        voice_channels: list = self.guild.voice_channels
        copy_vcs = voice_channels.copy()
        copy_vcs.sort(key=lambda x: len(x.members), reverse=True)
        self.voice_channel = copy_vcs[0]

        # Referenz zu den Members des Sprachkanals
        self.members = self.get_members()

        # Gesamtpunktzahl
        self.global_points = {}

        # Punktzahl pro Runde (wird nach jeder Runde zurueckgesetzt)
        self.current_points = {}

        # Dictionary fuer die Bestimmung der jeweiligen Partner, die beobachtet werden sollen
        self.partners = {}

        # Liste der Members, die in der Pre-Ansicht "Bereit" geklickt haben
        self.ready_members = []

        # Asynchrones Objekt, fuer Prozessverwaltung der aktuellen Phase (Lernphase | Pause)
        self.phase = None

        # Statusvariable (True, wenn die Teilnehmer lernen
        self.learning = True

        # Ist True, wenn Lernprozess gestoppt werden soll
        self.stopped = False

        # True in der ersten Runde, sonst immer False
        self.fist = True

        # Dauer einer Lernphase
        self.learning_duration = 30

        # Dauer einer Pause
        self.pause_duration = 5

        # True, wenn ausgewaehlt wurde, dass die Lernenden waehrend der Lernphasen gestummt werden wollen.
        self.mute = False

    async def start(self):
        """ Startfunktion fuer den Systemcontroller

        :return:
        """
        await self.bunch(with_calculation=False)
        await self.message_controller.initialize()

    # ##############
    # Member Methods
    # ##############
    def get_members(self):
        """ Hilfsfunktion, um die Member des aktuellen Sprachkanals zu bestimmen

        :return: Member des aktuellen Sprachkanals
        """
        return [i for i in self.voice_channel.members]  # if i.name != "egsm1n"]

    def refresh_members(self):
        """ Hilfsfunktion, um die Memberliste zu aktualisieren.

        Diese Methode wird benoetigt, wenn neue Lernende dazu kommen.

        :return:
        """
        self.members = self.get_members()

    def reset_current_points(self):
        """ Punktzahl pro Runde wird aktualisiert

        :return:
        """
        temp_dict = {}
        self.refresh_members()

        for m in self.members:
            temp_dict[m.name] = 10

        self.current_points = temp_dict

    async def mix_the_partners_and_write(self):
        """ Hilfsfunktion, um Dictionary von Partnern durch Zufall zu erstellen und die Teilnehmer zu benachrichtigen

        :return:
        """
        mixed = random.sample([i.name for i in self.members], len(self.members))
        temp_dict = {}

        for i in range(len(self.members)):
            if i != len(self.members) - 1:
                temp_dict[mixed[i]] = mixed[i + 1]
            else:
                temp_dict[mixed[i]] = mixed[0]

        self.partners = temp_dict

        for i in self.partners.keys():
            p = None
            for m in self.members:
                if m.name == i:
                    p = m
                    break

            await p.send(content="Dein Partner ist: " + self.partners[i])

    def calculate_points(self):
        """ Berechnet die Punktzahl für eine Runde.

        :return:
        """
        if all([points == 10 for points in self.current_points.values()]):
            for key_iter in self.global_points.keys():
                self.global_points[key_iter] += 20

        else:
            for key_iter in self.current_points.keys():
                if self.current_points[key_iter] == 10:
                    self.global_points[key_iter] += 15
                else:
                    self.global_points[key_iter] += self.current_points[key_iter]

    async def refresh_global_points(self):
        """ Berechnet die neue Punktzahl unter Betracht der Punkte der aktuellen Runde

        :return:
        """

        self.refresh_members()
        changed = False

        # Checkt, ob jemand neues dazu gekommen ist
        for m in self.members:
            if m.name not in self.global_points.keys():
                self.global_points[m.name] = 0
                changed = True

        # Check ob jemand verlassen hat
        cop_dict = self.global_points.copy()
        for m in cop_dict.keys():
            if m not in [i.name for i in self.members]:
                self.global_points.pop(m)
                changed = True

        if changed and not self.fist:
            await self.mix_the_partners_and_write()

    async def bunch(self, with_calculation=False):
        """ Zusammenfassung mehrerer Methoden

        :param with_calculation: True, wenn Punkte ebenfalls aktualisiert werden sollen
        :return:
        """
        self.refresh_members()

        if with_calculation:
            self.calculate_points()

        await self.refresh_global_points()
        self.reset_current_points()

    async def write_everyones_partner(self):
        """ Hilfsmethode, um den Teilnehmern zu schreiben, wer ihr Partner ist

        :return:
        """
        for i in self.partners.keys():
            p = None
            for m in self.members:
                if m.name == i:
                    p = m
                    break

            await p.send(content="Dein Partner ist: " + self.partners[i])

    async def admonish(self, reported):
        """ Methode, um jemanden zu warnen, dass er beim ablenkenden Verhalten erwischt wurde

        :param reported:
        :return:
        """
        for i in self.members:
            if i.name == reported:
                await i.send("Du wurdest erwischt. Konzentriere dich wieder auf deine Aufgabe!")
                break

    # ################
    # Settings Methods
    # ################

    async def mute_members(self):
        """ Methode, um die Teilnehmer zu stummen

        :return:
        """

        for member in self.members:
            try:
                await member.edit(mute=True)
            except Exception:
                pass

    async def unmute_members(self):
        """ Methode, um die Teilnehmer zu stummen

        :return:
        """

        for member in self.members:
            try:
                await member.edit(mute=False)
            except Exception:
                print("Catched!")
                pass

    # Learning Session

    async def learning_session(self):
        """ Prozedur zur Darstellung einer Lernsystem

        :return:
        """
        async def learn_phase():
            """ Methode fuer den Ablauf einer Lernphase

            :return:
            """
            timestamp_now = int(datetime.datetime.now().timestamp())
            timestamp_end = timestamp_now + self.learning_duration * 60

            time_to_wait = (self.learning_duration * 60) / 10

            # Einteilung der Phase in 10 Abschnitte um Zeitleiste zu aktualisieren
            for i in range(10):
                if not self.stopped:
                    await self.message_controller.show_learning(i, timestamp_end)
                    await asyncio.sleep(time_to_wait)
                else:
                    break

        async def pause_phase():
            """ Methode fuer den Ablauf einer Pause

            :return:
            """
            timestamp_now = int(datetime.datetime.now().timestamp())
            timestamp_end = timestamp_now + self.pause_duration * 60

            time_to_wait = (self.pause_duration * 60) / 10

            # Einteilung der Phase in 10 Abschnitte um Zeitleiste zu aktualisieren
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
                        if not self.fist:
                            # await self.write_everyones_partner()
                            pass
                        else:
                            self.fist = False
                        if self.mute:
                            await self.mute_members()

                        self.phase = asyncio.create_task(learn_phase())
                        await self.phase
                    except asyncio.CancelledError:
                        pass
                    finally:
                        await self.unmute_members()
                        await self.bunch(with_calculation=True)
                        await self.tts_phase_ended()
                        self.learning = False

                else:
                    print(self.global_points)
                    try:
                        self.phase = asyncio.create_task(pause_phase())
                        await self.phase
                    except asyncio.CancelledError:
                        pass
                    finally:
                        await self.bunch(with_calculation=False)

                        # Decomment this, if tts after pause is needed!
                        # await self.tts_phase_ended()

                        self.learning = True

            else:
                break

    async def skip_phase(self):
        """ Methode, die das Ueberspringen der aktuellen Phase ermoeglicht

        :return:
        """
        self.phase.cancel()

    async def stop_session(self):
        """ Methode, die das Abbrechen der Lernsession ermoeglicht

        :return:
        """
        self.stopped = True
        self.phase.cancel()
        await self.message_controller.show_start_menu()

    async def tts_phase_ended(self):
        a = asyncio.ensure_future(self.message_controller.tts_phase_ended(True))

    # ####################
    # Notification Methods
    # Alle folgenden Methoden werden beim Betaetigen des entsprechenden Buttons aufgerufen
    # ####################

    # Start Menu Bundle

    async def start_menu_button_start(self):
        await self.mix_the_partners_and_write()
        await self.message_controller.show_pre(self.ready_members)

    async def start_menu_button_intro(self):
        await self.message_controller.show_intro()

    async def start_menu_button_konfiguration(self):
        await self.message_controller.show_conf()

    async def start_menu_button_beenden(self):
        await self.message_controller.show_end()

    # Conf Bundle

    async def conf_select_lerndauer(self, selected):
        self.learning_duration = int(selected)

    async def conf_select_pausedauer(self, selected):
        self.pause_duration = int(selected)

    async def conf_select_stummen_nicht_stummen(self, mute_members):
        self.mute = mute_members

    async def conf_button_zurueck(self):
        await self.message_controller.show_start_menu()

    # Intro Bundle

    async def intro_button_zurueck(self):
        await self.message_controller.show_start_menu()

    async def intro_button_tutorial(self):
        pass

    # Pre Bundle

    async def pre_button_bereit(self, presser):
        if presser.name not in [i.name for i in self.ready_members]:
            self.ready_members.append(presser)

        if all([i.name in [j.name for j in self.ready_members] for i in self.members]):
            await self.learning_session()
        else:
            await self.message_controller.show_pre(self.ready_members)

    # Learn Bundle

    async def learn_button_stop(self):
        await self.stop_session()

    async def learn_button_phase_ueberspringen(self):
        await self.skip_phase()

    async def learn_button_melden(self, reporter):
        name_of_reporter = reporter.name
        name_of_partner = self.partners[name_of_reporter]

        await self.admonish(name_of_partner)

        if self.current_points[name_of_partner] > 0:
            self.current_points[name_of_partner] -= 1

    # Pause Bundle

    async def pause_button_stop(self):
        await self.stop_session()

    async def pause_button_phase_ueberspringen(self):
        await self.skip_phase()

    async def pause_button_melden(self):
        pass

    async def pause_select_stummen_nicht_stummen(self, mute_members):
        self.mute = mute_members
