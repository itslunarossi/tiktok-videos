#!/usr/bin/env python3
"""
Twitter/X Video Downloader
Usage: python download_twitter.py --url tweet_url OR --user username
"""

import argparse
import os
import subprocess
import sys
import json

def install_yt_dlp():
    """Install yt-dlp if not present"""
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        print("✓ yt-dlp already installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing yt-dlp...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], check=True)
            print("✓ yt-dlp installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("ERROR: Could not install yt-dlp. Please install manually: pip install yt-dlp")
            return False

def get_tweet_info(url):
    """Get tweet metadata without downloading"""
    cmd = [
        'yt-dlp',
        '--skip-download',
        '--write-info-json',
        '--print', '%(uploader_name)s | %(upload_date)s | %(duration)ss | %(view_count)s views | %(title)s',
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def download_video(url, output_dir='./downloads'):
    """Download Twitter/X video"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Twitter/X specific format - best quality without watermark
    cmd = [
        'yt-dlp',
        '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '--output', os.path.join(output_dir, '%(uploader_name)s_%(upload_date)s_%(id)s.%(ext)s'),
        '--sleep-interval', '2',
        '--max-sleep-interval', '5',
        '--add-header', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        url
    ]
    
    print(f"Downloading to {output_dir}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Download complete!")
        # List downloaded files
        for f in os.listdir(output_dir):
            if f.endswith('.mp4'):
                filepath = os.path.join(output_dir, f)
                size = os.path.getsize(filepath) / (1024 * 1024)
                print(f"  📹 {f} ({size:.1f} MB)")
        return True
    else:
        print(f"✗ Error: {result.stderr}")
        return False

def download_user_tweets(username, count, output_dir):
    """Download videos from user's tweets"""
    url = f"https://x.com/{username}"
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = [
        'yt-dlp',
        '--playlist-items', f'1-{count}',
        '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '--download-archive', os.path.join(output_dir, 'twitter_archive.txt'),
        '--output', os.path.join(output_dir, '%(uploader_name)s/%(upload_date)s_%(id)s.%(ext)s'),
        '--sleep-interval', '2',
        '--max-sleep-interval', '5',
        '--add-header', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '--filter', 'media',  # Only videos
        url
    ]
    
    print(f"Downloading {count} tweets with videos from @{username} to {output_dir}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Download complete!")
        # Count downloaded files
        mp4_count = 0
        for root, dirs, files in os.walk(output_dir):
            mp4_count += sum(1 for f in files if f.endswith('.mp4'))
        print(f"  Total videos: {mp4_count}")
        return True
    else:
        print(f"✗ Error: {result.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Download Twitter/X videos')
    parser.add_argument('--url', '-l', help='Direct tweet URL')
    parser.add_argument('--user', '-u', help='Twitter/X username (without @)')
    parser.add_argument('--count', '-n', type=int, default=1, help='Number of tweets to download')
    parser.add_argument('--output', '-o', default='./downloads', help='Output directory')
    parser.add_argument('--metadata-only', action='store_true', help='Show info only, no download')
    
    args = parser.parse_args()
    
    # Install yt-dlp
    if not install_yt_dlp():
        sys.exit(1)
    
    # Determine URL
    if args.url:
        url = args.url
        # Handle different URL formats
        if 'x.com' in url:
            pass  # Already in correct format
        elif 'twitter.com' in url:
            url = url.replace('twitter.com', 'x.com')
    elif args.user:
        url = f"https://x.com/{args.user}"
    else:
        parser.print_help()
        sys.exit(1)
    
    # Metadata only mode
    if args.metadata_only:
        print("Fetching tweet info...")
        info, error = get_tweet_info(url)
        if info:
            print(f"✓ {info}")
        else:
            print(f"✗ Error: {error}")
        return
    
    # Download
    if args.count == 1 or args.url:
        download_video(url, args.output)
    else:
        if args.user:
            download_user_tweets(args.user, args.count, args.output)
        else:
            print("Error: --count requires --user")

if __name__ == '__main__':
    main()
