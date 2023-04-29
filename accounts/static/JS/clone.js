// Make sub-menu below corresponding nav element
let navAbout = document.querySelector('.sub-nav.about')
let navSell = document.querySelector('.sub-nav.sell')
let navContact = document.querySelector('.sub-nav.contact')
let subAbout = document.querySelector('.sub-about')
let subSell = document.querySelector('.sub-sell')
let subContact = document.querySelector('.sub-contact')
// preload
subAbout.style.left=navAbout.offsetLeft.toString()+'px';
subAbout.style.top=(navAbout.offsetHeight+navAbout.offsetTop).toString()+'px';
subSell.style.left=navSell.offsetLeft.toString()+'px';
subSell.style.top=(navSell.offsetHeight+navSell.offsetTop).toString()+'px';
subContact.style.left=navContact.offsetLeft.toString()+'px';
subContact.style.top=(navContact.offsetHeight+navContact.offsetTop).toString()+'px';
let resizeSubMenu = function() {
    subAbout.style.left=navAbout.offsetLeft.toString()+'px';
    subAbout.style.top=(navAbout.offsetHeight+navAbout.offsetTop).toString()+'px';
    subSell.style.left=navSell.offsetLeft.toString()+'px';
    subSell.style.top=(navSell.offsetHeight+navSell.offsetTop).toString()+'px';
    subContact.style.left=navContact.offsetLeft.toString()+'px';
    subContact.style.top=(navContact.offsetHeight+navContact.offsetTop).toString()+'px';
}
window.addEventListener('resize',resizeSubMenu);

