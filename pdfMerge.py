import sys
import PyPDF2 as pdf

def pdfMerger(file_list, output_name):
    try:
        if len(file_list) < 2:
            print("Please provide at least 2 PDF files to merge.")
            return

        merger = pdf.PdfMerger()
        for filename in file_list:
            with open(filename, 'rb') as file:
                pdf_reader = pdf.PdfReader(file)
                merger.append(pdf_reader)

        with open(output_name, 'wb') as output_file:
            merger.write(output_file)

    except Exception as e:
        print("An error occurred while merging PDF files:", e)

    finally:
        for file in file_list:
            print(file)
        print("Merged PDF saved as", output_name)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python pdf_merge.py output.pdf input1.pdf input2.pdf [input3.pdf ...]")
    else:
        output_name = sys.argv[1]
        input_files = sys.argv[2:]
        pdfMerger(input_files, output_name)
