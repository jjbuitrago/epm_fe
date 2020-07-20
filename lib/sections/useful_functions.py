import unidecode


def norm_str(text):
    if text is not None:
        item = {}
        item['label'] = text
        item['value'] = text
        return(item)
