#!/usr/bin/env python3

import os
import argparse

def get_args():
    parser = argparse.ArgumentParser(
        prog="python3 ebook_organizer.py",
        description="Organize a collection of ebook files.")
    parser.add_argument("ebook_dir",
                       help="Directory containing ebook files to organize")
    parser.add_argument("output_dir",
                       help="Directory where organized ebooks will be copied")
    return parser.parse_args()

def main():
    args = get_args()
    print(f"Will organize ebooks from {args.ebook_dir} to {args.output_dir}")

if __name__ == "__main__":
    main()