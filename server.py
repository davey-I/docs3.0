from bottle import route, run, template, static_file, response, request
from string import Template
import os
from bs4 import BeautifulSoup as bs


PAGES_DIR = './pages'

@route('/')
def index():
    return static_file('index.html', root='./')

@route('/static/<filename>')
def servers_static(filename):
    return static_file(filename, root='./')

@route('/prism/<filename>')
def serve_prism(filename):
    return static_file(filename, root='./prism')

@route('/pages/<foldername>/<pagename>')
def serve_page(foldername, pagename):
    return static_file(pagename, root=f'./pages/{foldername}')

#################################
### ADD NEW CHAPTER TO NOTEPAGE #
#################################

@route('/save_page', method='POST')
def save_page():
    data = request.json
    page_name = data.get('page')
    page_folder = data.get('page_folder')
    new_content = data.get('content')
    
    if not page_name or not new_content:
        response.status = 400
        return {'status': 'Missing data'}
    file_path_folder = os.path.join(PAGES_DIR, page_folder)
    file_path = os.path.join(file_path_folder, f'{page_name}.html')

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

#####################
### ADD NEW SUB-DIV #
#####################

@route('/add_subdiv', method='POST')
def save_page():
    data = request.json
    page_name = data.get('page')
    page_folder = data.get('page_folder')
    new_content = data.get('content')
    parentID = data.get('parentID')
    
    if not page_name or not new_content:
        response.status = 400
        return {'status': 'Missing data'}
    file_path_folder = os.path.join(PAGES_DIR, page_folder)
    file_path = os.path.join(file_path_folder, f'{page_name}.html')

    if not os.path.exists(file_path):
        response.status = 404
        return {'status': 'Page not found'}

    # Parse existing HTML file
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = bs(f, 'html.parser')

    # Parse new content and append to <body>
    parentdiv = soup.find("div", id=parentID)
    parentdiv.append(bs(new_content, 'html.parser'))

    # Write back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return {'status': f'Content added to <div>'}


##############################
### ADD NEW PAGE TO NOTEBOOK #
##############################

