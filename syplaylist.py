import sys
import src.messages as messages
from src.user_errors import SpotifyError, YoutubeError, YoutubeDLError
from src.log import Log
from src.console import Console

from src.spotify_playlist import SpotifyPlaylist
from src.youtube_playlist import YoutubePlaylist

if __name__ == "__main__":
    try:
        debug = False
        console = Console(sys.argv) # Get the arguments put in console.
        if debug == True:
            console.args["playlist_id"] = messages.console["liked_videos"]
        # If they're valid, the script execution continues.
        if debug == True or console.check_args():
            sp = SpotifyPlaylist()
            yc = YoutubePlaylist()
            if (sp.get_user_info()):
                if(console.args["playlist_id"] == messages.console["liked_videos"]):
                    # My 'Liked videos'.
                    sp.add_songs_to_playlist(sp.create_playlist(), yc.get_liked_videos())
                else:
                    # Videos from other playlist.
                    playlist = yc.get_playlist_videos(console.args["playlist_id"])
                    spotify_playlist_id = sp.create_playlist(playlist["name"], playlist["description"], playlist["public"])
                    sp.add_songs_to_playlist(spotify_playlist_id, playlist["songs"])
    except (SpotifyError, YoutubeError, YoutubeDLError) as e:
        e.log_print()
    except Exception as e:
        Log().write_error(e)