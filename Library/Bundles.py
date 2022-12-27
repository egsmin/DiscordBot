import discord
import Controller


class StartMenuBundle:
    embed = discord.Embed(
        title="Discord Lern-Bot",
        description="Start Menü",
    ).add_field(
        name="Start",
        value="Legt sofort los.",
        inline=False
    ).add_field(
        name="Intro",
        value='Erhaltet Informationen darüber, wie der Bot funktioniert und erfahrt mehr über das Thema "ablenkendes Verhalten".',
        inline=False
    ).add_field(
        name="Konfiguration",
        value="Hier könnt ihr eure Einstellungen ändern.",
        inline=False
    ).add_field(
        name="Beenden",
        value="Beendet das Programm",
        inline=False
    )

    class View(discord.ui.View):
        def __init__(self, sc):
            super().__init__(timeout=3600)
            self.sc = sc

        @discord.ui.button(label='Start', style=discord.ButtonStyle.success)
        async def button_callback_start(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.start_menu_button_start()

        @discord.ui.button(label='Intro', style=discord.ButtonStyle.secondary)
        async def button_callback_intro(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.start_menu_button_intro()

        @discord.ui.button(label='Konfiguration', style=discord.ButtonStyle.blurple)
        async def button_callback_konfiguration(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.start_menu_button_konfiguration()

        @discord.ui.button(label='Beenden', style=discord.ButtonStyle.danger)
        async def button_callback_beenden(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.start_menu_button_beenden()

    @classmethod
    def create_bundle(cls, sc):
        return {
            "embed": cls.embed,
            "view": cls.View(sc)
        }


class ConfBundle:
    embed = discord.Embed(
        title="Discord Lern-Bot",
        description="Konfiguration",
    ).add_field(
        name="Lern- / Pause-Dauer",
        value="Gewünschte Dauer der jeweiligen Phase",
        inline=False
    ).add_field(
        name="Stumm / Nicht Stummen",
        value="Bestimmt, ob ihr während einer Lern-Phase gestummt werden sollt.\n"
              "(Diese Einstellung kann während der Phasen geändert werden)",
        inline=False
    )

    class View(discord.ui.View):
        def __init__(self, sc):
            super().__init__(timeout=3600)
            self.sc = sc

        @discord.ui.select(options=[discord.SelectOption(label=str(i) + " Minuten") for i in [1, 5, 10, 15, 20, 25, 30]],
                           placeholder="Lern-Dauer")
        async def select_callback_learn_duration(self, interaction, select):
            await interaction.response.defer()
            await self.sc.conf_select_lerndauer(select.values[0].split(" ")[0])

        @discord.ui.select(options=[discord.SelectOption(label=str(i) + " Minuten") for i in [1, 5, 10, 15, 20, 25, 30]],
                           placeholder="Pause-Dauer")
        async def select_callback_pause_duration(self, interaction, select):
            await interaction.response.defer()
            await self.sc.conf_select_pausedauer(select.values[0].split(" ")[0])

        @discord.ui.select(options=[discord.SelectOption(label="Stummen"), discord.SelectOption(label="Nicht Stummen")],
                           placeholder="Stummen / Nicht Stummen")
        async def select_callback_mute(self, interaction, select):
            await interaction.response.defer()
            await self.sc.conf_select_stummen_nicht_stummen(select.values[0] == "Stummen")

        @discord.ui.button(label='Zurück', style=discord.ButtonStyle.red, row=4)
        async def button_callback_back(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.conf_button_zurueck()

    @classmethod
    def create_bundle(cls, sc):
        return {
            "embed": cls.embed,
            "view": cls.View(sc)
        }


class IntroductionBundle:
    embed = discord.Embed(
        title="Discord Lern-Bot",
        description="Einführung",
    ).add_field(
        name="Begrüßung",
        value="Herzlich Willkommen zum Discord-Focus-Bot.",
        inline=False
    ).add_field(
        name="Allgemein",
        value="Dieser Bot begleitet euch beim Lernen und soll euch dabei helfen, eure Konzentration zu steigern.",
        inline=False
    ).add_field(
        name="Das Problem",
        value="Mit der stetigen Entwicklung der digitalen Geräte stehen uns immer mehr Möglichkeiten zur Verfügung. Die Wissenschaft fand allerdings heraus, dass diese auch eine Kehrseite mit sich tragen. Während Menschen lernen oder arbeiten, behalten sie das jeweilige Ziel immer im Gedächtnis. Durch ständige Ablenkungen wie Mitteilungen oder dem Drang, bspw. auf das Handy zu schauen, werden diese Ziele jedoch teilweise bis vollständig verdrängt, worunter die Effizienz leiden kann.",
        inline=False
    ).add_field(
        name="Die Lösung",
        value="Einerseits wurden bisher viele Mittel zur Selbstkontrolle entwickelt. Viele davon versuchen die ungewollten Angewohnheiten zu unterdrücken oder umzuleiten, ablenkende Inhalte auszublenden oder die Motivation, auf solche Geräte zu verzichten zu stärken. Andererseits wurden im Bereich der sozialen Wissenschaften positive Effekte des gemeinsamen Lernens entdeckt. Dieser Bot zielt darauf ab, beide Seiten zu verknüpfen, indem das gegenseitige Beobachten eingeführt wird. Hierbei soll jeder seinen Bildschirm teilen und die Lernenden beobachten sich gegenseitig. Das Ziel des Fokussiert-Seins ist nun beständiger im Gedächtnis. Würde man im Normalfall dieses Ziel vergessen, so wird man von dem Gefühl, beobachtet zu werden, davon abgehalten.",
        inline=False
    ).add_field(
        name="Ablauf",
        value="Sobald ihr die Lernsession startet, erscheinen abwechselnd zwei verschiedene Phasen. Die Regeln während der Phasen werden nun genauer erläutert.",
        inline=False
    ).add_field(
        name="Lernphase",
        value="1. Bitte aktiviert den Ruhemodus / Nicht-Stören-Modus eures Handys. Es ist wichtig, dass ihr euch nicht von Benachrichtigungen und Mitteilungen ablenken lasst. \n2. Vermeidet ablenkende Inhalte auf eurem PC.\n3. Aktiviert eure Bildschirmübertragung\n4.Ihr bekommt einen Partner zugewiesen, dessen Bildschirm und Verhalten ihr während des Lernens im MILDEREN Maße überwachen sollt.",
        inline=False
    ).add_field(
        name="Pause",
        value="Ihr dürft während der Pause machen, was ihr wollt! Benutzt eure Mobilgeräte und Computer oder quatscht miteinander. Das ist euch überlassen",
        inline=False
    ).add_field(
        name="Sonstiges",
        value="Alles weitere wird sich im Laufe der Session klären!\n\nFalls ihr fertig seid mit dem Lernen, drückt einfach auf Stop.\n\nVIEL ERFOLG!",
        inline=False
    )

    class View(discord.ui.View):
        def __init__(self, sc):
            super().__init__(timeout=3600)
            self.sc = sc

        @discord.ui.button(label='Zurück', style=discord.ButtonStyle.red)
        async def button_callback_back(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.intro_button_zurueck()

        @discord.ui.button(label='Tutorial', style=discord.ButtonStyle.green)
        async def button_callback_tutorial(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.intro_button_tutorial()

    @classmethod
    def create_bundle(cls, sc):
        return {
            "embed": cls.embed,
            "view": cls.View(sc)
        }


class TutorialBundle:
    embed = discord.Embed(
        title="",
        description="",
    ).add_field(
        name="",
        value="",
        inline=False
    )

    class View(discord.ui.View):
        def __init__(self, sc):
            super().__init__(timeout=3600)
            self.sc = sc

        @discord.ui.button(label='0', style=discord.ButtonStyle.red)
        async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()

        @discord.ui.select(options=[], placeholder="")
        async def select_callback(self, interaction, select):
            await interaction.response.defer()

    @classmethod
    def create_bundle(cls, sc):
        return {
            "embed": cls.embed,
            "view": cls.View(sc)
        }


class PreBundle:
    @classmethod
    def embed(cls, ready_members):

        ready_members_str = "\n".join([i.name for i in ready_members])
        if ready_members_str == "":
            ready_members_str = "->"
        return discord.Embed(
            title="Discord Lern-Bot",
            description="Vorbereitung",
        ).add_field(
            name="Bildschirm teilen",
            value="Bitte aktiviert eure Bildschirmübertragung",
            inline=False
        ).add_field(
            name="Partner beobachten",
            value="Ihr habt nun einen Partner zugewiesen bekommen. Bitte beobachtet dessen Bildschirm. Falls noch unklar ist, wie die Übertragung am Besten beobachtet werden kann, schaut einfach im Start Menü unter Intro -> Tutorial nach, oder schreibt mir \"$tutorial\" per Privatchat",
            inline=False
        ).add_field(
            name="Bereit:",
            value=ready_members_str,
            inline=False
        )

    class View(discord.ui.View):
        def __init__(self, sc):
            super().__init__(timeout=3600)
            self.sc = sc

        @discord.ui.button(label='Bereit', style=discord.ButtonStyle.red)
        async def button_callback_ready(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.pre_button_bereit(interaction.user)

    @classmethod
    def create_bundle(cls, sc, ready_members):
        return {
            "embed": cls.embed(ready_members),
            "view": cls.View(sc)
        }


class LearnBundle:

    @classmethod
    def embed(cls, stage, dt):

        bar = stage * "🟩" + (10 - stage) * "⬜️"

        return discord.Embed(
            title="Discord Lern-Bot",
            description="Lern-Phase",
        ).add_field(
            name="Zeit",
            value="Phase endet <t:" + str(dt) + ":R>",
            inline=True,
        ).add_field(
            name="Fortschritt",
            value="[" + bar + "]",
            inline=True
        )

    class View(discord.ui.View):
        def __init__(self, sc):
            super().__init__(timeout=3600)
            self.sc = sc

        @discord.ui.button(label='Stop', style=discord.ButtonStyle.red)
        async def button_callback_stop(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.learn_button_stop()

        @discord.ui.button(label='Phase überspringen', style=discord.ButtonStyle.blurple)
        async def button_callback_skip(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.learn_button_phase_ueberspringen()

        @discord.ui.button(label='Melden', style=discord.ButtonStyle.gray, disabled=False)
        async def button_callback_report(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.learn_button_melden(interaction.user)

    @classmethod
    def create_bundle(cls, sc, stage, dt):
        return {
            "embed": cls.embed(stage=stage, dt=dt),
            "view": cls.View(sc)
        }


class PauseBundle:
    @classmethod
    def embed(cls, stage, dt, gp):
        bar = stage * "🟩" + (10 - stage) * "⬜️"
        pointstr = "\n".join([m + ": " + str(gp[m]) + " Punkte" for m in gp.keys()])

        return discord.Embed(
            title="Discord Lern-Bot",
            description="Pause",
        ).add_field(
            name="Punkte",
            value=pointstr,
            inline=False
        ).add_field(
            name="Zeit",
            value="Phase endet <t:" + str(dt) + ":R>",
            inline=True,
        ).add_field(
            name="Fortschritt",
            value="[" + bar + "]",
            inline=True
        )

    class View(discord.ui.View):
        def __init__(self, sc):
            super().__init__(timeout=3600)
            self.sc = sc

        @discord.ui.button(label='Stop', style=discord.ButtonStyle.red)
        async def button_callback_stop(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.pause_button_stop()

        @discord.ui.button(label='Phase überspringen', style=discord.ButtonStyle.blurple)
        async def button_callback_skip(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.pause_button_phase_ueberspringen()

        @discord.ui.button(label='Melden', style=discord.ButtonStyle.gray, disabled=True)
        async def button_callback_report(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            await self.sc.pause_button_melden()

        @discord.ui.select(options=[discord.SelectOption(label="Stummen"), discord.SelectOption(label="Nicht Stummen")],
                           placeholder="Stummen / Nicht Stummen")
        async def select_callback_mute(self, interaction, select):
            await interaction.response.defer()
            await self.sc.pause_select_stummen_nicht_stummen(select.values[0] == "Stummen")

    @classmethod
    def create_bundle(cls, sc, stage, dt, gp):
        return {
            "embed": cls.embed(stage=stage, dt=dt, gp=gp),
            "view": cls.View(sc)
        }


class EndBundle:

    @classmethod
    def create_bundle(cls, sc):
        return {
            "embed": None,
            "view": None
        }
