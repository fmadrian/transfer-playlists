# transfer-playlists

Script that transfers songs from playlists or liked videos from YouTube to a Spotify playlist.

## Requirements

1. [Python](https://www.python.org/) 3.9.5.
2. A [Google cloud app](https://console.cloud.google.com/) with YouTube Data API v3 enabled.
3. Approve the [Spotify for Developers: Console](https://developer.spotify.com/console/)

## Setup

### Install the script dependencies

To install the script dependencies run:

```
pip install -r requirements.txt
```

### Generate the spotify_auth.json file

**NOTE: You only have follow these steps once.**

Run the following command:

```
python transfer.py
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
13. Move the file in the folder where _transfer.py_ is.

### Get your Spotify ID

1. Go to your [Spotify account](https://www.spotify.com/account/overview/).
2. Copy the value in the field **'Username'**.
3. Paste it into **spotify_auth.json** in the **'user_id'** field.

### How to get a Spotify token | Approve Spotify for Developers: Console

Before using the script you need an OAuth Token provided by the Spotify .
**NOTE: API tokens obtain this method expire after an hour. If a token expires, you need to repeat these steps.**

1. Go to [Spotify API: Get users profile](https://developer.spotify.com/console/get-users-profile/).
2. Press the **GET TOKEN** button.
3. Select the following scopes:

   - user-read-private
   - user-read-email
   - playlist-modify-public
   - playlist-modify-private

   **NOTE: You can select all the scopes EXCEPT 'playlist-read-public'**.

4. Click the **REQUEST TOKEN** button.
5. Copy the value displayed in the field **'OAuth Token'**.
6. Paste it into **spotify_auth.json** in the **'token'** field.

**NOTE: You will have to approve the Spotify for Developers: Console, the first time you try to get a token.**

## Commands

Transfer a YouTube playlist:

```
python transfer.py <playlist_url>
```

Example: [YouTube](https://www.youtube.com/playlist?list=PLXo96vlNmlLKcHgZEkpZ2lS32kh-h4BAa) | [Spotify](https://open.spotify.com/playlist/2w6IqJ1Zt6myya1nG1K0Et)

<p align="center">
   <img alt="YouTube playlist - YouTube" title="YouTube playlist - YouTube" src="https://user-images.githubusercontent.com/47431198/174152878-29fcd2f5-5fef-43af-9604-5a1fe2e9c723.png" width=472 height=333>
   <img alt="YouTube playlist - Spotify" title="YouTube playlist - Spotify" src="https://user-images.githubusercontent.com/47431198/174154383-637b23b4-2d18-4e04-88b2-3a3f7cd85475.png" width=472 height=333>

</p>

Transfer your liked videos:

```
python transfer.py -liked
```

<p align="center">
   <img alt="Liked videos - YouTube" title="Liked videos - YouTube" src="https://user-images.githubusercontent.com/47431198/174153719-635f02b6-486b-40d2-9546-5bfd6fea727c.png" width=472 height=333>
   <img alt="Liked videos - Spotify" title="Liked videos - Spotify" src="https://user-images.githubusercontent.com/47431198/174152538-f376197b-bba5-4691-bc04-697755440c9a.png" width=472 height=333>
</p>

Shows the help guide:

```
python transfer.py -h
python transfer.py -help
```

## How to use the script

1. Type one of the two commands.

2. Go to the URL displayed in the console (Get a YouTube authorization code).

   **After this, the browser will display a prompt indicating the permissions (scopes) the app requires. You have to authorize it.**

3. Authorize your app.

   **After this, the browser will display an authorization code**

4. Copy the authorization code displayed in the prompt and paste it in the console.
5. Press 'Enter'.
6. Wait until the script transfers the songs.
7. You will get a Spotify playlist with the name **'YouTube liked videos'** (if you transferred your liked videos) or **the name of the YouTube playlist**.

**NOTE: After using the script, check the 'log.txt' file to see which songs were and weren't transferred to the playlist.**

## Additional information

- Some songs might not be transferred if you exceed Spotify and / or YouTube API usage quota.
- The script can only retrieve music from public videos.
- youtube-dl might not be able to retrieve information about some songs.
- Some songs might not be available on Spotify.

## Resources used

[Spotify API](https://developer.spotify.com/console/)

[YouTube Data API v3](https://developers.google.com/youtube/v3/)

[youtube-dl](https://youtube-dl.org/)
