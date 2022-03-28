
import requests, json
from src.files import FileManager
import src.urls as urls, src.messages as messages
from src.user_errors import RequirementError, SpotifyError
from src.log import Log

class SpotifyPlaylist:
    def __init__(self):
        # loads the auth information
        self.user_id = ""
        self.token = ""
        self.read_authinfo()
    
    def read_authinfo(self):
        try:
            jsonobject = FileManager.readJSONFile("spotify_auth")
            self.user_id = jsonobject["user_id"]
            self.token = jsonobject["token"]
        except Exception as e:
            FileManager.createJSONFile("spotify_auth", {
                "user_id" : "","token":""
            })
            raise RequirementError(messages.spotify["no_auth_info"])

    def get_user_info(self):
        try:
            request = "me"
            query = urls.spotify[request]
            request_headers = {
                "Authorization": "Bearer {}".format(self.token)
            }
            response = requests.get(query, data=None, headers=request_headers)

            if (response.status_code != 200 and response.status_code != 201):
                raise SpotifyError(request, response)
            else:
                user = response.json()
                msg = "Spotify ID: {}\n Name: {}\n Type: {}".format(
                    user["external_urls"]["spotify"],
                    user["display_name"],
                    user["product"])
                Log().write_info("", msg)
                return True
        except (SpotifyError, Exception):
            raise
    # Create a Spotify playlist.
    def create_playlist(self, name="YouTube liked videos", description="Playlist that has music found in YouTube liked videos.", public=True):
        try:
            # url = query, data = body , headers = request_headers
            request = "create_playlist"
            query = urls.spotify[request].format(self.user_id)
            request_data = json.dumps({
                "name": name,
                "public": public,
                "description": description
            })
            request_headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
            response = requests.post(query, data=request_data, headers=request_headers)

            # If a request doesn't return an OK we raise an exception
            if (response.status_code != 200 and response.status_code != 201):
                raise SpotifyError(request, response)

            # Returns the playlist's id (we need it to add the songs)
            Log().write_info(request, messages.spotify["playlist_created"].format(name, response.json()["id"]))
            return response.json()["id"]
        except (SpotifyError, Exception) as e:
            raise

    # Gets a song's URI from its name.
    def get_spotify_uri(self, song_name, artist):
        try:
            # Returns the first result of the search, if there is any.
            request = "search_song"
            query = urls.spotify[request].format(song_name, artist, "track")
            request_headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
            response = requests.get(query, headers=request_headers)
            if (response.status_code != 200 and response.status_code != 201):
                raise SpotifyError(request, response)

            # See: https://developer.spotify.com/documentation/web-api/reference/search/search/
            # We get a response, and then obtain the array that contains the tracks (["tracks"]["items"])
            response_json = response.json()
            songs = response_json["tracks"]["items"]
            # If we don't get any results (songs), we log it (raise an error).
            if (len(songs) == 0):
                raise SpotifyError(request, msg=messages.spotify["no_songs"].format(song_name, artist))

            # We get the first result of the search and return that song's URI.
            song_uri = songs[0]["uri"]
            Log().write_info(request, messages.spotify["got_song_uri"].format(song_name, artist, song_uri))
            return song_uri
        except SpotifyError as e:
            e.log_print()
        except Exception as e:
            Log().write_error(e)

    # adds a list of songs to the playlist.
    def add_songs_to_playlist(self, spotify_playlist_id, songs):
        try:
            extra_songs = []
            # It can only add up to 100 songs per request.
            if(len(songs) > 100):
                # Has to cut from the array the extra songs to add them using other request.
                extra_songs = songs[100:]
                songs = songs[:100]

            uris = []
            # We get the songs URI's 
            for song in songs:
                uris.append(song["spotify_uri"])
            request = "add_tracks_to_playlist"
            query = urls.spotify[request].format(spotify_playlist_id)

            request_data = json.dumps({
                "uris": uris,
            })
            request_headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
            response = requests.post(query, data=request_data, headers=request_headers)
            response_code = response.status_code

            if(response_code != 200 and response_code != 201):
                raise SpotifyError(request, response)

            Log().write_info(request, messages.spotify["songs_added"].format(spotify_playlist_id))

            # If there's extra songs, make another request to add them.
            if(len(extra_songs) > 0):
                self.add_songs_to_playlist(spotify_playlist_id, extra_songs)

        except (SpotifyError, Exception):
            raise