@route('/add_page', method='POST')
def add_page():
    data = request.json
    page_name = data.get('page')
    folder_name = data.get('folder')
    if not os.path.exists(f'./pages/{folder_name}'):
        return {'status': 'Folder not found !'}
    
    folder_name_path = os.path.join(PAGES_DIR, folder_name)
    file_path = os.path.join(folder_name_path, f'{page_name}.html')
    template = Template('''<!DOCTYPE html>
<html>
<head>
    <title data-folder-path="/$FOLDER_NAME">$ID</title>
    <link rel="stylesheet" href=" ../../static/style.css">
    <link rel="stylesheet" href="../../prism/prism.css">
</head>
<body class="body">
    <div class="page-folder-header-div">
            <h1 class="pagetitle" data-folder-path="$FOLDER_NAME">$ID</h1>
            <a href="./../..">
                 <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
                         stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 11L12 4L21 11" />
                        <path d="M5 10V20H19V10" />
                        <path d="M10 20V14H14V20" />
                 </svg>
            </a>
    </div>

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
    
   <script src="../../prism/prism.js"></script>
   <script src="../../static/script.js"></script>
</body>
</html>
''')
    html = template.substitute(ID=page_name, FOLDER_NAME=folder_name)
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
    folder_name = data.get('page_folder')
    div_id = data.get('id')
    new_content = data.get('data')  # This should be a string of HTML
    new_soup = bs(new_content, 'html.parser')

    if not (page_name and div_id and new_content):
        return {'status': 'Missing data'}

    # Load the HTML file
    with open(f'./pages/{folder_name}/{page_name}.html', 'r', encoding='utf-8') as f:
        soup = bs(f, 'html.parser')

    target_div = soup.find('div', id=div_id)
    target_div.clear()

    #for el in new_soup:
    target_div.append(bs(data['data'], 'html.parser'))
    

    with open(f'./pages/{folder_name}/{page_name}.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return {'status': 'Saved successfully'}
    

###########################
### GET CURRENT HTML CODE #
###########################

@route('/get_editable', method="POST")
def get_editable():
    data = request.json
    page_name = data.get('page_name')
    page_folder = data.get('page_folder')
    path_with_folder = os.path.join(PAGES_DIR, page_folder)
    div_id = data.get('id')

    file_path = os.path.join(path_with_folder, f'{page_name}.html')
    if not os.path.exists(file_path):
        response.status = 404
        return {'error': 'Page not found'}

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = bs(f, 'html.parser')

    target_div = soup.find('div', id=div_id)
    if not target_div:
        response.status = 404
        return {'error': 'Div not found'}

    # Return only the contents (not the <div> wrapper)
    return {'html': target_div.decode_contents()}
    
#######################
### CREATE NEW FOLDER #
#######################

@route('/create_folder', method="POST")
def create_folder():
    data = request.json
    filepath = data.get('folderpath')
    foldername = data.get('folderName')
    if not os.path.exists(f'./pages/{foldername}'):
        # Create the directory
        try:
            os.mkdir(filepath)
            with open('./index.html', 'r', encoding='utf-8') as f:
                soup = bs(f, 'html.parser')
            li_new = soup.new_tag("li")
            li_new['class'] = 'page-overwiew-listIL'
            li_new['id'] = f'page-overwiew-listIL-{foldername}'
            a_new = soup.new_tag("a")
            a_new['class'] = 'page-overwiew-lista-tag'
            a_new['id'] = f'page-overwiew-lista-tag-{foldername}'
            a_new['href'] = f'./pages/{foldername}/{foldername}-index.html'
            a_new.append(f'{foldername}')
            li_new.append(a_new)
            #li_new.append(f"{foldername}")

            li_element_list = soup.find_all('li')
            li_element_list_len = len(li_element_list)
            li_element_list[li_element_list_len-1].append(li_new)

            with open('./index.html', 'w', encoding='utf-8') as f:
                f.write(str(soup))

            with open(f'./pages/{foldername}/{foldername}-index.html', 'w', encoding='utf-8') as f:
                html_content = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{foldername} Index</title>
                <link href=" /static/style.css" rel="stylesheet"/>
            </head>
            <body>
             <div class="page-folder-header-div">
                <h1>{foldername}</h1>
                <a href="./../..">
                 <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
                         stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 11L12 4L21 11" />
                        <path d="M5 10V20H19V10" />
                        <path d="M10 20V14H14V20" />
                 </svg>
                </a>
             </div><br><br><br>
                <div class="page-folder-page-div" id="page-folder-page-div-{foldername}">
                    
                </div>
            <script src="/static/script.js"></script>
            <script>
                let folderName = '{foldername}'
                let div_id = 'page-folder-page-div-{foldername}'
                document.addEventListener('DOMContentLoaded', function() {{
                 load_pages_to_folderindex_overview(folderName, div_id);
                }});
            </script>
            </body>
            </html>"""
                f.write(html_content)
            
            return {'status': f'Directory Created successfully'}
        except FileExistsError:
            return{'status' : 'Directory could not be created'}
    else:
        return{'status' : 'Directory already exists'}


#############################################
### LOADE PAGES TO FOLDER OVERVIEW AS LINKS #
#############################################

@route('/load_indexpages', method="POST")
def load_indexpages():
    data = request.json
    page_folder = data.get('page_folder')
    path_with_folder = os.path.join(PAGES_DIR, page_folder)

    if not os.path.exists(path_with_folder):
        response.status = 404
        return {'error': 'Folder not found'}

    # Hier nun die Titel der in diesem Ordner vorhandenen pages holen und 
    # und hier damit einen neuen <div> content erstellen, sodass dieser 
    # auf client-side einfach nur noch ersetzt werden kann...
    page_names = []
    with os.scandir(path_with_folder) as listOfEntries:
        for ent in listOfEntries:
            if ent.is_file():
                page_names.append(ent.name)

    with open(f'{path_with_folder}/{page_folder}-index.html', 'r', encoding='utf-8') as f:
        soup = bs(f, 'html.parser')

    div_id = f'page-folder-page-div-{page_folder}'
    target_div = soup.find('div', id=div_id)
    if not target_div:
        response.status = 404
        return {'error': 'Div not found'}
    
    for el in page_names:
        a_new = soup.new_tag("a")
        a_new['class'] = 'page-overwiew-lista-tag'
        a_new['id'] = f'page-overwiew-lista-tag-{el}'
        a_new['href'] = f'{el}'
        a_new.append(el)
        target_div.append(a_new)

    # Return only the contents (not the <div> wrapper)
    return {'html': target_div.decode_contents()}

run(host='localhost', port=8000, debug=True) 
