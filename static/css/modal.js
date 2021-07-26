// Get each modal and close button
const triggers = document.getElementsByClassName("showModal");
const triggerArray = Array.from(triggers).entries();
const modals = document.getElementsByClassName("modal");
const closeButtons = document.getElementsByClassName("close");

// Configure show/hide functions
for (let [index, trigger] of triggerArray) {
    function show(){ modals[index].style.display = "block";}
    function hide(){ modals[index].style.display = "none";}
    trigger.addEventListener("click", show);
    closeButtons[index].addEventListener("click", hide);

    // Close modal if "Escape" key is pressed
    function escapeDown(event) {
        if(event.key == 'Escape' && modals[index].style.display == "block"){
            modals[index].style.display = "none";
        }
    }
    window.addEventListener('keydown', escapeDown);
}
// Close modal if mouse is clicked outside of popup
function windowClick(event) {
    if(event.target.className == "modal"){
        event.target.style.display = "none";
    }
}
window.addEventListener('click', windowClick);