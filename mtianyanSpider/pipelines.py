class ElasticSearchPipeline:
    """通用的ElasticSearch存储方法"""

    def process_item(self, item, spider):
        item.save_to_es()
        return item
