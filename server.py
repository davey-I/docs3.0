from bottle import route, run, template, static_file, response, request
from string import Template
import os
from bs4 import BeautifulSoup as bs
import re

PAGES_DIR = '/home/inderdav/src/docs3.0/pages'

@route('/')
def index():
    return static_file('index.html', root='/home/inderdav/src/docs3.0')

@route('/static/<filename>')
def servers_static(filename):
    return static_file(filename, root='/home/inderdav/src/docs3.0')

@route('/prism/<filename>')
def serve_prism(filename):
    return static_file(filename, root='/home/inderdav/src/docs3.0/prism')

@route('/pages/<pagename>')
def serve_page(pagename):
    return static_file(pagename, root='/home/inderdav/src/docs3.0/pages')

#################################
### ADD NEW CHAPTER TO NOTEPAGE #
#################################

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

    # Parse existing HTML file
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = bs(f, 'html.parser')

    # Parse new content and append to <body>
    body = soup.body
    if body:
        body.append(bs(new_content, 'html.parser'))
    else:
        return {'status': 'No <body> tag found in HTML'}

    # Write back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return {'status': f'Content added to <body> in {page_name}.html'}



##############################
### ADD NEW PAGE TO NOTEBOOK #
##############################

@route('/add_page', method='POST')
def add_page():
    data = request.json
    page_name = data.get('page')
    file_path = os.path.join(PAGES_DIR, f'{page_name}.html')
    template = Template('''<!DOCTYPE html>
<html>
<head>
    <title>$ID</title>
    <link rel="stylesheet" href=" ../static/style.css">
    <link rel="stylesheet" href="../prism/prism.css">
</head>
<body class="body">
    <h1 class="pagetitle">$ID</h1>

    <!-- Sidebar -->
    <div id="sidbear-enclosure-open-$ID" class="sidbear-enclosure-open">
        <button id="sidbear-enclosure-button-$ID" class="sidbear-enclosure-button-open" onclick="toggle_sidebar()" type="button">
            <svg width="30" height="30" viewBox="0 0 100 80" fill="white" xmlns="http://www.w3.org/2000/svg">
                <rect width="100" height="10"></rect>
                <rect y="30" width="100" height="10"></rect>
                <rect y="60" width="100" height="10"></rect>
             </svg>
        </button>
        <div id="sidebar-mainbox-$ID" class="sidebar-mainbox-open">
        
            <div id="sidebar-subbox-1" class="sidebar-subbox-open" onclick=" append_foldable_content()">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
                    stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="16"/>
                    <line x1="8" y1="12" x2="16" y2="12"/>
                 </svg>
            </div>

            <div id="sidebar-subbox-2" class="sidebar-subbox-open">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
                    stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M9.09 9C9.32591 8.33109 9.78918 7.76807 10.4 7.41421C11.0108 7.06036 11.7266 6.93913 12.4152 7.07107C13.1038 7.20302 13.7206 7.57857 14.162 8.12132C14.6034 8.66407 14.8397 9.33984 14.83 10.03C14.83 12 12.5 12.5 12.5 14"/>
                    <circle cx="12" cy="17" r="1"/>
                </svg>
            </div>

            <div id="sidebar-subbox-3" class="sidebar-subbox-open">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
                    stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M9.09 9C9.32591 8.33109 9.78918 7.76807 10.4 7.41421C11.0108 7.06036 11.7266 6.93913 12.4152 7.07107C13.1038 7.20302 13.7206 7.57857 14.162 8.12132C14.6034 8.66407 14.8397 9.33984 14.83 10.03C14.83 12 12.5 12.5 12.5 14"/>
                    <circle cx="12" cy="17" r="1"/>
                </svg>
            </div>
      </div>
    </div>
    
   <script src="../prism/prism.js"></script>
   <script src="../static/script.js"></script>
</body>
</html>
''')
    html = template.substitute(ID=page_name)
    with open(file_path, 'x', encoding='utf-8') as f:
      f.write(html)

    return {'status': f'Page created {page_name}.html'}

###############################
### SAVE CONTENT EDIT/CHANGES #
###############################

@route('/save_editable', method='POST')
def save_editable():

    data = request.json

    page_name = data.get('page_name')
    div_id = data.get('id')
    new_content = data.get('data')  # This should be a string of HTML

    if not (page_name and div_id and new_content):
        return {'status': 'Missing data'}

    # Load the HTML file
    with open(f'./pages/{page_name}.html', 'r', encoding='utf-8') as f:
        soup = bs(f, 'html.parser')

    # Find the specific div by ID
    target_div = soup.find('div', id=div_id)

    if target_div:
        # Clear the old content of the div
        target_div.clear()

        # Insert parsed HTML into that div
        new_soup = bs(new_content, 'html.parser')
        for element in new_soup.contents:
            target_div.append(element)

        # Save the modified HTML
        with open(f'./pages/{page_name}.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))

        return {'status': 'Saved successfully'}
    else:
        return {'status': f'Div with ID "{div_id}" not found'}

run(host='localhost', port=8000, debug=True) 