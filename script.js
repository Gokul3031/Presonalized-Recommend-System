// function fetchSuggestions(input) {
//     if (input.length < 3) return;  // Trigger autocomplete for 3 or more characters
//     fetch(`http://localhost:8000/autocomplete/${input}`)
//         .then(response => response.json())
//         .then(data => {
//             const list = document.getElementById('suggestions-list');
//             list.innerHTML = '';
//             data.forEach(item => {
//                 const li = document.createElement('li');
//                 li.innerText = item;
//                 li.onclick = function() {
//                     document.getElementById('book-name').value = item;
//                     list.innerHTML = '';
//                 };
//                 list.appendChild(li);
//             });
//         });
// }

// function getRecommendations() {
//     const bookName = document.getElementById('book-name').value;
//     if (!bookName) {
//         alert('Please enter a book name!');
//         return;
//     }

//     fetch('http://localhost:8000/recommend/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ book_name: bookName })
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return response.json();
//     })
//     .then(data => {
//         const resultsDiv = document.getElementById('recommendation-results');
//         resultsDiv.innerHTML = `<h2>Recommendations:</h2>`;
//         data.recommendations.forEach(book => {
//             const div = document.createElement('div');
//             div.innerHTML = `<h3>${book.title}</h3><p>Author: ${book.author}</p><p>Year: ${book.year}</p><p>Rating: ${book.rating}</p><img src="${book.img_url}" alt="Cover Image" style="width:100px;">`;
//             resultsDiv.appendChild(div);
//         });
//     })
//     .catch(error => {
//         console.error('Error fetching recommendations:', error);
//     });
// }

// Function to fetch autocomplete suggestions
// function fetchSuggestions(input) {
//     if (input.length < 3) return;  // Trigger autocomplete for 3 or more characters

//     fetch(`http://localhost:8000/autocomplete/${input}`)
//         .then(response => response.json())
//         .then(data => {
//             const list = document.getElementById('suggestions-list');
//             list.innerHTML = '';  // Clear previous suggestions
//             data.forEach(item => {
//                 const li = document.createElement('li');
//                 li.innerText = item;

//                 // When a suggestion is clicked, update the input field and clear suggestions
//                 li.onclick = function() {
//                     document.getElementById('book-input').value = item;
//                     list.innerHTML = '';  // Clear suggestions after selection
//                 };  

//                 list.appendChild(li);
//             });
//         });
// }

// Function to fetch autocomplete suggestions
function fetchSuggestions(input) {
    const list = document.getElementById('suggestions-list');

    // Clear suggestions if the input is empty or has less than 3 characters
    if (input.trim().length < 3) {
        list.innerHTML = '';
        return;  // No need to fetch suggestions
    }

    fetch(`http://127.0.0.1:8023/autocomplete/${input}`)
        .then(response => response.json())
        .then(data => {
            list.innerHTML = '';  // Clear previous suggestions
            data.forEach(item => {
                const li = document.createElement('li');
                li.innerText = item;

                // When a suggestion is clicked, update the input field and clear suggestions
                li.onclick = function() {
                    document.getElementById('book-input').value = item;
                    list.innerHTML = '';  // Clear suggestions after selection
                };

                list.appendChild(li);
            });
        });
}


// Function to fetch book recommendations based on the selected book name
function getRecommendations() {
    const bookName = document.getElementById('book-input').value;  // Single input field
    if (!bookName) {
        alert('Please enter a book name!');
        return;
    }

    fetch('http://127.0.0.1:8023/recommend/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ book_name: bookName })  // Sending book name for recommendation
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const resultsDiv = document.getElementById('recommendation-results');
        resultsDiv.innerHTML = `<h2>Recommended Books:</h2>`;
        data.recommendations.forEach(book => {
            const div = document.createElement('div');
            div.innerHTML = `<h3>${book.title}</h3><p>Author: ${book.author}</p><p>Year: ${book.year}</p><p>Rating: ${book.rating}</p><img src="${book.img_url}" alt="Cover Image" style="width:100px;">`;
            resultsDiv.appendChild(div);
        });
    })
    .catch(error => {
        console.error('Error fetching recommendations:', error);
    });
}


