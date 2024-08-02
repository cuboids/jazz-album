"""Select the jazz album of the day and open it in YouTube music."""

import datetime
import requests

from bs4 import BeautifulSoup
from ytmusicapi import YTMusic


# This is where we will look for potential jazz albums of the day.
URL = 'https://www.allaboutjazz.com/reviews/'


def get_yesterday_date() -> datetime.date:
    """Fetches yesterday's date.

    We will use yesterday's date, because there might not be any reviews
    for today yet.

    Returns:
        A datetime.date object representing yesterday's date.  # noqa: typo
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday


def convert_datetime_to_formatted_date(date: datetime.date) -> str:
    """Converts a date object to a formatted string.

    Args:
        date: The date object to be converted.

    Returns:
        A string representation of the date in the format: "Month day, year".
        The month is spelled out. For example, "March 21, 2023".
    """
    return date.strftime('%B %-d, %Y')


def find_highest_rated_album_and_artist_title(formatted_date: str) -> tuple:
    """Scrape the All About Jazz Reviews front page to find the jazz album
    with the highest rating. :)

    Args:
        formatted_date: A string representation of the date in the format: "March 21, 2023".

    Returns:
        A string containing the name of the album and the name of the artist.
    """
    response = requests.get(URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', class_='row data-row')

        highest_rated_album = None
        highest_rated_artist = None
        highest_rating = 0

        for review in reviews:
            date = review.find('span', class_='small').text.strip().split('\n')[-1].strip()
            album = review.find('h4').text.strip()
            artist = review.find('div', class_='data-row-content').contents[2].strip()
            rating = int(len(review.find_all('b', class_='fa fa-star')))

            if date == formatted_date:
                if rating > highest_rating:
                    highest_rated_album = album
                    highest_rated_artist = artist
                    highest_rating = rating

        if highest_rated_album and highest_rated_artist:
            return highest_rated_album, highest_rated_artist
        else:
            print(f'Hmm... Today is an unlucky day, we didn\'t find any albums for {formatted_date}. :O')
    else:
        print(f'Failed to fetch the reviews page. Status code: {response.status_code}')


def find_youtube_music_playlist(album_and_artist: tuple) -> str:
    """Find the YouTube Music Audio Playlist corresponding to an
    album and artist title.

    Args:
        album_and_artist: A string containing the name of the album and the name of the artist.

    Returns:
        A string containing the URL of the YouTube Music Audio Playlist.
    """
    yt_music = YTMusic()

    query = ' '.join(album_and_artist)
    # We will trust that the first result is correct.
    browse_id = yt_music.search(query=query, filter='albums')[0]['browseId']
    album = yt_music.get_album(browse_id)
    audio_playlist_id = album['audioPlaylistId']

    return f'https://www.youtube-nocookie.com/embed/videoseries?list={audio_playlist_id}'


def main() -> dict:
    """Find yesterday's highest rated jazz album on All About Jazz,
    - and find the YouTube Music URL corresponding to that album."""

    yesterday = get_yesterday_date()
    yesterday_formatted = convert_datetime_to_formatted_date(yesterday)
    album_and_artist = find_highest_rated_album_and_artist_title(yesterday_formatted)
    url = find_youtube_music_playlist(album_and_artist)

    return {
        'youtube_url': url,
        'album': album_and_artist[0],
        'artist': album_and_artist[1]
    }


if __name__ == '__main__':
    main()
