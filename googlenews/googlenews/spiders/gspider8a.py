import scrapy
from googlenews.items import GooglenewsItem
from scrapy.loader import ItemLoader
import nltk
from newspaper import Article
import datetime
from textblob import TextBlob
import string

class gSpider(scrapy.Spider):
    # nltk.download('punkt')
    name = 'gnews8a'
    delta = datetime.timedelta(days=1)

    # this is where we put skipped list
    skipped = ["Financial Times"]

    # Change Parameter Here, 
    startDate =  datetime.date(2021, 8, 23)
    endDate = datetime.date(2021, 8, 25)
    region = "south-korea"
    query = "semiconductor"

    def start_requests(self):
        while self.startDate <= self.endDate:
            activeDate = self.startDate.strftime("%m/%d/%Y")
            yield scrapy.Request(f'https://www.google.com/search?q={self.query}+{self.region}&rlz=1C1ONGR_enSG933SG933&tbs=cdr:1,cd_min:{activeDate},cd_max:{activeDate},sbd:1&tbm=nws&sxsrf=ALeKk01aflpQNP1ZZ_T4be6c1j0AaGca-g:1629088758656&source=lnt&sa=X&ved=2ahUKEwiVoJHG3LTyAhUIA3IKHUJTA3gQpwV6BAgHECw&biw=1920&bih=969&dpr=1')
            self.startDate += self.delta
    
    def parse(self, response):

        for articles in response.css('div.dbsr'):
            
            news_office = articles.css('div.XTjFC.WF4CUc::text').get()

            # a function to clean article
            def clean_article(value):
                translation= str.maketrans("","",string.punctuation)
                cleanArticle = value.translate(translation)
                return cleanArticle

            if news_office not in self.skipped:

                # summarizer start here
                url = articles.css('a::attr(href)').get()

                try:
                    article = Article(url)
                    article.download()
                    article.parse()
                    article.nlp()
                    
                    summary = article.summary
                    new_summary = clean_article(summary)

                    tokenizer = nltk.tokenize.TreebankWordTokenizer()
                    tokens = tokenizer.tokenize(new_summary)
                    join_tokens = ",".join(tokens)

                    stemmer = nltk.stem.PorterStemmer()
                    join_stemmer = ",".join(stemmer.stem(token) for token in tokens)

                    lemmatizer = nltk.stem.WordNetLemmatizer()
                    join_lemmatizer = ",".join(lemmatizer.lemmatize(token) for token in tokens)

                    fullText = article.text
                    analysis = TextBlob(fullText)
                    sentiment = analysis.polarity
                    subjective = analysis.subjectivity

                except:
                    summary = articles.css('div.Y3v8qd::text').get()
                    new_summary = clean_article(summary)

                    tokenizer = nltk.tokenize.TreebankWordTokenizer()
                    tokens = tokenizer.tokenize(new_summary)
                    join_tokens = ",".join(tokens)

                    stemmer = nltk.stem.PorterStemmer()
                    join_stemmer = ",".join(stemmer.stem(token) for token in tokens)

                    lemmatizer = nltk.stem.WordNetLemmatizer()
                    join_lemmatizer = ",".join(lemmatizer.lemmatize(token) for token in tokens)

                    fullText = article.text
                    analysis = TextBlob(fullText)
                    sentiment = analysis.polarity
                    subjective = analysis.subjectivity

                # summarizer end here

                l = ItemLoader(item = GooglenewsItem(), selector=articles)

                l.add_css('title', 'div.JheGif.nDgy9d')
                l.add_value('excerpt', summary)
                l.add_css('source','div.XTjFC.WF4CUc')
                l.add_css('date', 'span.WG9SHc span')
                l.add_value('query', self.query)
                # l.add_value('start', self.start)
                # l.add_value('end',self.end)
                l.add_value('region', self.region)
                l.add_value('tokens', join_tokens)
                l.add_value('stemmed',join_stemmer)
                l.add_value('lemmatized', join_lemmatizer)
                l.add_value('sentiment', sentiment)
                l.add_value('subjective', subjective)
                l.add_css('link','a::attr(href)')

                yield l.load_item()
            
            else:
                pass


        # nextPage = response.css('[id="pnnext"]').attrib['href']
        # nextLink = "https://google.com" + nextPage

        # if nextPage is not None:
        #     yield response.follow(nextLink, callback=self.parse)