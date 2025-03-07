let profile = document.getElementById("user")
let isOpen = false;

profile.addEventListener("click", () => {
    if(isOpen){
        document.getElementById("pop").style.display = "none";
        isOpen = false;
    }else{
        document.getElementById("pop").style.display = "block";
        isOpen = true;
    }
})