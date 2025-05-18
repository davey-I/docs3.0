/* Append new foldable content to page end  */
function append_foldable_content(){
   const ID = prompt("Enter Content Title: ")
   if (ID){
   const foldable_container_snippet = `
      <!--## ${ID} #################################################################################################################-->
      <div class="foldable-container" id="foldcontainer-${ID}" onClick="toggleFoldableContent('${ID}')">
         <h2 class="foldable-title" id="foldable-title-${ID}">${ID}</h2>

         <div class="foldable-content folded" id="foldable-content-${ID}">
             Lorem ipsum ...
         </div>
      </div>
    `;

   const title = document.querySelector('.pagetitle').textContent;

   fetch('/save_page', {
      method: 'POST',
      headers: {
         'Content-Type' : 'application/json'
      },
      body : JSON.stringify({
         page: title,
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

/* Create new page, when on Index-page */
function create_new_page(){
   var id = prompt("Enter Page Name: ")
   if (id) {
   fetch('/add_page', {
      method : 'POST',
      headers : {
         'Content-Type' : 'application/json'
      },
      body : JSON.stringify({
         page : id
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

