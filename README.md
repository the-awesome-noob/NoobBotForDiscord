# NoobBotForDiscord Bot Template

Follow these steps to get your own instance of noob.bot running:
1. Create the Bot Application

Go to the **Discord Developer Portal** by clicking [here.](https://discord.com/developers/applications)

Click *New Application* and name it noob.bot. (or, anything you want. noob.bot isn't required, just reccomended.)

Go to the *Bot* tab on the left.

Click *Add Bot* and confirm.

Under the *Token* section, click *Reset Token* and copy the token immediately. **Keep this token secret!**

Enable *MESSAGE CONTENT INTENT* further down on the same page.

2. Download the Files

Go to the bot file and download it by clicking [here.](https://github.com/the-awesome-noob/BreadBotForDiscord/blob/main/botgithubversion.py)

Also download the requirements file as without it the bot will not run. You can get it by clicking [here](https://github.com/the-awesome-noob/BreadBotForDiscord/blob/main/requirements.txt)

3. Configure and Run

Make sure you have **Python** installed. If you don't, download it by clicking [here.](https://www.python.org/)

Open your terminal or command prompt in the folder where you downloaded the files.

Install the **required** library:

pip install -r requirements.txt

Set your Bot Token as an environment variable (replace YOUR_TOKEN_HERE):

Windows (PowerShell): $env:BOT_TOKEN="YOUR_TOKEN_HERE"

Run the bot (make sure the filenames match):

python botgithubversion.py
