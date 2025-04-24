import os
from PyPDF2 import PdfMerger


def get_pdf_files(folder_path):
    """Return a sorted list of PDF file paths in the given folder."""
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    files.sort()
    return [os.path.join(folder_path, f) for f in files]


def merge_pdfs(pdf_files, output_path):
    """Merge the list of PDF files into a single PDF at output_path."""
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()


def main():
    folder = input("Enter the path to the folder containing PDF files: ").strip()
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a valid directory.")
        return
    pdf_files = get_pdf_files(folder)
    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return
    output_file = os.path.join(folder, "merged_output.pdf")
    merge_pdfs(pdf_files, output_file)
    print(f"Merged {len(pdf_files)} PDFs into: {output_file}")


if __name__ == "__main__":
    main()
