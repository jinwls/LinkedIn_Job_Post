# Overview

  I came to wonder in what skills a data analyst or any other data related job needed. So to figure the problem, I needed data of the job description for the right job. So, I decided to scrape some job postings from LinkedIn using Scrapy.

### Web Scraping
  However, there was a problem when scraping LinkedIn website. When you scroll down to the bottom of the page it will load more data into the site. This type of scrolling is called **infinite scroll**. The site will load 25 job postings for every scroll. Thus, when you are trying to scrape the data out of the link, you would only get 25 job posting data because it is not loaded yet.

  This site uses AJAX(Asynchronous Javascript And XML), which gives the site the capability of loading the data without reloading the whole website. When the scroll hit the bottom, the javascript will send HTTP request and load new items automatically. So, the biggest problem for scraping these type of website is to figure out the URL javascript used to get new data. 

![화면 기록 2022-06-18 오후 5 16 05](https://user-images.githubusercontent.com/98644650/174429354-51b010e3-4aba-452e-8cea-8ad811e2d86f.gif)

  To figure out the hidden URL I used web dev tool(right-click > Inspect or F12) from Google Chrome. First, you will have to enable '**LogXMLHttpRequest**' from the console option. 

<img src="https://user-images.githubusercontent.com/98644650/174429496-ef1a36e6-2d76-4319-868f-7009143a4f0d.gif" width="250" height="250"/>

![화면 기록 2022-06-18 오후 5 21 31](https://user-images.githubusercontent.com/98644650/174429496-ef1a36e6-2d76-4319-868f-7009143a4f0d.gif)

After that, go to the **Network** tab and scroll the site to the bottom to see the URL that responses to the loaded data. 
