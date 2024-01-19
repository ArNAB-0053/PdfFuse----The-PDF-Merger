import requests
import configparser

from flask import Flask, render_template, request, send_file, redirect
import PyPDF2 as pdf
import io

app = Flask(__name__)

def pdfMerger(file_list, output_filename):
    try:
        if len(file_list) < 2:
            return None

        merger = pdf.PdfMerger()
        for filename in file_list:
            with open(filename, 'rb') as file:
                pdf_reader = pdf.PdfReader(file)
                merger.append(pdf_reader)

        output_stream = io.BytesIO()
        merger.write(output_stream)
        output_stream.seek(0)
        return output_stream, output_filename

    except Exception as e:
        print("An error occurred while merging PDF files:", e)
        return None, None


@app.route("/", methods=["GET", "POST"])
def download_pdf():
    if request.method == "POST":
        files = request.files.getlist("file")
        file_names = []

        for file in files:
            if file and file.filename.endswith(".pdf"):
                file.save(file.filename)
                file_names.append(file.filename)

        merged_pdf, output_filename = pdfMerger(file_names, request.form.get("output_filename"))

        if 'merge-btn' in request.form:
            # Merge PDFs button was clicked
            if merged_pdf is not None and output_filename:
                return send_file(
                    merged_pdf,
                    download_name=output_filename + ".pdf",
                    as_attachment=False,
                    mimetype="application/pdf"
                )
            else:
                return "Error occurred while merging PDF files. Please provide at least 2 PDF files."

        elif 'download-btn' in request.form:
            # Download button was clicked
            if merged_pdf is not None and output_filename:
                return send_file(
                    merged_pdf,
                    download_name=output_filename + ".pdf",
                    as_attachment=True,
                    mimetype="application/pdf"
                )
            else:
                return "Error occurred while merging PDF files. Please provide at least 2 PDF files."

    return render_template("index.html")

@app.route("/home")
def home():
    return redirect("/")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443)
