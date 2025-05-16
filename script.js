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

   /* let last_element = document.querySelector('body > div:last-of-type')
      last_element.insertAdjacentHTML('afterend', foldable_container_snippet)
   ....(probably delete...*/ 

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

/* JUST FOR TESTING bottle */

function addNewBlock() {
    const newHtml = `
        <div class="foldable-container">
            <h2>New Block</h2>
            <div class="foldable-content folded">
                New block content added!
            </div>
        </div>
    `;

    fetch('/save_page', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            page: 'test1',      // this maps to test1.html
            content: newHtml    // content to append
        })
    })
    .then(res => res.json())
    .then(data => alert(data.status))
    .catch(err => console.error('Save error:', err));
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