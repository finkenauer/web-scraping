import scrapy

class sucasa(scrapy.Spider):
    name = "sucasa"
    start_urls = [
        #'http://www.sucasa.com.br/listagem.aspx?ddlPretensao=1&cidade=291&ddlBairro=&bairro=&vlVenda=0',
        'http://www.sucasa.com.br/listagem.aspx?pretensao=1&cidade2=291&order=11&page=1&visualizar=1',
    ]

    def parse(self, response):
        for habit in response.xpath('//div[@class="col-xs-12 col-sm-12 col-md-6 col-lg-4 boxImovel"]'):
            habit_id = habit.xpath("div[@class='imovel borderHover1']/div[@class='bgImovel']/figure/p/text()").extract()
            price = habit.xpath("div[@class='imovel borderHover1']/div[@class='bgImovel']/div[@class='features']/div[@class='preco']/text()").extract()
            model = habit.xpath("div[@class='imovel borderHover1']/div[@class='bgImovel']/div[@class='features']/h3/text()").extract()
            yield{
                'imovel_id': (habit_id[0].split(": ")[1]),
                'preco': price,
                'tipo': (model[0].split(" - ")[0]),
                'bairro': habit.xpath("div[@class='imovel borderHover1']/div[@class='bgImovel']/div[@class='features']/p/text()")[0].extract().split(" - ")[0],
                'dorms': habit.xpath("div[@class='imovel borderHover1']/div[@class='bgImovel']/div[@class='features']/p[@class='importantes in_dorm']/span/text()").extract(),
                'suites': habit.xpath("div[@class='imovel borderHover1']/div[@class='bgImovel']/div[@class='features']/p[@class='importantes in_suites']/span/text()").extract(),
                'vagas': habit.xpath("div[@class='imovel borderHover1']/div[@class='bgImovel']/div[@class='features']/p[@class='importantes in_garagens']/span/text()").extract()
            }
        
        total_pages = int(response.xpath("//ul[@class='paginacao']/li[@class='pagina']/strong/text()").extract()[0].split(" de ")[1])
        for page in range(2, total_pages+1):
            yield scrapy.Request('http://www.sucasa.com.br/listagem.aspx?pretensao=1&cidade2=291&order=11&page=%s&visualizar=1' % page, callback=self.parse)

        # next_page = response.xpath("///div[@class='opcoes opcoesBot bottom']/div[@id='dv_page']/ul[@class='paginacao']/li[@class='proximo']/a/i[@class='fa fa-caret-right']").extract_first()
        # if next_page is not None:
        #     #url = response.xpath("//div[@class='opcoes opcoesBot bottom']/div[@id='dv_page']/ul[@class='paginacao']/li[@class='proximo']/a/i[@class='fa fa-caret-right']").xpath("../../../a/i").extract_first()
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
