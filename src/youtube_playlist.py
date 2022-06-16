import os
import src.urls as urls, src.messages as messages
from src.user_errors import YoutubeError, YoutubeDLError
# youtube client
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from src.spotify_playlist import SpotifyPlaylist
# youtube dl
import youtube_dl
from src.log import Log

class YoutubePlaylist:
    # https://developers.google.com/youtube/v3/docs/videos/list#try-it
    def __init__(self):
        self.youtube = self.get_youtube_client()
        self.log = Log()
    # Get the Youtube client.
    def get_youtube_client(self):
        try:
            scopes = ["https://www.googleapis.com/auth/youtube",
                           "https://www.googleapis.com/auth/youtube.force-ssl",
                           "https://www.googleapis.com/auth/youtube.readonly"]
            # Disable OAuthlib's HTTPS verification when running locally.
            # *DO NOT* leave this option enabled in production.
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

            api_service_name = "youtube"
            api_version = "v3"
            client_secrets_file = "client_id.json"

            # Get credentials and create an API client
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            credentials = flow.run_console()

            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, credentials=credentials)

            return youtube
        except KeyboardInterrupt:
            pass
        except Exception:
            raise

    # Get videos in 'Liked videos'
    def get_liked_videos(self):
        # https://developers.google.com/youtube/v3/docs/videos/list
        # Each object in items is a video.
        # https://developers.google.com/youtube/v3/docs/videos#resource
        try: 
            request = self.youtube.videos().list(
                part= "snippet,contentDetails,statistics",
                myRating= "like",
                maxResults= 50 # 5 by default, 50 videos max.
            )
            response = request.execute()
            playlist_items = response["items"]
            
            if(response.get("nextPageToken") != None):
                playlist_items = self.get_more_videos(response["nextPageToken"], response["items"], "liked")

            songs = []
            for item in playlist_items:
                try:
                    # Getting the video's title and id
                    video_title = item["snippet"]["title"]
                    video_url = urls.youtube["video"].format(item["id"])
                    # https://github.com/ytdl-org/youtube-dl#developer-instructions     EMBEDDING YOUTUBE-DL
                    # Then, we get the name of the song and artist through youtube_dl
                    # We download the information.
                    try:
                        video_info = youtube_dl.YoutubeDL({}).extract_info(video_url, download=False)

                        if(video_info == None or video_info.get("track") == None or video_info.get("artist") == None):
                            raise YoutubeDLError("get_liked_videos", msg=messages.youtube["info_incomplete"].format(video_title, video_url))
                    except YoutubeDLError as e:
                        raise e
                    except Exception as e:
                        raise YoutubeDLError("get_liked_videos", msg=messages.youtube["other_error"].format(e,video_title, video_url))
                    # We only extract the information that we need
                    # After that we get the URI of each song.
                    # If we cannot find a song in the list, the process continues with the next song on the list.

                    # After we get a URI, we add it to the retrieved songs list.
                    spotify_uri = SpotifyPlaylist().get_spotify_uri(video_info["track"], video_info["artist"])
                    if (spotify_uri != None):
                        songs.append({
                            "video_url": video_url,
                            "song_name": video_info["track"],
                            "artist": video_info["artist"],
                            "spotify_uri": spotify_uri
                        })
                except (YoutubeError, YoutubeDLError) as e:
                    e.log_print()
            return songs
        except Exception:
            raise

    # Retrieve videos from a playlist.
    def get_playlist_videos(self, playlist_id):
        try:
            request = self.youtube.playlistItems().list(
                part="snippet,id,contentDetails",
                maxResults=50,  # 5 by default.
                playlistId=playlist_id,
            )
            response = request.execute()
            playlist_items = response["items"]

            if(response.get("nextPageToken") != None):
                playlist_items = self.get_more_videos(response["nextPageToken"], response["items"], "playlist", playlist_id)

            songs = []
            for item in playlist_items:
                try:
                    # Get the video's ID and title.

                    # https://developers.google.com/youtube/v3/docs/playlistItems/list
                    video_title = item["snippet"]["title"]
                    video_url = urls.youtube["video"].format(item["contentDetails"]["videoId"])
                    # https://github.com/ytdl-org/youtube-dl#developer-instructions
                    # Get song and artist's name using youtube_dl
                    
                    try:
                        video_info = youtube_dl.YoutubeDL({}).extract_info(video_url, download=False)
                    
                        if (video_info == None or video_info.get("track") == None or video_info.get("artist") == None):
                            raise YoutubeDLError("get_playlist_videos",
                                                msg=messages.youtube["info_incomplete"].format(video_title, video_url))
                    except YoutubeDLError as e:
                        raise e
                    except Exception as e:
                        raise YoutubeDLError("get_playlist_videos", msg=messages.youtube["other_error"].format(e,video_title, video_url))

                    # We only extract the information that we need
                    # After that we get the URI of each song.
                    # If we cannot find a song in the list, the process continues with the next song on the list.

                    # After we get a URI, we add it to the retrieved songs list.
                    spotify_uri = SpotifyPlaylist().get_spotify_uri(video_info["track"], video_info["artist"])
                    if (spotify_uri !=  None):
                        songs.append({
                            "video_url": video_url,
                            "song_name": video_info["track"],
                            "artist": video_info["artist"],
                            "spotify_uri": spotify_uri
                        })
                except YoutubeDLError as e:
                    e.log_print()

            # We get the playlist's information
            request = self.youtube.playlists().list(
                part="snippet,id,status",
                maxResults=1,
                id=playlist_id,
            )
            response = request.execute()
            # Playlist's privacy.
            # If the playlist is not public on Youtube, it won't be public on Spotify.
            is_public = False
            playlist = response["items"][0]
            if playlist["status"]["privacyStatus"] == "public":
                is_public = True
            return {
                "songs": songs,
                "name" : playlist["snippet"]["title"],
                "description" : playlist["snippet"]["description"],
                "public" :  is_public
            }
        except (YoutubeError, Exception):
            raise

    def get_more_videos(self, nextPageToken, items, type, playlist_id=None):
        if(type == 'liked'):
            request = self.youtube.videos().list(
                    part= "snippet,contentDetails,statistics",
                    myRating= "like",
                    pageToken=nextPageToken,
                    maxResults= 50 # 5 by default, 50 videos max.
            )
        elif(type == 'playlist'):
            request = self.youtube.playlistItems().list(
                part="snippet,id,contentDetails",
                maxResults=50,  # 5 by default.
                pageToken=nextPageToken,
                playlistId=playlist_id,
            )
        
        response = request.execute()    
        # Add the videos to the list.
        for item in response["items"]:
            items.append(item)
            
        if(response.get("nextPageToken") != None):
            return self.get_more_videos(response["nextPageToken"], items, type, playlist_id)     
        else: 
           return items