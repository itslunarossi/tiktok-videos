# TikTok Video Downloader

## Setup

Install yt-dlp:
```bash
pip install -U yt-dlp
```

## Usage

### Download latest video from an account:
```bash
python download.py --user Simon_Ingari
```

### Download multiple videos:
```bash
python download.py --user Simon_Ingari --count 10
```

### Download from specific URL:
```bash
python download.py --url "https://www.tiktok.com/@Simon_Ingari/video/123456789"
```

## Options
- `--user` or `-u`: TikTok username (without @)
- `--url` or `-l`: Direct video URL
- `--count` or `-n`: Number of videos to download (default: 1)
- `--output` or `-o`: Output directory (default: ./downloads)

## Examples

```bash
# Download 5 latest videos
python download.py -u Simon_Ingari -n 5

# Download to specific folder
python download.py -u corporate_guru -o /path/to/videos

# Get metadata only (no download)
python download.py -u Simon_Ingari --metadata-only
```
