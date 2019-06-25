from google_drive_downloader import GoogleDriveDownloader as gdd

gdd.download_file_from_google_drive(
    file_id="0B7XkCwpI5KDYNlNUTTlSS21pQmM",
    dest_path="./GoogleNews-vectors-negative300.bin.gz",
    unzip=False
)
