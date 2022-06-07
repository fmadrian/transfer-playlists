name= "syplaylist"
version = '0.20220325.1'
log = {
    "create" : "LOG CREATED",
    "already_exists" : "LOG OPENED SUCCESSFULLY",
}
spotify = {
    "no_auth_info" : "The Spotify authentication information (spotify_auth.json) didn't exist or is not valid. Please fill the file with the information required.",
    "no_songs" : "No results for {} by {}", # Got song information, but we can't find it in Spotify
    "got_song_uri" : "Got {} by {}. URL: {}",
    "playlist_created" : "Spotify playlist created. Name: {} ID: {} ",
    "songs_added" : "Songs have been added to {} ({}) playlist. URL: {}"
}
youtube ={
    "info_incomplete" : "Could not get enough information for : {} {}", # youtube-dl couldn't get song information in the video
    "info_complete": "{} by {} got from : {}",
    "other_error": "{} for :{} {}" 
}
console = {
    "liked_videos" : "-liked",
    "invalid" : "The commands introduced are not valid.",
    "no_params" : "Didn't introduced the necessary commands.",
    "help_msg" : "Transfer songs from a YouTube playlist to your Spotify account."
                + "\nRead README.md for a full guide on requirements and how to use the script."
                + "\n"
                + "\nCommands:"
                + "\n"
                 + "\n-h, -help	Shows the help guide."
                 + "\n<playlist_url>	Transfers an specific playlist."
                 + "\n-liked 		Transfers your liked videos."
                 + "\n"
                 + "\n"
                 + "\nAfter using the script, check the log.txt file to see which songs were / weren't transferred to the playlist."
}

