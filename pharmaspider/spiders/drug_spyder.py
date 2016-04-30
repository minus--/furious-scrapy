import scrapy
from pharmaspider.items import DrugItem

class DrugSpider(scrapy.Spider):
    name = "drug"
    allowed_domains = ["phct.com.tn"]
    start_urls = ["http://www.phct.com.tn/index.php?option=com_searchproduct&view=searchproduct&layout=ficheprd&refprod=200470&catprd=V"]


    def parse(self, response):        
        print(response.body)
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


