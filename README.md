# Overview

  I came to wonder in what skills a data analyst or any other data related job needed. So to figure the problem, I needed data of the job description for the right job. So, I decided to scrape some job postings from LinkedIn using Scrapy.


### Web Scraping
  However, there was a problem when scraping LinkedIn website. When you scroll down to the bottom of the page it will load more data into the site. This type of scrolling is called **infinite scroll**. The site will load 25 job postings for every scroll. Thus, when you are trying to scrape the data out of the link, you would only get 25 job posting data because it is not loaded yet.

  This site uses AJAX(Asynchronous Javascript And XML), which gives the site the capability of loading the data without reloading the whole website. When the scroll hit the bottom, the javascript will send HTTP request and load new items automatically. So, the biggest problem for scraping these type of website is to figure out the URL javascript used to get new data. 
  
<p align="center">
  <img src="https://user-images.githubusercontent.com/98644650/174429354-51b010e3-4aba-452e-8cea-8ad811e2d86f.gif" width="500" height="281">
</p>

  To figure out the hidden URL I used web dev tool `right-click > Inspect or F12` from Google Chrome. First, you will have to enable '**LogXMLHttpRequest**' from the console option. 
  
<p align="center">
  <img src="https://user-images.githubusercontent.com/98644650/174429496-ef1a36e6-2d76-4319-868f-7009143a4f0d.gif" width="500" height="281"/>
</p>

After that, go to the **Network** tab and scroll the site to the bottom to see the URL that responses to the loaded data.

```python
  def start_request(self):
      urls = [f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&location=%EB%AF%B8%EA%B5%AD&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&start={page}' \ 
              for page in range(25,1000,25) for keyword in ['data%20specialist','data%20analyst','data%20scientist','data%20engineer']]
        for url in urls:
            yield Request(url, callback=self.parse)
```

  The URL should look something like this. The last two digits will be updated every loading of 25 job postings(multiple of 25). So, I used for loop to get request for the selected pages. Each page will get request and move on to the next step, `parsing`, by defining the callback function in `Request()` function. 

```python
  def parse(self, response):
    for link in response.css('div.base-card a::attr(href)'):
        yield response.follow(link.get(), callback=self.parse_list)
        time.sleep(0.5)
```
  The link that has been requested, only contains the list of title and the company, but does not contain the description of each postings. So, you will have to follow through each job description URL. Here again I used for loop to go through every description link that has been selected using CSS selector. Also, try to use some methods like `time.sleep()` to avoid your IP from getting banned. 
  
```python
  def parse_lists(self, response):
    l = ItemLoader(item = JobItem(), selector = response)
    
    l.add_css('title', 'h1 ::text')
    l.add_css('company', 'a.topcard__org-name-link ::text')
    ...
    
    yield l.load_item()
```

  I have used the built-in functions in scrapy, `Items` and `Item Loaders`, to contain data. `Items` provide the container for the data scrapped and `Item Loaders` provide the mechanism for populating the item containers. Good thing about using `Item Loaders` is that you can automate common tasks like cleaning the extracted data before containing it.
  
