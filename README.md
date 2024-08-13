# CommunityWeekly

## What is this?

This is a simple script I wrote while listening to my Discover Weekly playlist. The purpose of the script is to allow a Twitch community to create their own weekly playlist through the usage of commands in Twitch. 

## What do I need to set it up?

To start with you will need a Twitch account for the bot to use and a Spotify account to host the playlist on. 

Next you will need several API Tokens and Client IDs but the script will guide you through the process. Here is where you can find all of the information needed, **DO NOT SHARE THIS INFORMATION WITH ANYONE**:

**TWITCH_TOKEN** = https://twitchapps.com/tmi/

**TWITCH_CLIENT_ID** = https://dev.twitch.tv/console/apps/create *(Create an application with the OAuth Redirect URL being http://localhost)*

**NICK** is your choice

**PREFIX** is your choice

**CHANNEL** is your channel name on Twitch

**SPOTIFY_CLIENT_ID** and **SPOTIFY_CLIENT_SECRET** = https://developer.spotify.com/dashboard/create *(Make sure to set redirect URI to http://localhost:5000/callback and click Web API)*

## Commands

Currently only three commands exist:

**cwsong \<spotify link or id\>** - Allows a chatter to submit a song link

**cwhelp** - Gives a chatter instructions on how to submit a song link

**cwend** - Allows moderators to finalize the playlist

## What did you use to make this project?

I used Python 3.12 and PyCharm 2023.3.3. The individual dependencies can be found in the requirements.txt file.

## Plans for the future

Currently I have no intention of continuing the project but I do have features in mind for future updates. 
One feature I think would be nice to implement is song recommendation generation based on the chatters submissions so that a playlist could be padded out to reach the 50 song target. 
Several other QoL improvements are planned as well such as better input validation and better formatting.
