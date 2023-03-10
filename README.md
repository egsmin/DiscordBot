# DiscordBot
DiscordBot for learning purposes and help for self-control through socially shared regulation of learning. 

## How to run the Bot
1. Clone this project.
2. Go to the [Discord Developer Portal](https://discord.com/developers) and log in.
3. Create a new application and give it a name (this name is *not* the name of the bot, that occurs in Discord).
4. After you have created the application, go the **Bot** section on the left side.
5. Click on **Add Bot**
6. Give the bot a name
7. Copy the Token. You have to click on **View Token**, in order to see it and be able to copy it.
8. Open the project, you already have cloned in Step 1, in a development tool of your choice.
9. You have to rename the file, named `config_template.py` into `config.py`
10. Open `config.py`. You will see the following code:
    ```python
    access_token = ""
    ```
11. You have to paste the token here, which you've copied in step 7.
12. Please go back to the [Discord Developer Portal](https://discord.com/developers)
13. On the left side, switch to the **OAuth2 > URL Generator** Section
14. In the **scopes** selection, you select **bot**
15. After that, the **Bot Permissions** selection will appear. Please select the **Administrator** here.
16. Copy the generated link below.
17. Paste it into the browser. Select the Discord-Server, you want to add the bot to (Of course, you have to be admin of a server for this step).
18. Run the following commands in terminal:
    ```
    pip install discord
    ```
18. Run the `main.py` script.

## Start the Bot in Discord
1. After you've finished the steps before, the Discord Bot should be marked as 'online' in Discord.
2. Before you start the Bot, please make sure, that 
   1. you have created at least one text-channel
   2. you have created at least one voice-channel
   3. all participants, are in the same voice-channel. 
3. The bot will only consider the voice-channel with the most members.
4. After done, you can write `$start` into a text-channel of your choice. The bot will only consider the text-channel, you write the `$start`-command into.
5. The Bot will switch its status to 'offline', when you stop the python script.

Please contact me for help.