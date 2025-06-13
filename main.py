from playwright.sync_api import sync_playwright, Playwright
from blueskyScraper import blueskyScraper
from database import databaseConnector as db
import json
import shutil
import time
import os
import re

with open("parameters.json", "r") as file:
    extractJSON = json.load(file)
    keywords = extractJSON["keywords"]
    platforms = extractJSON["platforms"]

with sync_playwright() as playwright:
    for platform in platforms:
        if platform == "bluesky":
            for keyword in keywords:
                blueskyOutput = blueskyScraper(playwright, [keyword], 500)
                filePath = f"scrapeOutputs/{platform}/staging/"+str(int(time.time()))+".json"
                with open(filePath, "w") as file:
                    json.dump(blueskyOutput, file)

connection = db.dbConnect("SOCIAL_MEDIA_SENTIMENT")
cursor = db.cursorConnect(connection)

platformFolders = os.listdir("scrapeOutputs")
for platform in platformFolders:
    filesToProcess = os.listdir(f"scrapeOutputs/{platform}/staging")
    if(len(filesToProcess) == 0):
        print(f"No newly scraped posts from {platform}. Moving on to the next platform.")
        continue
    else:
        for filename in filesToProcess:
            sourcePath = os.path.join("scrapeOutputs", platform, "staging", filename)
            destinationPath = os.path.join("scrapeOutputs", platform, "processed", filename)
            with open(f"scrapeOutputs/{platform}/staging/{filename}", "r") as file:
                postExtract = json.load(file)
                for topic in postExtract:
                    for post in postExtract[topic]:
                        db.insertRecord(cursor, platform, post)
            shutil.move(sourcePath, destinationPath)


db.cursorDisconnect(cursor)
db.dbDisconnect(connection)

print("Successfully scraped 500 more posts from each platform for each keyword!")