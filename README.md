## *Favorite Streamers*

This basic python script that utilizing Twitch.tv's helix API to generate a simple list of a user's followed streamers with details.

#### The output of this file currently includes:

- The channel's name
- The current game or category that they are under 
- Their current amount of viewers

## Dependencies
Currently this application is super bare-bones so the only library requirements that are needed is very small.

All libraries are in the `requirements.txt`

## How to use
The main requirement that is needed for this script is **Client Id** and **Authorization Token**.

Both of these can be retrieved from [this handy token generator](https://twitchtokengenerator.com/) with the `user:read:follows` scope.

A **User Id** will also be prompted and can be grabbed from [another handy generator](https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/) 

This script will prompt for re-entry of all these variables when running the script and be stored in a `config.ini` file.
