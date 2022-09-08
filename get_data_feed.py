import requests
from bs4 import BeautifulSoup

def get_feed_from_inshorts(category=None):
    """
    This function gets input feed (technology) from inshorts
    end point and parses the html content and
    builds a json object to send it to elasticsearch
    Args: None
    Returns : json dict with selected category news details
    """
    #print(category)
    data_dict = {}
    formatted_result_dict = {}
    try:
        if category:
            response = requests.get("https://inshorts.com/en/read/{0}".format(category))
        else:
            response = requests.get("https://inshorts.com/en/read/")
    except Exception as e:
        data_dict['success'] = False
        data_dict['error_message'] = str(e)
        return data_dict
    soup = BeautifulSoup(response.text,'lxml')
    news_cards = soup.find_all(class_='news-card')
    if not news_cards:
        data_dict['success'] = False
        data_dict['error_message'] = str(e)
        return data_dict
    for s_card in news_cards:
            try:
                title = s_card.find(class_='news-card-title').find('a').text
            except AttributeError:
                title = None

            try:
                imageUrl = s_card.find(class_='news-card-image')['style'].split("'")[1]
            except AttributeError:
                imageUrl = None

            try:
                url = ('https://www.inshorts.com' + s_card.find(class_='news-card-title')
                   .find('a').get('href'))
            except AttributeError:
                url = None

            try:
                content = s_card.find(class_='news-card-content').find('div').text
            except AttributeError:
                content = None
 
            try:
                author = s_card.find(class_='author').text
            except AttributeError:
                author = None

            try:
                date = s_card.find(clas='date').text
            except AttributeError:
                date = None

            try:
                time = s_card.find(class_='time').text
            except AttributeError:
                time = None

            try:
                read_more_url = s_card.find(class_='read-more').find('a').get('href')
            except AttributeError:
                read_more_url = None
            
            data_dict = {
                "feed_date" : date,
                "feed_time" : time,
                "feed_title" : title,
                "feed_url" : url,
                "feed_image_url" : imageUrl,
                "feed_content" : content,
                "feed_author" : author,
                "feed_url_for_read_more" : read_more_url
            }
            data_dict['success'] = True
    if data_dict['success']:
        for key,val in data_dict.items():
            if not key == 'success' and not val == None:
                formatted_result_dict[key] = val.strip('\n')
    return formatted_result_dict



        
    

        
