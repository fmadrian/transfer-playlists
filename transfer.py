import sys
import src.messages as messages
from src.user_errors import SpotifyError, YoutubeError, YoutubeDLError
from src.log import Log
from src.console import Console

from src.spotify_playlist import SpotifyPlaylist
from src.youtube_playlist import YoutubePlaylist

if __name__ == "__main__":
    try:
        console = Console(sys.argv) # Get the arguments put in console.
        sp = SpotifyPlaylist()
        # If they're valid and the Spotify token is valid, the script continues.
        if console.check_args() and sp.get_user_info():
            yc = YoutubePlaylist()
            if(console.args["playlist_id"] == messages.console["liked_videos"]):
                # YouTube's 'Liked videos'.
                spotify_playlist_created = sp.create_playlist()
                sp.add_songs_to_playlist(spotify_playlist_created, yc.get_liked_videos())
            else:
                # Videos from a playlist.
                youtube_playlist = yc.get_playlist_videos(console.args["playlist_id"])
                spotify_playlist_created = sp.create_playlist(youtube_playlist["name"], youtube_playlist["description"], youtube_playlist["public"])
                sp.add_songs_to_playlist(spotify_playlist_created, youtube_playlist["songs"])
    except (SpotifyError, YoutubeError, YoutubeDLError) as e:
        e.log_print()
    except Exception as e:
        Log().write_error(e)