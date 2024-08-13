import spotipy
import os
import random
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from twitchio.ext import commands
from dotenv import load_dotenv, set_key
from pathlib import Path

# First time setup of .env file
if not os.path.isfile(".env"):
    validation = 'N'

    # Warning to user to prevent sensitive information being shown on stream
    print("Make sure you keep the following information private, your API keys are sensitive information.\n")
    input("Press Enter to continue...\n")

    # Creates .env file
    env_file_path = Path(".env")
    env_file_path.touch(mode=0o600, exist_ok=False)

    while validation == 'N':  # Validation loop to allow the user to verify they input the correct information
        set_key(dotenv_path=env_file_path,  # Sets TWITCH_TOKEN environment variable
                key_to_set='TWITCH_TOKEN',
                value_to_set=input("Please enter Twitch Token\n"))
        set_key(dotenv_path=env_file_path,  # Sets TWITCH_CLIENT_ID environment variable
                key_to_set='TWITCH_CLIENT_ID',
                value_to_set=input("Please enter Twitch Client ID\n"))
        set_key(dotenv_path=env_file_path,  # Sets NICK environment variable
                key_to_set='NICK',
                value_to_set=input("Please enter nickname for bot\n"))
        set_key(dotenv_path=env_file_path,  # Sets PREFIX environment variable
                key_to_set='PREFIX',
                value_to_set=input("Please enter prefix for commands\n"))
        set_key(dotenv_path=env_file_path,  # Sets CHANNEL environment variable
                key_to_set='CHANNEL',
                value_to_set=input("Please enter twitch channel username\n").lower())
        set_key(dotenv_path=env_file_path,  # Sets SPOTIFY_CLIENT_ID environment variable
                key_to_set='SPOTIFY_CLIENT_ID',
                value_to_set=input("Please enter Spotify Client ID\n"))
        set_key(dotenv_path=env_file_path,  # Sets SPOTIFY_CLIENT_SECRET environment variable
                key_to_set='SPOTIFY_CLIENT_SECRET',
                value_to_set=input("Please enter Spotify Client Secret\n"))
        set_key(dotenv_path=env_file_path,  # Sets PLAYLIST_ID environment variable
                key_to_set='PLAYLIST_ID',
                value_to_set=input("Please enter Playlist ID\n"))

        load_dotenv()  # Loads .env
        # Print statement to allow the user to confirm if they put the correct information in
        print(
            "You input:\nTWITCH_TOKEN: {0}\nTWITCH_CLIENT_ID: {1}\nNICK: {2}\nPREFIX: {3}\nCHANNEL: {4}\nSPOTIFY_CLIENT_ID: {5}\nSPOTIFY_CLIENT_SECRET: {6}\nPLAYLIST_ID: {7}".format(
                os.getenv('TWITCH_TOKEN'),
                os.getenv('TWITCH_CLIENT_ID'),
                os.getenv('NICK'),
                os.getenv('PREFIX'),
                os.getenv('CHANNEL'),
                os.getenv('SPOTIFY_CLIENT_ID'),
                os.getenv('SPOTIFY_CLIENT_SECRET'),
                os.getenv('PLAYLIST_ID')))
        validation = input("Are these correct? [Y or N]\n").upper()  # Allows user to end first time setup
        # Informs user where they can locate their environment variables if they need to be changed
    print("Information can be found at {0}\n".format(os.getcwd() + "\\.env"))

load_dotenv()  # Loads .env file with all values

bot = commands.Bot(  # Creates the twitch bot with the given information from .env
    token=os.getenv('TWITCH_TOKEN'),
    client_id=os.getenv('TWITCH_CLIENT_ID'),
    nick=os.getenv('NICK'),
    prefix=os.getenv('PREFIX'),
    initial_channels=[os.getenv('CHANNEL')]
)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIFY_CLIENT_ID'),  # Spotify API oauth call
                                               client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                                               redirect_uri='http://localhost:5000/callback',
                                               scope='playlist-modify-public, playlist-read-collaborative'))

df = pd.DataFrame({  # Pandas DataFrame for storing song and user data
    'Song': [],
    'User': []
})

songsPerUser = 2  # Value that determines how many submissions a single chatter can give


# Command that allows chatters to submit songs
# Checks for invalid inputs and ensures that chatters are abiding by the submission limit
# TODO: Add more robust input validation and support for multiple links
# noinspection PyBroadException
@bot.command(name='cwsong')
async def song_command(ctx: commands.Context, phrase: str):
    global df  # Allows for modification of the global DataFrame
    try:
        if sp.track(phrase):  # Checks if the link is valid
            # Checks if the chatter has submitted already and if they have exceeded the submission limit
            if ctx.author.name in df['User'].to_numpy() and int(
                    df['User'].value_counts()[ctx.author.name]) >= songsPerUser:
                # Informs the chatter that they hit the submission limit
                await ctx.send("You already submitted song(s) this week {0}".format(ctx.author.name))
            # Else appends the chatters submission to the DataFrame
            else:
                df = pd.concat([df, pd.DataFrame({'Song': [phrase], 'User': [ctx.author.name]})])  # Appends to df
                await ctx.send("Thank you {0}!".format(ctx.author.name))  # Informs chatter that their submission was accepted
    except Exception as e:  # Simple exception that catches Spotipy song fetch error
        await ctx.send("{0} that song does not exist".format(ctx.author.name))  # Informs the chatter tha their song link didn't work


# Command that informs a user how to submit songs
# TODO: Make formatting of help message better in chat
@bot.command(name='cwhelp')
async def help_command(ctx: commands.Context):
    await ctx.send("To use the bot type !cwsong <Spotify link here> If you are having trouble with hyperlinks you can use spotify id found here: https://open.spotify.com/track/<COPY THIS PART>?si=number")


# End command allows for the bot to finish
# Can only be used by moderators
# TODO: Implement cleaner program exit
@bot.command(name='cwend')
async def end_command(ctx: commands.Context):
    if ctx.author.is_mod:  # Checks to see if chatter is a mod
        create_playlist()  # Runs the create_playlist function to update the spotify playlist
        await ctx.send("Community Weekly is now over check it out here: {0}".format(os.getenv('PLAYLIST_ID')))  # Informs chat where to find the playlist
        exit()  # Exits the program, messy exit but does the job


# Function updates the spotify playlist
# If more than 50 songs were submitted, it randomly chooses 50.
def create_playlist():
    if len(df) > 50:  # If the DataFrame has more than 50 submissions, replaces a random selection of 50
        sp.playlist_replace_items(os.getenv('PLAYLIST_ID'), random.sample(df['Song'].tolist(), 50))
    # TODO: Implement song recommendations based on given seeds to pad out playlist if less than 50 submissions
    else:  # Else updates the playlist with the songs obtained for the week
        sp.playlist_replace_items(os.getenv('PLAYLIST_ID'), df['Song'].tolist())


if __name__ == '__main__':
    bot.run()  # Runs the bot
