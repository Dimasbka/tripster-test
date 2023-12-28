// custom javascript

(function() {
  console.log('Загружено');
})();

function voteAdd( publication_id, vote ) {
  console.log( 'voteDelete', publication_id, vote  );
  var tr = document.getElementById("p_"+publication_id);

  fetch('/publication/vote/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 'publication_id':publication_id, 'vote':vote }),
  })
  .then(response => response.json())
  .then(res => {
    // если ничего не поменялось ничего не делаем 
    if (res.status == 'pass') return;

    tr.querySelector(".field-rating").innerHTML = res.rating;
    tr.querySelector(".field-votes").innerHTML = res.votes;

    tr.querySelectorAll(".field-actions a").forEach((item) => item.classList.remove("checed"));
    tr.querySelector(".vote-delete").classList.add("checed");
    if(res.vote == 1){
      tr.querySelector(".vote-plus").classList.add("checed");
    }else if(res.vote == -1){
      tr.querySelector(".vote-minus").classList.add("checed");
    }
  })
  .catch(err => console.log(err));

  return false;
}

function voteDelete( publication_id ) {
  console.log( 'voteDelete', publication_id );
  var tr = document.getElementById("p_"+publication_id);

  fetch('/publication/vote/delete/', {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 'publication_id':publication_id }),
  })
  .then(response => response.json())
  .then(res => {
    // если ничего не поменялось ничего не делаем 
    tr.querySelector(".field-rating").innerHTML = res.rating;
    tr.querySelector(".field-votes").innerHTML = res.votes;

    tr.querySelectorAll(".field-actions a").forEach((item) => item.classList.remove("checed"));
  })
  .catch(err => console.log(err));
  
  return false;
}
