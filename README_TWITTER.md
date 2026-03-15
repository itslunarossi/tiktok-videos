# Twitter/X Video Downloader

## Setup

Install yt-dlp:
```bash
pip install -U yt-dlp
```

## Usage

### Download a Twitter/X video:
```bash
python download_twitter.py --url "https://x.com/AtaqueFutbolero/status/2032598715895067004"
```

### Download latest 5 tweets with video from a user:
```bash
python download_twitter.py --user AtaqueFutbolero --count 5
```

### Options
- `--url` or `-l`: Direct tweet URL
- `--user` or `-u`: Twitter username
- `--count` or `-n`: Number of tweets with videos to download
- `--output` or `-o`: Output directory (default: ./downloads)

## Examples

```bash
# Download single video
python download_twitter.py -l "https://x.com/AtaqueFutbolero/status/2032598715895067004"

# Download to specific folder
python download_twitter.py -l "https://x.com/user/status/123" -o /path/to/videos

# Download latest 10 videos from a user
python download_twitter.py -u username -n 10
```