Check [items.py](https://github.com/jinwls/LinkedIn_Job_Post/blob/main/job/job/items.py) and [job.py](https://github.com/jinwls/LinkedIn_Job_Post/blob/main/job/job/spiders/job.py) for more details. 


### Data Cleaning
For data cleaning, I will show few of the codes that I used to clean my data. 

  **1. Removing newlines**
  
  ```python
    def remove_newlines(text):
      Newlines_removed = text.replace('\\n', ' ')
                             .replace('\n', ' ')
                             .replace('\t', ' ')
                             .replace('\\', ' ')
                             .replace('. com', '.com')
      return Newlines_removed
  ``` 
  **2. Removing whitespace**
  
  ```python
    def remove_whitespace(text):
      text = text.replace('?', ' ? ')
                 .replace(')', ' ) ')
                 .replace('(', ' ( ')
      Whitespace_removed = text.strip()
      return Whitespace_removed
  ```
  **3. Removing repeated words**
  
  ```python
    def remove_repeat(text):
      pattern = re.compile(r'([A-Za-z])\1{1,}', re.DOTALL)
      Repetition_removed = pattern.sub(r'\1\1', text)
      return Repetition_removed
  ```
  **4. Removing Stopwords**
  
  ```python
  from nltk.corpus import stopwords 
  nltk.download('stopwords') 
  from nltk.tokenize import word_tokenize 

    class StopwordRemove(object):
      def __call__(self, values):
        values = ' '.join(values).strip()
        Token_list = values.split(' ')
        stopword = stopwords.word('english')
        stopword = set(stopword)
        
        # remove contraction words
        for word in Token_list:
          if word in contraction_map:
            token = [item.replace(word, contraction_map[word]) for item in Token_list]
        # convert back to one string
        values = ' '.join(str(word) for word in Token_list)
        
        # remove stopwords
        values = repr(values)
        Stopword_removed = [word for word in word_tokenize(values) if word not in stopword]
        Stopword_removed = ' '.join(Stopword_removed)
        Stopword_removed = Stopword_removed.replace("'", '').replace('"', '')
        return Stopword_removed
  ```
See [This Publication](https://towardsdatascience.com/cleaning-preprocessing-text-data-by-building-nlp-pipeline-853148add68a) by Kajal Yadav for more detail about Data Cleaning functions. Also, check [tidy.py](https://github.com/jinwls/LinkedIn_Job_Post/blob/main/job/job/tidy.py) for more details.


### Creating Pipeline for SQL Connection
  I used `PostgreSQL` and before connecting python to the postgreSQL database server, I created the table using the following code on postgreSQL.
```SQL
    CREATE TABLE public.JobPost
(
    id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
    job character varying(100),
    company character varying(100),
    city character varying(100),
    state character varying(100),
    datePosted date,
    jobType character varying(100),
    jobLevel character varying(100),
    jobIndustry character varying(100),
    jobFunction character varying,
    jobDetail character varying(8000),
	dateScraped date default CURRENT_DATE
);

```
After creating the table, to connect to the postgreSQL database server in python, you need `psycopg` library. Use the `connect()` function of the `psycopg2` modeule. By using the `connection` function, you can create new `cursor` to execute any SQL statements. 

```python     
    def get_connection(self):
       self.conn = psycopg2.connect(
              host = 'localhost',
              dbname = 'LinkedinPost',
              user = 'postgres' # your userid here
              password = 'password' # your password here
          )
       self.cur = self.conn.cursor() 
```

When you are inserting value, assign it by using `item['Container Name']`.

```python
  def process_item(self, item, spider):
      self.cur.execute(f"insert into public.JobPost(job, company, city, states, dateposted, jobtype, joblevel, jobindustry, jobfunction, jobdetail) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(
                item['job'],
                item['company'],
                item['city'],
                item['state'],
                item['date'],
                item['type'],
                item['level'],
                item['industry'],
                item['function'],
                item['detail']))
      self.conn.commit() 
```

You could also add an additional SQL statement to get rid of the duplicate values because it might scrape the same data when you are using it multiple times. 

```python
    self.cur.execute("""
                    DELETE FROM public.JobPost a
                        USING   public.JobPost b
                    WHERE   a.id < b.id 
                        AND a.job = b.job
                        AND a.company = b.company
                        AND a.dateposted = b.dateposted
                        AND a.city = b.city
                        AND a.states = b.states
                        AND a.joblevel = b.joblevel;
                    """)
```

Finally, close the commuinication with the database server by calling the `close()` method of the `cursor` and the `connection` objects. Also, to apply the pipeline , make sure to assign it in the `setting.py`.

```python
ITEM_PIPELINES = {'job.pipelines.JobPostgreSQL': 300}
```

Check [pipelines.py](https://github.com/jinwls/LinkedIn_Job_Post/blob/main/job/job/settings.py) for more details.

And that's it!! Run the file and get your own data of LinkedIn job posts!!
