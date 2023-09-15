from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download_file')
def download_file():
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np

    def get_topics_page():
        topics_url = 'https://github.com/topics'
        response = requests.get(topics_url)
        if response.status_code != 200:
            raise Exception('Failed to load page {}'.format(topics_url))
        doc = BeautifulSoup(response.text, 'html.parser')
        return doc

    doc = get_topics_page()

    def get_topic_titles(doc):
        selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
        topic_title_tags = doc.find_all('p', {'class': selection_class})
        topic_titles = []
        for tag in topic_title_tags:
            topic_titles.append(tag.text)
        return topic_titles

    titles = get_topic_titles(doc)

    def get_topic_desc(doc):
        selection_class = 'f5 color-fg-muted mb-0 mt-1'
        topic_desc_tags = doc.find_all('p', {'class': selection_class})
        topic_desc = []
        for tag in topic_desc_tags:
            topic_desc.append(tag.text.strip())
        return topic_desc
    desc = get_topic_desc(doc)
    topics_dict = {
        'Title': titles,
        'Description': desc
    }
    topics_df = pd.DataFrame(topics_dict)
    topics_df.to_csv('topics.csv')
    print("File downloaded ")
    return 'CSV file downloaded as "topics.csv"!'


if __name__ == '__main__':
    app.run(debug=True)
