from playwright.sync_api import Playwright
import time
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import re
from postClasses import SkeetData
from config import config

SKEET_FINDER_PATH = "html > body > div:nth-child(1) > div > div > div > div > div > main > div > div > div:nth-child(2) > div > div > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > div > div > div:nth-child(2) > div > div:nth-child"
SKEET_CONTENT_PATH = "div > div:nth-child(2) > div:nth-child(2)"
SKEET_USER_HANDLE_PATH = "div:nth-child(1) > div > div"
SKEET_TIMESTAMP_PATH = "div:nth-child(1) > div > a"
SKEET_TEXT_PATH = "div:nth-child(2)"
SKEET_COMMENTS_PATH = "div:nth-child(1)"
SKEET_RESKEETS_PATH = "div:nth-child(2)"
SKEET_LIKES_PATH = "div:nth-child(3)"
QUOTE_SKEET_HANDLE_PATH = "div:nth-child(2) > div > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(1) > div > div"
QUOTE_SKEET_TEXT_PATH = "div:nth-child(2) > div > div:nth-child(2) > div:nth-child(2)"

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

credentials = config("bluesky", "logins.ini")

def FindDaylightSavings():
    currentYear = time.gmtime().tm_year
    for days in range(1,8):
        # TODO: identify daylight savings date to pass into DateParser
        time.strptime()

def CountConverter(countString: str):
    if (countString.find("K")>0):
        return (int(float(countString.replace("K", ""))*1000))
    if (len(countString) == 0):
        return 0
    return int(countString)

def DateParser(date: str):
    dateSplitter = date.split(" at ")
    amPmSplitter = re.split(r"([A | P]M)", dateSplitter[1])
    trimTime = re.sub(r"[\s+]", "", amPmSplitter[0])
    hourMinuteSplit = trimTime.split(":")
    if hourMinuteSplit[0].__len__() < 2:
        hourMinuteSplit[0] = "0" + hourMinuteSplit[0]
        if amPmSplitter[1] == "PM":
            if int(hourMinuteSplit[0]) < 12:
                hourMinuteSplit[0] = str(int(hourMinuteSplit[0])+12)
    # TODO: convert to UTC
    return dateSplitter[0]+ " " + hourMinuteSplit[0] + ":" + hourMinuteSplit[1]


