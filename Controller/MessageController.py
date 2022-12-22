import asyncio

import Library.Bundles as Bundles


class MessageController:

    def __init__(self, ctx, sc):
        self.sc = sc
        self.ctx = ctx
        self.message = await ctx.send(content="Lädt...")

    async def edit(self, bundle, content=None):
        embed = bundle['embed']
        view = bundle['view']

        await self.message.edit(embed=embed, view=view, content=content)

    async def show_start_menu(self):
        bundle = Bundles.StartMenuBundle.create_bundle(self.sc)
        await self.edit(bundle)

    async def show_conf(self):
        bundle = Bundles.ConfBundle.create_bundle(self.sc)
        await self.edit(bundle)

    async def show_intro(self):
        bundle = Bundles.IntroductionBundle.create_bundle(self.sc)
        await self.edit(bundle)

    async def show_pre(self):
        bundle = Bundles.PreBundle.create_bundle(self.sc)
        await self.edit(bundle)

    async def show_learning(self):
        bundle = Bundles.LearnBundle.create_bundle(self.sc)
        await self.edit(bundle)

    async def show_pause(self):
        bundle = Bundles.PauseBundle.create_bundle(self.sc)
        await self.edit(bundle)

    async def show_end(self):
        bundle = Bundles.EndBundle.create_bundle(self.sc)
        await self.edit(bundle, content="Prozess beendet")
        await asyncio.sleep(10)
        await self.message.delete()
