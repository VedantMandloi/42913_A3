import os
import glob

import networkx as nx

from bs4 import BeautifulSoup
from bs4 import Comment
from tqdm import tqdm

PATH_TO_URL_ID_MAPPING = '../data/Webb_Spam_Corpus_graph_files/url_id_mapping'
PATH_TO_URL_GRAPH_FILE = '../data/Webb_Spam_Corpus_graph_files/url_graph_file'
PATH_TO_CORPUS = '../data/WebbSpamCorpus/'

graph = nx.Graph()

with open(PATH_TO_URL_ID_MAPPING) as file:
    for line in file:
        id, url = line.split()
        graph.add_node(id, url=url)

with open(PATH_TO_URL_GRAPH_FILE) as file:
    for line in file:
        list_of_nodes = line.split()
        source = list_of_nodes[0]
        destination = list_of_nodes[1:]
        for node in destination:
            graph.add_edge(source, node)

graph.remove_nodes_from(list(nx.isolates(graph)))

pr = nx.pagerank(G=graph, alpha=0.85)
for k, v in pr.items():
    graph.add_node(k, pagerank=v)

nx.write_graphml(graph, '../data/graph_for_viz.graphml')

inv_graph = {v: k for k, v in nx.get_node_attributes(graph, 'url').items()}

os.chdir(PATH_TO_CORPUS)
corpus_files = glob.glob('*')

for file in tqdm(corpus_files):

    with open(file, encoding='latin-1') as f:
        soup = BeautifulSoup(f, 'lxml')
    metadata = soup.find_all(string=lambda text: isinstance(text, Comment))

    url = ''
    keywords = ''
    title = ''

    for data in metadata:
        if 'URL:' in data:
            url = data.replace('URL:', '').strip()

        if 'X-Meta-Keywords:' in data:
            keywords = data.replace('X-Meta-Keywords:', '').strip()

        if 'Title:' in data:
            title = data.replace('Title:', '').strip()

    id = inv_graph.get(url, None)
    if id:
        body = soup.getText().strip()

        text = ' '.join((keywords, title, body))
        text = text.replace('\n', ' ').lower()
        text = ' '.join(text.split())

        graph.add_node(id, text=text)

nx.write_gpickle(graph, '../mapped_web_graph.gz')