def blueskyScraper(playwright: Playwright, searchQueries, postDepth: int):
    allQueriesHolder = {}
    chromium = playwright.chromium
    browser = chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://bsky.app/")
    page.wait_for_load_state("networkidle")
    page.locator("button[aria-label='Sign in']").click()
    page.wait_for_load_state("networkidle")
    page.get_by_placeholder("Username or email address").fill(credentials["user"])
    page.get_by_placeholder("Password").fill(credentials["password"])
    page.locator("button[aria-label='Next']").click()
    page.wait_for_load_state("networkidle")
    searchBox = page.get_by_role("search")
    for searchQuery in searchQueries:
        postHolder = list()
        searchBox.fill(searchQuery)
        searchBox.press("Enter")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        print(f"Searching for the first {postDepth} posts related to keyword: {searchQuery}")
        for skeets in range(2, postDepth+2):
            linkObject = {"headline": "", "link": ""}
            quoteSkeet = {"quotedUser": "", "quotedText": ""}
            finderPath = SKEET_FINDER_PATH + "(" + str(skeets) + ")"
            page.locator(finderPath).wait_for(state='visible')
            page.locator(finderPath).scroll_into_view_if_needed()
            contentPath = finderPath + " > " + SKEET_CONTENT_PATH
            handlePath = contentPath + " > " + SKEET_USER_HANDLE_PATH
            handleText = page.locator(handlePath).text_content()
            username = handleText.split("@")[0]
            usernameStepOne = re.sub(r"[\xa0]", "", username)
            usernameClean = re.sub(r"[\u202a-\u202e]", "", usernameStepOne)
            handle = handleText.split("@")[1] if len(handleText.split("@")) > 1 else None
            if handle:
                handleClean = "@" + re.sub(r"[\u202a-\u202e]", "", handle)
            timestampPath = contentPath + " > " + SKEET_TIMESTAMP_PATH
            timestamp = page.locator(timestampPath).get_attribute("aria-label")
            timestampClean = DateParser(timestamp)
            if (page.locator(contentPath + " > div:nth-child(4)").is_visible()):
                textBuff = " > div:nth-child(3)"
                interactionBuff = " > div:nth-child(4) > "
                textPath = contentPath + textBuff
                commentsPath = contentPath + interactionBuff + SKEET_COMMENTS_PATH
                reskeetsPath = contentPath + interactionBuff + SKEET_RESKEETS_PATH
                likesPath = contentPath + interactionBuff + SKEET_LIKES_PATH
            else:
                textPath = contentPath + " > " + SKEET_TEXT_PATH
                commentsPath = contentPath + " > div:nth-child(3) > " + SKEET_COMMENTS_PATH
                reskeetsPath = contentPath + " > div:nth-child(3) > " + SKEET_RESKEETS_PATH
                likesPath = contentPath + " > div:nth-child(3) > " + SKEET_LIKES_PATH
            if (page.locator(textPath + " > div:nth-child(2)").is_visible()):
                if (page.locator(textPath + " > div:nth-child(2) > a").is_visible()):
                    linkObject["headline"] = page.locator(textPath + " > div:nth-child(2) > a").get_attribute("aria-label")
                    linkObject["link"] = page.locator(textPath + " > div:nth-child(2) > a").get_attribute("href")
                elif (page.locator(textPath + " > div:nth-child(2) > div > div:nth-child(2)[role='link']").is_visible()):
                    quoteUserWithFormatting = page.locator(textPath + " > " + QUOTE_SKEET_HANDLE_PATH + " > a:nth-child(1)").text_content()
                    quoteUserClean = re.sub(r"[\u202a-\u202e]", "", quoteUserWithFormatting)
                    quoteSkeet["quotedUser"] = quoteUserClean
                    quoteSkeet["quotedText"] = page.locator(textPath + " > " + QUOTE_SKEET_TEXT_PATH).text_content()
                textPath = textPath + " > div:nth-child(1)"
            skeetText = page.locator(textPath).text_content()
            skeetTextRemoveKeywordUppercase = re.sub(searchQuery.capitalize(), "", skeetText)
            skeetTextRemoveKeywordLowercase = re.sub(searchQuery.lower(), "", skeetTextRemoveKeywordUppercase)
            skeetTextRemoveLineBreak = re.sub(r"(\n+)", " ", skeetTextRemoveKeywordLowercase)
            skeetTextRemoveEmptySpace = re.sub("  ", " ", skeetTextRemoveLineBreak)
            skeetTextClean = skeetTextRemoveEmptySpace.strip()
            sentimentScores = sia.polarity_scores(skeetText)
            commentsCount = page.locator(commentsPath).text_content()
            commentsInt = CountConverter(commentsCount)
            reskeetsCount = page.locator(reskeetsPath).text_content()
            reskeetsInt = CountConverter(reskeetsCount)
            likesCount = page.locator(likesPath).text_content()
            likesInt = CountConverter(likesCount)
            sendToDB = SkeetData(timestampClean, usernameClean, handleClean, skeetTextClean, commentsInt, reskeetsInt, likesInt, sentimentScores["compound"], searchQuery)
            if (list(linkObject.values())[0]):
                sendToDB.link_headline = linkObject["headline"]
                sendToDB.link_url = linkObject["link"]
            if (list(quoteSkeet.values())[0]):
                sendToDB.quoted_user = quoteSkeet["quotedUser"]
                sendToDB.quoted_text = quoteSkeet["quotedText"]

            jsonObject = sendToDB.__dict__
            postHolder.append(jsonObject)
        allQueriesHolder[searchQuery] = postHolder
        page.locator("a[aria-label='Home'][role='link']").click()
        page.wait_for_timeout(2000)

    return allQueriesHolder
