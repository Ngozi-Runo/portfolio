#!/usr/bin/env python3
"""
Image Management Script for Portfolio Project

This script helps manage and optimize images for the portfolio website.
It can resize images, convert formats, and generate responsive image variants.
"""

import os
import sys
from PIL import Image
import argparse

def optimize_image(input_path, output_path, max_width=800, quality=85):
    """
    Optimize an image by resizing and compressing it.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the optimized image
        max_width (int): Maximum width for the image
        quality (int): JPEG quality (1-100)
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for JPEG output)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Calculate new dimensions maintaining aspect ratio
            width, height = img.size
            if width > max_width:
                ratio = max_width / width
                new_height = int(height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save with optimization
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            print(f"Optimized: {input_path} -> {output_path}")
            
    except Exception as e:
        print(f"Error optimizing {input_path}: {e}")

def create_responsive_variants(image_path, output_dir):
    """
    Create responsive image variants (small, medium, large).
    
    Args:
        image_path (str): Path to the source image
        output_dir (str): Directory to save variants
    """
    sizes = {
        'small': 400,
        'medium': 800,
        'large': 1200
    }
    
    filename = os.path.splitext(os.path.basename(image_path))[0]
    
    for size_name, width in sizes.items():
        output_path = os.path.join(output_dir, f"{filename}-{size_name}.jpg")
        optimize_image(image_path, output_path, max_width=width)

def optimize_all_images():
    """Optimize all images in the static/images directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, 'static', 'images')
    
    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file)
                # Create backup
                backup_path = file_path + '.backup'
                if not os.path.exists(backup_path):
                    os.rename(file_path, backup_path)
                    optimize_image(backup_path, file_path)

def main():
    parser = argparse.ArgumentParser(description='Manage portfolio images')
    parser.add_argument('--optimize-all', action='store_true', 
                       help='Optimize all images in the project')
    parser.add_argument('--optimize', type=str, 
                       help='Optimize a specific image file')
    parser.add_argument('--create-variants', type=str,
                       help='Create responsive variants of an image')
    parser.add_argument('--quality', type=int, default=85,
                       help='JPEG quality (1-100, default: 85)')
    parser.add_argument('--max-width', type=int, default=800,
                       help='Maximum width for optimization (default: 800)')
    
    args = parser.parse_args()
    
    if args.optimize_all:
        optimize_all_images()
    elif args.optimize:
        if not os.path.exists(args.optimize):
            print(f"Error: File {args.optimize} not found")
            sys.exit(1)
        
        output_path = args.optimize
        optimize_image(args.optimize, output_path, args.max_width, args.quality)
    elif args.create_variants:
        if not os.path.exists(args.create_variants):
            print(f"Error: File {args.create_variants} not found")
            sys.exit(1)
        
        output_dir = os.path.dirname(args.create_variants)
        create_responsive_variants(args.create_variants, output_dir)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
