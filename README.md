# Weekly Mix Review Playlist Creator

This Python script automates the process of updating a Spotify playlist with a mix of songs from various genres. The playlist is updated on a weekly basis or manually, using GitHub Actions for automation. The script searches for tracks from the specified genres, shuffles them, clears the existing playlist, and adds the new tracks to it.

## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites

You'll need the following software to run this project:

- Python 3.6 or higher
- `pip` to install required packages

### Installation

1. Clone this repository:

```bash
git clone https://github.com/your_username/weekly-mix-review.git
cd weekly-mix-review
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # or "venv\Scripts\activate" on Windows
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Set up your Spotify Developer credentials:

- Visit the Spotify Developer Dashboard: https://developer.spotify.com/dashboard/applications
- Create a new application and note the Client ID and Client Secret
- Set the Redirect URI in your application settings to http://localhost:8080


5. Create a .env file in the project directory and add your Spotify Developer credentials:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8080
```

6. Replace your_existing_playlist_id in the update_playlist.py script with the ID of the existing playlist you want to update with new songs.

## Running the script

To run the script and update the playlist manually, execute the following command in your terminal or command prompt:

```bash
python update_playlist.py
```

The script will authenticate with the Spotify API, search for tracks from the specified genres, shuffle them, clear the existing playlist, and add the new tracks to it.

## Automating the process with GitHub Actions

To set up GitHub Actions to run the script weekly or manually, follow the instructions in the github_actions_setup.md file.

License

This project is licensed under the MIT License - see the LICENSE file for details.