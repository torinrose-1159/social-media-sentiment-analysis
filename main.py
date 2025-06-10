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
            blueskyOutput = blueskyScraper(playwright, keywords, 2)
            filePath = "scrapeOutputs/bluesky/"+str(int(time.time()))+".json"
            with open(filePath, "w") as file:
                json.dump(blueskyOutput, file)

