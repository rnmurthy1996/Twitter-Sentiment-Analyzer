import GetOldTweets3 as got
from datetime import date, timedelta
import matplotlib.pyplot as plt

def Sentiment_Analyzer():

    #populate lists with negative and positive connotative words
    with open('negative.txt') as f:
        negWords = f.read().splitlines()

    with open('positive.txt') as f:
        posWords = f.read().splitlines()

    count = 1

    while True:
        #end program if 4 queries have already been enteres
        if(count > 4):
            break

        #request user input and terminate if requested
        print("Enter search term you want to analyze twitter sentiment for (Ex. \"Coronavirus\"). Enter \"END\" to end program:")
        query = input();
        if(query == "END"):
            break
        print("Enter start date for analysis (MM/DD/YYYY):")
        startDate = input();
        print("Enter end date for analysis (MM/DD/YYYY):")
        endDate = input();

        startArr = startDate.split("/")
        endArr = endDate.split("/")
        startMonth = startArr[0]
        startDay = startArr[1]
        startYear = startArr[2]
        endMonth = endArr[0]
        endDay = endArr[1]
        endYear = endArr[2]

        start = date(int(startYear), int(startMonth), int(startDay))
        end = date(int(endYear), int(endMonth), int(endDay)) - timedelta(days=1)

        dict = {}

        #run sentiment analysis on query from start date to end date
        while start <= end:
            print(str(start) + " - " + query)
            date1 = start
            year1 = date1.strftime("%Y")
            month1 = date1.strftime("%m")
            day1 = date1.strftime("%d")

            date2 = date1 + timedelta(days=1)
            year2 = date2.strftime("%Y")
            month2 = date2.strftime("%m")
            day2 = date2.strftime("%d")

            start += timedelta(days=1)

            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query)\
                                                   .setSince(year1+"-"+month1+"-"+day1)\
                                                   .setUntil(year2+"-"+month2+"-"+day2)\
                                                   .setTopTweets(True)\
                                                   .setMaxTweets(10)
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)
            negCount = 0
            posCount = 0;
            for tweet in tweets:
                for posWord in posWords:
                    if posWord in tweet.text:
                        posCount += 1
                for negWord in negWords:
                    if negWord in tweet.text:
                        negCount += 1

            #populate dict with daily sentiment ratios
            if(negCount > 0):
                dict[start] = float(posCount)/float(negCount)
            else:
                dict[start] = 0

        color = ""
        if(count % 4 == 1): color = "b"
        elif(count % 4 == 2): color = "g"
        elif(count % 4 == 3): color = "r"
        elif(count % 4 == 0): color = "y"
        count += 1

        plt.xlabel('Date')
        plt.ylabel('Sentiment Ratio')
        j = 0
        sum = 0

        for key in dict.keys():
            j += 1
            sum += dict.get(key)
        avg = sum/float(j)

        i = 0
        #plot daily sentiment ratios and add query to legend
        for key in dict.keys():
            plt.plot(key, dict.get(key), color + 'o', label=query + ': Average = ' + str(round(avg, 2)) if i == 0 else "")
            i += 1
            sum += dict.get(key)

        #add average daily sentiment ratio line for query
        keyList = list(dict.keys())
        date1 = keyList[0]
        date2 = keyList[len(keyList)-1]
        plt.plot([date1, date2], [avg, avg], color + '-')


Sentiment_Analyzer()
plt.legend(loc="upper left")
plt.show()
