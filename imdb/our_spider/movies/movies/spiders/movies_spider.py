import scrapy 


class MoviesSpider(scrapy.Spider):
    name = 'all_movies'
    start_urls = ['https://ru.m.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту']

    def parse(self, response):
        for link in response.css('div.mw-category-group ul li a::attr(href)'):
            yield response.follow(link, callback=self.parse_movie)
    
    def parse_movie(self, response):
        film_name = response.css('th.infobox-above::text').get()

        genre_film = response.css('td span[data-wikidata-property-id="P136"] a::text').extract()
        film_director = response.css('td span[data-wikidata-property-id="P57"] a::text').extract()
        film_country = response.css('td span.country-name a::text').get(),
        year_of_make_film = response.css('td span.dtstart::text').get()


        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        url = f'https://www.imdb.com/find/?q={film_name}&ref_=nv_sr_sm'


 
        yield scrapy.Request(url, callback=self.parse_imdb, headers=headers, meta={'film_name': film_name, 
                                                                                   'genre_film': genre_film, 
                                                                                   'film_director': film_director,
                                                                                   'film_country': film_country,
                                                                                   'year_of_make_film': year_of_make_film})


    def parse_imdb(self, response):
        href_value = response.css('.ipc-metadata-list-summary-item__t::attr(href)').get()
        
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        if href_value:
            next_url = f'https://www.imdb.com{href_value}'

            yield scrapy.Request(next_url, callback=self.parse_rating, meta={'film_name': response.meta['film_name'], 
                                                                             'genre_film': response.meta['genre_film'], 
                                                                             'film_director': response.meta['film_director'],
                                                                             'film_country': response.meta['film_country'],
                                                                             'year_of_make_film': response.meta['year_of_make_film']}, headers=headers)

    def parse_rating(self, response):
        rating_value = response.css('span.sc-bde20123-1.cMEQkK::text').get()

        yield {
            'name': response.meta['film_name'],
            'genre': response.meta['genre_film'],
            'director': response.meta['film_director'],
            'country': response.meta['film_country'],
            'year_of_make': response.meta['year_of_make_film'],
            'rating': rating_value
        }





