import uvicorn
import networkx as nx

from tqdm import tqdm
from starlette.applications import Starlette
from starlette.responses import UJSONResponse

app = Starlette()


graph = nx.read_gpickle('../data/mapped_web_graph.gz')


def search_web_graph(text: str) -> list:
    results = []
    for key, value in tqdm(graph.nodes(data=True)):

        web_text = value.get('text', '').lower().split()

        word_list = [word.lower() for word in text.split()]

        if all(word in web_text for word in word_list):

            return_text = ''

            for word in word_list:
                word_index = web_text.index(word)
                occur = ' '.join(web_text[word_index-5:word_index+5])
                return_text += occur

            results.append({'id': key,
                            'url': value.get('url', None),
                            'pagerank': value.get('pagerank', None),
                            'text': return_text})

        elif any(word in web_text for word in word_list):

            return_text = ''

            for word in word_list:
                try:
                    word_index = web_text.index(word)
                    return_text += ' '.join(web_text[word_index-5:word_index+5])
                except ValueError:
                    continue

            results.append({'id': key,
                            'url': value.get('url', None),
                            'pagerank': value.get('pagerank', None),
                            'text': return_text})
    return results


def get_ranked_results(text: str) -> list:
    results = search_web_graph(text)
    results = sorted(results, key=lambda k: k['pagerank'], reverse=True)
    return results[:20]


@app.route('/search', methods=['POST'])
async def run_search(request):
    text = await request.json()
    results = get_ranked_results(text['text'])
    return UJSONResponse({'Results': results})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, debug=False, log_level='info')

