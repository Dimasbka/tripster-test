// custom javascript

(function() {
  console.log('Загружено',csrftoken);
})();



function infoUpdate( publication_id ) {
  console.log( 'infoUpdate', publication_id  );
  var tr = document.getElementById("p_"+publication_id);
  fetch('/publication/info/', {
//  fetch('/api/votes/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
   	  'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'publication_id':publication_id }),
  })
  .then(response => response.json())
  .then(res => {
    // если ничего не поменялось ничего не делаем 
    if (res.status == 'pass') return;

    tr.querySelector(".field-rating").innerHTML = res.rating;
    tr.querySelector(".field-votes").innerHTML = res.votes;
    tr.querySelectorAll(".field-actions a").forEach((item) => item.classList.remove("checed"));

    if(res.vote == 1){
      tr.querySelector(".vote-plus").classList.add("checed");
    }else if(res.vote == -1){
      tr.querySelector(".vote-minus").classList.add("checed");
    }

    const delete_wrap = tr.querySelector(".vote-delete-wrap");
    if(res.vote_id){
        const html = `<a onclick='voteDelete(${publication_id},${res.vote_id})' class="vote-delete checed">удалить оценку</a>`;
        delete_wrap.innerHTML = html;
    }else{
        delete_wrap.innerHTML = '';
    }


  })
  .catch(err => console.log(err));

  return false;
}


function voteAdd( publication, vote ) {
  console.log( 'voteAdd', publication, vote  );
  var tr = document.getElementById("p_"+publication);

//  fetch('/publication/vote/', {
  fetch('/api/votes/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
   	  'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'publication':publication, 'vote':vote }),
  })
  .then(response => response.json())
  .then(res => {
     // обновляю статистику
     infoUpdate( publication );
  })
  .catch(err => console.log(err));

  return false;
}

function voteDelete( publication, vote_id ) {
  console.log( 'voteDelete', publication );
  var tr = document.getElementById("p_"+publication );


//  fetch('/publication/vote/delete/', {
//    body: JSON.stringify({ '':vote_id }),
  fetch(`/api/votes/${vote_id}/`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
  })
  .then(response => {
     // обновляю статистику
     infoUpdate( publication );

  })
  .catch(err => console.log(err));
  
  return false;
}

