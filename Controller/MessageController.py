import asyncio

import Library.Bundles as Bundles


class MessageController:

    def __init__(self, ctx, sc):
        self.sc = sc
        self.ctx = ctx
        self.message = None

    async def initialize(self):
        """ Initialisierung des MessageControllers

        Hierbei wird eine Pseudonachricht versendet,
        die im weiteren Verlauf des Lernprozesses immer wieder bearbeitet wird.

        :return:
        """
        self.message = await self.ctx.send(content="Lädt...")
        await self.show_start_menu()

    async def edit(self, bundle, content=None):
        """ Hilfsfunktion, um das Bearbeiten der Nachricht zu vereinfachen

        :param bundle:
        :param content:
        :return:
        """
        embed = bundle['embed']
        view = bundle['view']

        await self.message.edit(embed=embed, view=view, content=content)

    # ################
    # Ansichtsmethoden
    # Alle nachfolgenden Methoden dienen zur Darstellung der entsprechenden Ansichten
    # ################
    async def show_start_menu(self):
        bundle = Bundles.StartMenuBundle.create_bundle(self.sc)
        await self.edit(bundle)

    async def show_conf(self):
        bundle = Bundles.ConfBundle.create_bundle(self.sc)
        await self.edit(bundle)

    async def show_intro(self):
        bundle = Bundles.IntroductionBundle.create_bundle(self.sc)
        await self.edit(bundle)

    async def show_pre(self, ready_members):
        bundle = Bundles.PreBundle.create_bundle(self.sc, ready_members)
        await self.edit(bundle)

    async def show_learning(self, stage, dt):
        bundle = Bundles.LearnBundle.create_bundle(self.sc, stage, dt)
        await self.edit(bundle)

    async def show_pause(self, stage, dt, gp):
        bundle = Bundles.PauseBundle.create_bundle(self.sc, stage, dt, gp)
        await self.edit(bundle)

    async def show_end(self):
        bundle = Bundles.EndBundle.create_bundle(self.sc)
        await self.edit(bundle, content="Prozess beendet")
        await asyncio.sleep(10)
        await self.message.delete()

    async def tts_phase_ended(self, learning):
        """ Methode, damit der Bot eine Nachricht versenden kann die das Ende einer Phase klarstellt. Die Nachricht
        wird akustisch ausgesprochen.

        :param learning:
        :return:
        """
        m = None
        if learning:
            m = await self.ctx.send(content="Lernphase beendet.", tts=True)
        else:
            m = await self.ctx.send(content="Pause beendet.", tts=True)
        await asyncio.sleep(10)
        await m.delete()

