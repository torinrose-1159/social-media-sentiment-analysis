from playwright.sync_api import sync_playwright, Playwright
from blueskyScraper import blueskyScraper
import json
import time
import re

with open("parameters.json", "r") as file:
    extractJSON = json.load(file)
    keywords = extractJSON["keywords"]
    platforms = extractJSON["platforms"]

with sync_playwright() as playwright:
    for platform in platforms:
        if platform == "bluesky":
            blueskyOutput = blueskyScraper(playwright, ["police", "Elon"], 2)
            filePath = "scrapeOutputs/bluesky/"+str(int(time.time()))+".json"
            with open(filePath, "w") as file:
                output = list()
                for topics in list(blueskyOutput.values()):
                    print(topics)
                    del output[:]
                    for posts in topics:
                        print(posts)
                        jsonFormatting = json.dumps(posts)
                        deleteFormatting = re.sub(r"\\u[0-9a-fA-F]{4}", "", jsonFormatting)
                        output.append(deleteFormatting)
                    json.dump(output, file)

