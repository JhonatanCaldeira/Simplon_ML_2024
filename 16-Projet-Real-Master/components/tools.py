import requests
import base64

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