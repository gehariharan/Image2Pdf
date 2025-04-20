import os
import argparse
from pathlib import Path
from PIL import Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas

def get_image_files(directory):
    """Get all image files in a directory"""
    # Define image extensions in lowercase
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
    image_files = []

    # Use a set to track file paths we've already added (case-insensitive on Windows)
    added_files = set()

    # Get all files in the directory
    directory_path = Path(directory)
    all_files = list(directory_path.iterdir())

    # Filter for image files
    for file_path in all_files:
        if file_path.is_file():
            # Check if the file extension matches any of our image extensions (case-insensitive)
            file_ext = file_path.suffix.lower()
            if file_ext in image_extensions:
                # Convert to absolute path to ensure uniqueness
                abs_path = file_path.absolute()
                # On Windows, use lowercase path for comparison to avoid duplicates
                path_key = str(abs_path).lower() if os.name == 'nt' else str(abs_path)

                if path_key not in added_files:
                    image_files.append(file_path)
                    added_files.add(path_key)

    # Sort files by name to maintain order
    # Try to sort numerically if filenames contain numbers (e.g., img1.jpg, img2.jpg, img10.jpg)
    def natural_sort_key(s):
        import re
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s.name))]

    try:
        image_files.sort(key=natural_sort_key)
    except Exception:
        # Fall back to regular sorting if natural sort fails
        image_files.sort()

    return image_files

def create_pdf_from_images(image_files, output_pdf_path, pagesize=A4):
    """Create a PDF from a list of image files"""
    if not image_files:
        return False

    try:
        # Create a canvas with the specified page size
        c = canvas.Canvas(output_pdf_path, pagesize=pagesize)
        width, height = pagesize  # Page size in points

        for img_path in image_files:
            try:
                # Convert Path object to string if it's not already
                img_path_str = str(img_path)

                img = Image.open(img_path_str)

                # Calculate the scaling factor to fit the image within the page
                img_width, img_height = img.size
                width_ratio = width / img_width
                height_ratio = height / img_height
                ratio = min(width_ratio, height_ratio) * 0.9  # 90% of the page

                # Calculate new dimensions
                new_width = img_width * ratio
                new_height = img_height * ratio

                # Calculate position to center the image on the page
                x_pos = (width - new_width) / 2
                y_pos = (height - new_height) / 2

                # Draw the image on the canvas
                c.drawImage(img_path_str, x_pos, y_pos, width=new_width, height=new_height)

                # Add image filename as a caption at the bottom of the page (optional)
                # c.setFont("Helvetica", 8)
                # c.drawCentredString(width / 2, 20, Path(img_path).name)

                # Add a new page for the next image
                c.showPage()

            except Exception as e:
                print(f"Error processing image {img_path}: {e}")

        # Save the PDF
        c.save()
        return True
    except Exception as e:
        print(f"Error creating PDF {output_pdf_path}: {e}")
        return False

def process_subfolders(main_folder, output_folder=None, page_size=A4, debug=False):
    """Process all subfolders in the main folder"""
    main_folder_path = Path(main_folder)

    # Set up output folder if specified
    if output_folder:
        output_path = Path(output_folder)
        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = main_folder_path

    # Get all subfolders
    subfolders = [f for f in main_folder_path.iterdir() if f.is_dir()]

    if not subfolders:
        print(f"No subfolders found in {main_folder}")
        return

    print(f"Found {len(subfolders)} subfolders in {main_folder}")

    # Process each subfolder
    pdf_count = 0
    for folder in subfolders:
        print(f"Processing folder: {folder.name}")

        # Get all image files in the subfolder
        image_files = get_image_files(folder)

        if not image_files:
            print(f"  No image files found in {folder.name}, skipping...")
            continue

        print(f"  Found {len(image_files)} images")

        # Print image list in debug mode
        if debug:
            print("  Image files to be processed:")
            for i, img in enumerate(image_files, 1):
                print(f"    {i}. {img.name}")

        # Create PDF output path - sanitize folder name for the PDF filename
        safe_name = ''.join(c for c in folder.name if c.isalnum() or c in ' _-()[]{}.')
        if not safe_name:
            safe_name = "folder"  # Fallback if name becomes empty after sanitizing

        pdf_output_path = output_path / f"{safe_name}.pdf"

        # Create PDF from images - convert Path to string
        if create_pdf_from_images(image_files, str(pdf_output_path), pagesize=page_size):
            print(f"  Created PDF: {pdf_output_path}")
            pdf_count += 1

    print(f"\nProcessed {len(subfolders)} folders, created {pdf_count} PDFs.")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Convert images in subfolders to PDFs")
    parser.add_argument("-i", "--input", help="Input folder containing subfolders with images")
    parser.add_argument("-o", "--output", help="Output folder for the generated PDFs (optional)")
    parser.add_argument("-s", "--size", choices=['a4', 'letter'], default='a4',
                        help="Page size for the PDF (default: a4)")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug mode to print detailed information")

    args = parser.parse_args()

    # If input folder is provided via command line, use it
    if args.input:
        main_folder = args.input
    else:
        # Otherwise, ask the user for input
        main_folder = input("Enter the folder containing subfolders with images: ")

    # Check if the folder exists
    if not os.path.isdir(main_folder):
        print(f"Error: The folder '{main_folder}' does not exist.")
        return

    # Set page size
    page_size = A4 if args.size.lower() == 'a4' else letter

    # Process the subfolders
    process_subfolders(main_folder, args.output, page_size, args.debug)

if __name__ == "__main__":
    main()
