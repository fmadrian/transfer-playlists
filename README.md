# syplaylist

Script that transfers songs from playlists or liked videos from YouTube to a Spotify playlist.

## Requirements

1. [Python](https://www.python.org/) 3.9.5.
2. A [Google cloud app](https://console.cloud.google.com/) with YouTube Data API v3 enabled.
3. Approve the [Spotify for Developers: Console](https://developer.spotify.com/console/)

## Getting ready

**NOTE: You only have follow these steps the first time.**

## Generate the spotify_auth.json file

Run the following command:

```
python syplaylist.py -liked
```

**After this, the file spotify_auth.json will be generated.**

### Get access to YouTube Data API v3

1. Create a [Google Cloud project](https://console.cloud.google.com/projectcreate).
2. Select the created project.
3. Go to the marketplace and enable the [YouTube Data API v3](https://console.cloud.google.com/marketplace/product/google/youtube.googleapis.com).
4. Fill the required information.
5. Select the following scopes:
   - youtube.readonly
6. Go to the **API and services** tab and select [Enabled API and services](https://console.cloud.google.com/apis/dashboard)
7. Select [Credentials](https://console.cloud.google.com/apis/credentials) tab.
8. Click the **Create credentials** button and then **OAuth client ID**.
9. Fill the following spaces
   1. _Application type_: **Desktop app**.
   2. _Name_: Any name.
10. Click the **Create** button.
11. Click the **Download JSON** button.
12. Rename the downloaded JSON file to **client_id**.
13. Copy and paste the file in the folder.

### Get your Spotify ID

1. Go to your [Spotify account](https://www.spotify.com/account/overview/).
2. Copy the value in the field **'Username'**.
3. Paste it into **spotify_auth.json** in the **'user_id'** field.

### Approve Spotify for Developers: Console

1. Go to [Spotify API: Get users profile](https://developer.spotify.com/console/get-users-profile/)
2. Press the **GET TOKEN** button.
3. Select the following scopes:

   - user-read-private
   - user-read-email
   - playlist-modify-public
   - playlist-modify-private

   **NOTE: You can select all the scopes EXCEPT 'playlist-read-public'**.

4. Click the **REQUEST TOKEN** button.
5. You need to approve the **Spotify for Developers: Console**.
6. Press **AGREE** button.

## How to use the script

Use the following commands:

Shows the help guide:

```
python syplaylist.py -h
python syplaylist.py -help
```

Transfer a YouTube playlist:

```
python syplaylist.py <playlist_url>
```

Transfer your liked videos:

```
python syplaylist.py -liked
```

1. Go to the URL displayed in the console (Get a YouTube authorization code).

   **After this, the browser will display a prompt indicating the permissions (scopes) the app requires. You have to authorize it.**

2. Authorize your app.

   **After this, the browser will display an authorization code**

3. Copy the authorization code displayed in the prompt and paste it in the console.
4. Press 'Enter'.
5. Wait until the process is done.
6. You will get a Spotify playlist with the name **'YouTube liked videos'** (if you transferred your liked videos) or **the name of the YouTube playlist**.

**NOTE: After using the script, check the 'log.txt' file to see which songs were and weren't transferred to the playlist.**

### How to get a Spotify token

Before using the script you need an Oauth Token provided by Spotify.
**NOTE: API tokens obtain this method expire after an hour. If a token expires, you need to repeat these steps.**

1. Go to [Spotify API: Get users profile](https://developer.spotify.com/console/get-users-profile/).
2. Select the following scopes:

   - user-read-private
   - user-read-email
   - playlist-modify-public
   - playlist-modify-private

   **NOTE: You can select all the scopes EXCEPT 'playlist-read-public'**.

3. Click the **REQUEST TOKEN** button.
4. Copy the value displayed in the field **'OAuth Token'**.
5. Paste it into **spotify_auth.json** in the **'token'** field.

## Known issues

- Your request might not be completed if you exceed Spotify and / or YouTube API usage quota.
- The script can only retrieve music from public and not age-restricted videos.

## Resources used

[Spotify API](https://developer.spotify.com/console/)

[YouTube Data API v3](https://developers.google.com/youtube/v3/)

[youtube-dl](https://youtube-dl.org/)
