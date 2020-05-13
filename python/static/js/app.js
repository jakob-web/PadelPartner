const goBack = function() {
    window.history.back();
  }
document.getElementById("backBtn").onclick = function (){
  goBack();
  }

  if (document.body.classList.contains("myGames")) {
  
    len = document.querySelectorAll(".matchlink").length
  
    for (i=0; i<len; i++) {
      // Gets every amount of sökes
      sökes = document.querySelectorAll(".matchlink")[i].querySelectorAll(".sökes")[0].innerHTML
      if(sökes == "None") {sökes = 4}
      
      document.querySelectorAll(".matchlink")[i].querySelectorAll(".antal_spelare")[0].innerHTML = 4-sökes +"/4"
      
      if (sökes == 0 || sökes < 0) {
        document.querySelectorAll(".matchlink")[i].querySelectorAll(".match_status")[0].children[0].src= '/static/img/check.png';
      }
    }  
    }
  

players = document.querySelectorAll(".players");
// Fetches the amount of spots that are already booked
sökes = document.querySelectorAll("#sökes")[0].innerHTML;
bookedSaved = 4-sökes;

const change = function() {
  // select all red "booked" profiles
  booked = document.querySelectorAll(".booked");
  // hidden form for amount of booked players
  antal = document.querySelectorAll("#antal");
  // change the value for antal to same amount of red "booked" profiles
  antal[0].value = document.querySelectorAll(".booked").length;


  if (this.classList.contains("bookedSaved")) {
    console.log("already booked");
  }
  else if (this.classList.contains("booked")) {
    this.src = '/static/img/user (1).png';
    this.classList.remove("booked");
    antal[0].value = document.querySelectorAll(".booked").length;
  }
  else {
    this.src = '/static/img/user (2).png';
    this.classList.add("booked");
    antal[0].value = document.querySelectorAll(".booked").length;
  }
}

if (document.body.classList.contains("bookContainer")) {
  for (i=0; i<4; i++) {
    players[i].onclick = change
  }
}

for (i=0; i<bookedSaved; i++) {
  players[i].classList.add("bookedSaved")
  players[i].src = '/static/img/user (2).png';
}


if (document.body.classList.contains("matchOverview")) {
  
  len = document.querySelectorAll(".matchlink").length

  for (i=0; i<len; i++) {
    // Gets every amount of sökes
    sökes = document.querySelectorAll(".matchlink")[i].children[3].innerHTML
    bookedSaved = 4-sökes;
    players = document.querySelectorAll(".matchlink")[i].querySelectorAll(".players");
    console.log(sökes)
    for (x=0; x<bookedSaved; x++) {
      // Få fram specifik list element
      players[x].classList.add("bookedSaved")
      players[x].src = '/static/img/user (2).png';
  }
  }
}

