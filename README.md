# Images to PDF

A Python script that looks through subfolders with images and converts those images in each subfolder into a single PDF. If a subfolder contains no images, it will be skipped.

## Requirements

To use this script, you need to install the following Python packages:

```
pillow
reportlab
```

You can install them using pip:

```
pip install pillow reportlab
```

## Usage

### Interactive Mode

```
python images_to_pdf.py
```

This will prompt you to enter the folder containing subfolders with images.

### Command-line Mode

```
python images_to_pdf.py -i path/to/main/folder
```

This will process all subfolders in the specified directory and create a PDF for each subfolder containing images.

### Specifying an Output Folder

```
python images_to_pdf.py -i path/to/main/folder -o path/to/output/folder
```

This will save all generated PDFs to the specified output folder.

### Changing Page Size

```
python images_to_pdf.py -i path/to/main/folder -s letter
```

By default, the script uses A4 page size. You can change it to letter size using the `-s` option.

### Debug Mode

```
python images_to_pdf.py -i path/to/main/folder -d
```

This will print detailed information about the images being processed.

## How It Works

1. The script scans the main folder to find all subfolders
2. For each subfolder, it identifies all image files (jpg, jpeg, png, bmp, gif, tiff, webp)
3. If images are found, they are sorted and converted into a single PDF named after the subfolder
4. The PDF is saved either in the original subfolder or in the specified output folder
5. Folders with no images are skipped

## Features

- Supports multiple image formats (jpg, jpeg, png, bmp, gif, tiff, webp)
- Natural sorting of image files (e.g., img1.jpg, img2.jpg, img10.jpg will be sorted correctly)
- Handles spaces and special characters in folder and file names
- Customizable page size (A4 or Letter)
- Optional output directory for the generated PDFs
- Debug mode for troubleshooting

## Example

If you have a folder structure like:
```
Main_Folder/
  ├── Subfolder1/
  │   ├── img1.jpg
  │   ├── img2.jpg
  │   └── img3.jpg
  ├── Subfolder2/
  │   ├── pic1.png
  │   └── pic2.png
  └── Subfolder3/
      └── (no images)
```

Running the script on `Main_Folder` will create:
```
Main_Folder/
  ├── Subfolder1/
  │   ├── img1.jpg
  │   ├── img2.jpg
  │   ├── img3.jpg
  │   └── Subfolder1.pdf  (contains all 3 images)
  ├── Subfolder2/
  │   ├── pic1.png
  │   ├── pic2.png
  │   └── Subfolder2.pdf  (contains both images)
  └── Subfolder3/
      └── (no images, no PDF created)
```

Or if you specify an output folder, the PDFs will be created there instead.