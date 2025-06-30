
/* Fetch editable content */
async function fetchEditableContent(pageName, divId, penid) {
  const page_folder = document.querySelector('.pagetitle').getAttribute('data-folder-path');
  const response = await fetch('/get_editable', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: divId,
      page_folder: page_folder,
      page_name: pageName
    })
  });

  if (!response.ok) {
    const error = await response.json();
    console.error("Error fetching content:", error.error);
    return;
  }

  const data = await response.json();
  const editableDiv = document.getElementById(divId);
  const penbutton = document.getElementById(penid);

  editableDiv.setAttribute('contenteditable', true)
  penbutton.classList.replace('foldable-content-penButton-hidden', 'foldable-content-penButton')
  
  editableDiv.innerText = data.html;  // Shows raw HTML code for editing
  document.getElementById(divId)
}

/* Save edited content */
function save_editable_content(PAGE_ID, ID) {
   document.getElementById(ID).setAttribute('contenteditable', false)
   var content = document.getElementById(ID);
   const page_folder = document.querySelector('.pagetitle').getAttribute('data-folder-path');

   if (!content) {
      console.error('No element found with ID:', ID);
      return;
   }

   fetch('/save_editable', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         page_name: PAGE_ID,
         page_folder: page_folder,
         id: ID,
         data: content.innerText
      })
   })
   .then(res => res.json())
   .then(data => alert(data.status))
   .catch(err => console.error('Save editable-content error:', err));
}

/* Append new foldable content to page end */
function append_foldable_content(){
   const ID = prompt("Enter Content Title: ")
   let PAGE_NAME = document.getElementsByClassName('pagetitle')[0].textContent;
   if (ID){
   const foldable_container_snippet = `
      <!--## ${ID} #################################################################################################################-->
      <div class="foldable-container" id="foldcontainer-${ID}">
         <h2 class="foldable-title" id="foldable-title-${ID}">${ID}</h2>
         <button class="foldable-content-unfoldbutton" id="foldable-content-unfoldbutton-newchapter" onclick="toggleFoldableContent('${ID}')" type="button">
          UNFOLD
         </button>
         <button class="foldable-content-edittoggle" onclick="fetchEditableContent('${PAGE_NAME}','editable-paragraph-${ID}', 'foldable-content-penButton-${ID}')" type="button">EDITMODE</button>
         <button class="create-subdiv" id="create-subdiv-${ID}" onclick="add_subdiv('editable-paragraph-${ID}')" type=*button"> ADD DIV </button>
         <div class="foldable-content folded" id="foldable-content-${ID}">
           <button type='button' class='foldable-content-penButton-hidden' onclick="save_editable_content('${PAGE_NAME}','editable-paragraph-${ID}', 'page-folder')" id='foldable-content-penButton-${ID}'>
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 20h9" />
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z" />
             </svg>
            </button>
            <div contenteditable="false" class="editable-paragraph" id="editable-paragraph-${ID}"><h1>TITLE IPSUM</h2></div>
         </div>
      </div>
    `;

   const title = document.querySelector('.pagetitle').textContent;
   const page_folder = document.querySelector('.pagetitle').getAttribute('data-folder-path');

   fetch('/save_page', {
      method: 'POST',
      headers: {
         'Content-Type' : 'application/json'
      },
      body : JSON.stringify({
         page: title,
         page_folder: page_folder,
         content: foldable_container_snippet
      })
   })
   .then(res => res.json())
   .then(data => alert(data.status))
   .catch(err => console.error('Save data error: ', err));
   /* --> add page refresher here */
}
else {
   console.log("You did not enter a Title !")
}
}

/* Append new foldable subdiv */
function add_subdiv(parentID){
   const ID = prompt("Enter Content Title: ")
   let PAGE_NAME = document.getElementsByClassName('pagetitle')[0].textContent;
   if (ID){
   const foldable_container_snippet = `
      <!--## ${ID} #################################################################################################################-->
      <div class="foldable-container" id="foldcontainer-${ID}">
         <h2 class="foldable-title" id="foldable-title-${ID}">${ID}</h2>
         <button class="foldable-content-unfoldbutton" id="foldable-content-unfoldbutton-newchapter" onclick="toggleFoldableContent('${ID}')" type="button">
          UNFOLD
         </button>
         <button class="foldable-content-edittoggle" onclick="fetchEditableContent('${PAGE_NAME}','editable-paragraph-${ID}', 'foldable-content-penButton-${ID}')" type="button">EDITMODE</button>
         <div class="foldable-content folded" id="foldable-content-${ID}">
           <button type='button' class='foldable-content-penButton-hidden' onclick="save_editable_content('${PAGE_NAME}','editable-paragraph-${ID}', 'page-folder')" id='foldable-content-penButton-${ID}'>
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 20h9" />
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z" />
             </svg>
            </button>
            <div contenteditable="false" class="editable-paragraph" id="editable-paragraph-${ID}"><h1>TITLE IPSUM</h2></div>
         </div>
      </div>
    `;

   const title = document.querySelector('.pagetitle').textContent;
   const page_folder = document.querySelector('.pagetitle').getAttribute('data-folder-path');

   fetch('/add_subdiv', {
      method: 'POST',
      headers: {
         'Content-Type' : 'application/json'
      },
      body : JSON.stringify({
         page: title,
         page_folder: page_folder,
         content: foldable_container_snippet,
         parentID: parentID
      })
   })
   .then(res => res.json())
   .then(data => alert(data.status))
   .catch(err => console.error('Save data error: ', err));
   /* --> add page refresher here */
}
else {
   console.log("You did not enter a Title !")
}
}

