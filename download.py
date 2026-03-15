#!/usr/bin/env python3
"""
TikTok Video Downloader
Usage: python download.py --user username OR --url video_url
"""

import argparse
import os
import subprocess
import sys

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

def get_video_info(url):
    """Get video metadata without downloading"""
    cmd = [
        'yt-dlp',
        '--skip-download',
        '--write-info-json',
        '--print', '%(uploader_id)s | %(upload_date)s | %(duration)ss | %(view_count)s views | %(title)s',
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def download_video(url, output_dir='./downloads', filename_pattern='%(uploader_id)s_%(upload_date)s_%(id)s.%(ext)s'):
    """Download TikTok video"""
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = [
        'yt-dlp',
        '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '--output', os.path.join(output_dir, filename_pattern),
        '--sleep-interval', '3',
        '--max-sleep-interval', '6',
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

def download_playlist(username, count, output_dir):
    """Download multiple videos from a user"""
    url = f"https://www.tiktok.com/@{username}"
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = [
        'yt-dlp',
        '--playlist-items', f'1-{count}',
        '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '--download-archive', os.path.join(output_dir, 'archive.txt'),
        '--output', os.path.join(output_dir, '%(uploader_id)s/%(upload_date)s_%(id)s.%(ext)s'),
        '--sleep-interval', '3',
        '--max-sleep-interval', '6',
        url
    ]
    
    print(f"Downloading {count} videos from @{username} to {output_dir}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Downloaded {count} videos!")
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
    parser = argparse.ArgumentParser(description='Download TikTok videos')
    parser.add_argument('--user', '-u', help='TikTok username (without @)')
    parser.add_argument('--url', '-l', help='Direct TikTok video URL')
    parser.add_argument('--count', '-n', type=int, default=1, help='Number of videos to download')
    parser.add_argument('--output', '-o', default='./downloads', help='Output directory')
    parser.add_argument('--metadata-only', action='store_true', help='Show info only, no download')
    
    args = parser.parse_args()
    
    # Install yt-dlp
    if not install_yt_dlp():
        sys.exit(1)
    
    # Determine URL
    if args.url:
        url = args.url
    elif args.user:
        url = f"https://www.tiktok.com/@{args.user}"
    else:
        parser.print_help()
        sys.exit(1)
    
    # Metadata only mode
    if args.metadata_only:
        print("Fetching video info...")
        info, error = get_video_info(url)
        if info:
            print(f"✓ {info}")
        else:
            print(f"✗ Error: {error}")
        return
    
    # Download
    if args.count == 1:
        download_video(url, args.output)
    else:
        if args.user:
            download_playlist(args.user, args.count, args.output)
        else:
            print("Error: --count requires --user")

if __name__ == '__main__':
    main()
