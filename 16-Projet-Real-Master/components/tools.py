import requests
import base64
from PyPDF2 import PdfReader
import os

def download_to_base64(url):
  """Downloads a file from a URL and returns its base64 encoded content.

  Args:
      url: The URL of the file to download.

  Returns:
      A string containing the base64 encoded content of the downloaded file,
      or None if there was an error downloading the file.
  """
  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    # Read the file content in chunks to avoid loading the entire file in memory
    base64_content = b"".join(base64.b64encode(chunk) for chunk in response.iter_content(1024))
    return base64_content.decode("ascii")
  except requests.exceptions.RequestException as e:
    print(f"Error downloading file: {e}")
    return None

# This function is reading PDF from the start page to final page
# given as input (if less pages exist, then it reads till this last page)
def get_pdf_text(document_path, start_page=1, final_page=10):
    reader = PdfReader(document_path)
    number_of_pages = len(reader.pages)

    page = ''
    for page_num in range(start_page - 1, min(number_of_pages, final_page)):
        page += reader.pages[page_num].extract_text()
    return page

def download_pdf_file(url: str):
    """Download PDF from given URL to local directory.

    :param url: The url of the PDF file to be downloaded
    :return: True if PDF file was successfully downloaded, otherwise False.
    """

    # Request URL and get response object
    response = requests.get(url, stream=True)

    # isolate PDF filename from URL
    pdf_file_name = os.path.basename(url).split("?")[0]
    if response.status_code == 200:
        # Save in current working directory
        filepath = os.path.join(os.getcwd(), pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{pdf_file_name} was successfully saved!')
            return True, filepath
    else:
        print(f'Uh oh! Could not download {pdf_file_name},')
        print(f'HTTP response status code: {response.status_code}')
        return False