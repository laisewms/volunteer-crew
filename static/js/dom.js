

document.querySelector('.submit-post').addEventListener('submit', evt => {
    evt.preventDefault();

    const postFormInputs = {
      title: document.querySelector('#post-title').value,
      content: document.querySelector('#post-content').value,
      // opp_photo: document.querySelector('#post-photo').value,
      opp_photo: document.querySelector('#post-photo').files[0].name

    };

    console.log(postFormInputs)



    fetch('/new_post',{
        method: 'POST',
        body:JSON.stringify(postFormInputs),
        headers: {
          'Content-Type': 'application/json',
        },
      })
  //      .then(response => response.json())
  //      .then(responseJson => {    
   
  //  });


})

// document.querySelector('#order-form').addEventListener('submit', evt => {
//     evt.preventDefault();
  
//     const formInputs = {
//       type: document.querySelector('#type-field').value,
//       amount: document.querySelector('#amount-field').value,
//     };
  
//     fetch('/new-order', {
//       method: 'POST',
//       body: JSON.stringify(formInputs),
//       headers: {
//         'Content-Type': 'application/json',
//       },
//     })
//       .then(response => response.json())
//       .then(responseJson => {
//         alert(responseJson.status);
//       });
//   });