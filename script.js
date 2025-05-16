/* Insert new foldable content */
function append_foldable_content(ID){
   const foldable_container_snippet = `
      <!--## skdfjlk #################################################################################################################-->
      <div class="foldable-container" id="foldcontainer-${ID}" onClick="toggleFoldableContent('${ID}')">
         <h2 class="foldable-title" id="foldable-title-${ID}">${ID}</h2>

         <div class="foldable-content folded" id="foldable-content-${ID}">
             Lorem ipsum ...
         </div>
      </div>
    `;

   fetch('/save_page', {
      method: 'POST',
      headers: {
         'Content-Type' : 'application/json'
      },
      body : JSON.stringify({
         page: 'test1',
         content: foldable_container_snippet
      })
   })
   .then(res => res.json())
   .then(data => alert(data.status))
   .catch(err => console.error('Save data error: ', err));
   /* --> add page refresher here */
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