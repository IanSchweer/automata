import praw
from datetime import datetime, timedelta
class CurrentDaysBands:
    def __init__(self, **praw_config):
        self.reddit = praw.Reddit(**praw_config)

    def get_sub(self):
        return self.reddit.subreddit('progmetal')

    def get_bands(self, day_to_grab):
        posts = self.get_sub().new(limit=500)
        return [
            self._extract_song_info(post.title)
            for post
            in posts
            if datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d') == day_to_grab
            and 'youtube.com' in post.url
            and "song" in self._extract_song_info(post.title)
        ]

    def _extract_song_info(self, post_title):
        song_info = list(map(str.strip, post_title.split(" - ")))
        for i in range(len(song_info)): 
            piece = song_info[i]
            for c in "[(":
                if c in piece:
                    piece = piece[:piece.index(c)].strip()
            song_info[i] = piece
        return dict(zip(["band", "song"], song_info))