/* Create new page, when on Index-page */
function create_new_page(){
   var id = prompt("Enter Page Name: ")
   var folder = prompt("Enter folder Name: ")
   if (id && folder) {
   fetch('/add_page', {
      method : 'POST',
      headers : {
         'Content-Type' : 'application/json'
      },
      body : JSON.stringify({
         page : id,
         folder : folder
      })
   })
   .then(res => res.json())
   .then(data => alert(data.status))
   .catch(err => console.error('Create page error: ', err));
 }
 else {
   console.log("You did not enter a name !") 
 }
}

/* Function to fold/unfold the foldable containers */
function toggleFoldableContent(ID){

   content_classname = "foldable-content-"
   conc_string_content = content_classname.concat(ID)

   let foldContent = document.getElementById(conc_string_content)

   if (foldContent.classList.contains('folded')) {
    foldContent.classList.replace('folded', 'unfolded')
   } else {
    foldContent.classList.replace('unfolded', 'folded')
   }

   let childDiv = foldContent.childNodes

   childDiv.forEach(cDiv => {
      if (cDiv.classList.contains('folded')) {
    cDiv.classList.replace('folded', 'unfolded')
   } else {
    cDiv.classList.replace('unfolded', 'folded')
   }
   });
}

/* Function for the button in the sidebar enclosure to open/close the sidebar */
function toggle_sidebar() {
  const sidebar_container = document.querySelector('.sidebar-mainbox-open') || document.querySelector('.sidebar-mainbox-closed');
  const sidebar_buttons = document.querySelectorAll('.sidebar-subbox-open, .sidebar-subbox-close');

  if (!sidebar_container) return; // Safety check

  // Toggle main sidebar class
  if (sidebar_container.classList.contains('sidebar-mainbox-open')) {
    sidebar_container.classList.replace('sidebar-mainbox-open', 'sidebar-mainbox-closed');
  } else {
    sidebar_container.classList.replace('sidebar-mainbox-closed', 'sidebar-mainbox-open');
  }

  // Toggle button classes
  sidebar_buttons.forEach(button => {
    if (button.classList.contains('sidebar-subbox-open')) {
      button.classList.replace('sidebar-subbox-open', 'sidebar-subbox-close');
    } else {
      button.classList.replace('sidebar-subbox-close', 'sidebar-subbox-open');
    }
  });
}

/* Toggle page overview window visibility */

function page_overview_visibility_toggle(){
   el = document.getElementById('page-overwiew-index')
   if (el.classList.contains('page-overwiew-hidden')){
      el.classList.replace('page-overwiew-hidden', 'page-overwiew')
   }
   else {
      el.classList.replace('page-overwiew', 'page-overwiew-hidden')
   }
}

/* Create new page-folder */
function create_new_pagefolder(){
   var foldername = prompt("Enter Foldername: ")
   var path1 = "./pages/"
   var path2 = path1.concat(foldername)
   
   if(foldername){
     fetch('/create_folder', {
      method : 'POST',
      headers : {
         'Content-Type' : 'application/json'
      },
      body : JSON.stringify({
         folderpath : path2,
         folderName : foldername
      })
   })
   .then(res => res.json())
   .then(data => alert(data.status))
   .catch(err => console.error('Create folder error: ', err));
   }
   else{
    console.error("You did not enter a foldername !")
   }
}

/* Load pages in folder-index page overview list */
async function load_pages_to_folderindex_overview(folderName, divid) {
  const page_folder = folderName;
  const div_id = divid;
  const response = await fetch('/load_indexpages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      page_folder: page_folder
    })
  });

  if (!response.ok) {
    const error = await response.json();
    console.error("Error fetching content:", error.error);
    return;
  }

  const data = await response.json();
  const page_list_div = document.getElementById(div_id);
  
  page_list_div.outerHTML = data.html;
}

/* Search Function */

async function search_content(){
   const search_string = prompt("Enter Searchterm : ");
   
   const response = await fetch('/search_content', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({
      search_string: search_string
   })
});

if (!response.ok) {
   const error = await response.json();
   console.error("Error fetching content:", error.error);
   return;
 }
 const data = await response.json();
 console.log("Text from backend : ", data.message)
}
