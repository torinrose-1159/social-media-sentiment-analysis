from playwright.sync_api import sync_playwright, Playwright
from blueskyScraper import blueskyScraper
import json
import time

with open("parameters.json", "r") as file:
    extractJSON = json.load(file)
    keywords = extractJSON["keywords"]
    platforms = extractJSON["platforms"]

with sync_playwright() as playwright:
    for platform in platforms:
        blueskyOutput = blueskyScraper(playwright, keywords, 100)
        filePath = "scrapeOutputs/bluesky/"+str(int(time.time()))+".json"
        with open(filePath, "w") as file:
            json.dump(blueskyOutput, file)

