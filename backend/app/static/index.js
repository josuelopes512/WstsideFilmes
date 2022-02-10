function exibir(id){
    div = document.getElementById("div"+id).style.display = "block"
    document.getElementById("img"+id).style.filter = "brightness(0.5)"
}

function sumir(id){
    div = document.getElementById("div"+id).style.display = "none"
    document.getElementById("img"+id).style.filter = "none"
}