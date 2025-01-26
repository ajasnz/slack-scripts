# Downloads and saves media and attachements from a slack .zip export
# You must have a valid slack .zip export for which the access tokens have not expired
# Extract the zip file and place this script in its root (with the folders for each channel
# Run
import os, json, requests

currentDir = os.getcwd()
downloadDir = os.path.join(currentDir, "z_downloaded_files")
os.makedirs(downloadDir, exist_ok=True)

def startup():
    print("Available Channels:")
    channels = [name for name in os.listdir(currentDir) if os.path.isdir(os.path.join(currentDir, name))]
    for index, channel in enumerate(channels):
        print(f"{index} - {channel}")
    print("Enter a comma separated list of the channels you want to download from, enter * to download everything:")
    selectedChannelsList = set(input("-> ").split(","))
    downloadFiles(selectedChannelsList, channels)
    
def downloadFiles(channelList, channels):
    for index, channel in enumerate(channels):
        if str(index) in channelList or "*" in channelList:
            print(f"Downloading from {channel}")
            for day in os.listdir(os.path.join(currentDir, channel)):
                dayExport = json.load(open(os.path.join(currentDir, channel, day), encoding='utf-8'))
                for message in dayExport:
                    if "files" in message:
                        for file in message["files"]:
                            if "url_private_download" in file:
                                fileUrl = file["url_private_download"]
                                fileName = file["name"]
                                filePath = os.path.join(downloadDir, channel, fileName)
                                os.makedirs(os.path.dirname(filePath), exist_ok=True)
                                if not os.path.isfile(filePath):
                                    print(f"Downloading {channel} / {fileName} from {fileUrl}")
                                    response = requests.get(fileUrl, stream=True)
                                    with open(filePath, 'wb') as out_file:
                                        out_file.write(response.content)
                                else:
                                    print(f"Skipping {fileName} from {fileUrl} because it already exists")
    print("\n\n--Done!--")
startup()
