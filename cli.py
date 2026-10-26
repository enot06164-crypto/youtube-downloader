# CLI entrypoint for linux/headless usage
import argparse, sys, os
sys.path.insert(0, '.')

def main():
    parser = argparse.ArgumentParser(description='Yandex Music Downloader CLI')
    parser.add_argument('--url', required=True, help='Track/album URL')
    parser.add_argument('--out', default='./downloads', help='Output dir')
    parser.add_argument('--quality', default='320', help='Bitrate')
    args = parser.parse_args()
    print(f"CLI mode: download {args.url} to {args.out}")

if __name__ == '__main__':
    main()
