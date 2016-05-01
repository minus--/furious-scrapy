import scrapy
from pharmaspider.items import DrugItem

class PharmaSpider(scrapy.Spider):
    name = "pharma"
    allowed_domains = ["phct.com.tn"]
    start_urls = ["http://www.phct.com.tn/index.php?option=com_searchproduct&view=searchproduct&ctg=M&Itemid=48&lang=fr"]

    def parse(self, response):
        response.xpath('//form[@name="form_gd_public"]').extract()
        url = response.xpath('//form[@name="form_gd_public"]/@action').extract()
        form_name = response.xpath('//form[@name="form_gd_public"]/@name').extract()
        form_id = response.xpath('//form[@name="form_gd_public"]/@id').extract()
        drug_id = response.xpath('//form[@name="form_gd_public"]//select[@id="dci"]/option/@value').extract()
        drug_name = response.xpath('//form[@name="form_gd_public"]//select[@id="dci"]/option/text()').extract()
        drug_dict = zip(drug_id, drug_name)
        for key,value in drug_dict:
            yield scrapy.FormRequest.from_response(
                response,
                formname = 'form_gd_public',
                formdata={
                'catprd': 'M',
                'classe': '',
                'dci': key,
                'opr': '1'
                },
                callback=self.parse_drug_list)


    def parse_drug_list(self, response):
        id_list = response.xpath('//div[@class="resultbox"]//img[@class="fiche"]/@id').extract()
        for id in id_list:
            url = "http://www.phct.com.tn/index.php?option=com_searchproduct&view=searchproduct&layout=ficheprd&refprod=%d&catprd=V" % int(id)
            yield scrapy.Request(url, callback=self.parse_drug)


    def parse_drug(self, response):        
        drug = DrugItem()
        name = response.xpath('//font/text()').extract()
        drug['name'] = name[0]
        drug_label = []
        drug_value = []
        titles = response.xpath('//table//th')
        for title in titles:
            res = title.xpath('.//text()').extract()
            if len(res) > 0:
                drug_label.append(res[0])
        items = response.xpath('//table//td')
        for item in items:
            res = item.xpath('.//text()').extract()
            if len(res) > 0:
                drug_value.append(res[0])

        drug_def = zip(drug_label,drug_value)
        drug['price'] = 'N/A'
        for key, value in drug_def:
            if key == 'Code Produit :':
                drug['code'] = value
            elif key == 'DCI1 :':
                drug['dci'] = value
            elif key == 'Fournisseur :':
                drug['lab'] = value
            elif key == 'Designation classe :':
                drug['med_class'] = value
            elif key == 'Prix pharmacien HT :':
                drug['price'] = value
            elif key == 'Disp. Part. :':
                drug['disp_part'] = value

        yield drug


