let slides = document.querySelectorAll(".slide");

let index = 0;

function showSlide(){

slides.forEach(s => s.classList.remove("active"));

slides[index].classList.add("active");

index++;

if(index >= slides.length){

index = 0;

}

}

setInterval(showSlide,4000);



document.querySelector(".next").onclick = ()=>{

index++;

if(index>=slides.length) index=0;

showSlide();

}

document.querySelector(".prev").onclick = ()=>{

index--;

if(index<0) index=slides.length-1;

showSlide();

}




// HEART TOGGLE

document.querySelectorAll(".heart").forEach(btn => {

btn.addEventListener("click",function(){

this.classList.toggle("active")

if(this.classList.contains("active")){
this.style.background="#F72585"
this.querySelector("i").style.color="white"
}
else{
this.style.background="white"
this.querySelector("i").style.color="#F72585"
}

})

})



// ADD TO CART BUTTON

document.querySelectorAll(".cart-btn").forEach(btn=>{

btn.addEventListener("click",()=>{

btn.innerText="Added ✓"

setTimeout(()=>{
btn.innerText="Add to cart"
},1500)

})

})



function toggleFilter(id){

let box = document.getElementById(id)

if(box.style.display=="block"){
box.style.display="none"
}
else{
box.style.display="block"
}

}






const features = document.querySelectorAll(".feature");

let featureIndex = 0;

function showFeature(){

features.forEach(f=>f.classList.remove("active"));

features[featureIndex].classList.add("active");

featureIndex++;

if(featureIndex >= features.length){
featureIndex = 0;
}

}

setInterval(showFeature,2000);







const reviews = document.querySelectorAll(".review");

let rIndex = 0;

function showReview(){

reviews.forEach(r => r.classList.remove("active"));

reviews[rIndex].classList.add("active");

}

document.querySelector(".review-next").onclick = () => {

rIndex++;

if(rIndex >= reviews.length){
rIndex = 0;
}

showReview();

}

document.querySelector(".review-prev").onclick = () => {

rIndex--;

if(rIndex < 0){
rIndex = reviews.length-1;
}

showReview();

}

/* auto slider */

setInterval(()=>{

rIndex++;

if(rIndex >= reviews.length){
rIndex = 0;
}

showReview();

},4000);




function toggleFilter(el){

let section = el.parentElement;

section.classList.toggle("active");

}



function toggleSort(){

let menu = document.getElementById("sortMenu");

if(menu.style.display === "block"){
menu.style.display = "none";
}
else{
menu.style.display = "block";
}

}



function toggleDropdown(event){

event.preventDefault();

let menu = document.getElementById("shopDropdown");

menu.classList.toggle("show");

}









