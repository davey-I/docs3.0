from bottle import route, run, template, static_file, response, request
import os

PAGES_DIR = '/home/inderdav/src/docs3.0/pages'

@route('/')
def index():
    return static_file('index.html', root='/home/inderdav/src/docs3.0')

@route('/static/<filename>')
def servers_static(filename):
    return static_file(filename, root='/home/inderdav/src/docs3.0')

@route('/pages/<pagename>')
def serve_page(pagename):
    return static_file(pagename, root='/home/inderdav/src/docs3.0/pages')

@route('/save_page', method='POST')
def save_page():
    data = request.json
    page_name = data.get('page')
    new_content = data.get('content')

    if not page_name or not new_content:
        response.status = 400
        return {'status': 'Missing data'}

    file_path = os.path.join(PAGES_DIR, f'{page_name}.html')

    if not os.path.exists(file_path):
        response.status = 404
        return {'status': 'Page not found'}

    with open(file_path, 'a', encoding='utf-8') as f:
        f.write('\n' + new_content + '\n')

    return {'status': f'Content appended to {page_name}.html'}

run(host='localhost', port=8000, debug=True) 