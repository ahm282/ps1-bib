fetch("api_books.json")
    .then((response) => response.json())
    .then((data) => {
        const booksContainer = document.querySelector("#books-container");
        for (const book of data.books) {
            const bookDiv = document.createElement("div");

            const cover = document.createElement("img");
            cover.classList.add("book-cover");

            cover.src = book.cover_image;
            cover.alt = book.title;
            bookDiv.appendChild(cover);

            // const infoDiv = document.createElement("div");
            // infoDiv.classList.add("book-info");

            const title = document.createElement("h3");
            bookDiv.classList.add("book-div");
            title.classList.add("book-title");

            title.textContent = book.title;
            // infoDiv.appendChild(title);

            const author = document.createElement("p");
            author.classList.add("book-author");

            author.textContent = book.author;
            // infoDiv.appendChild(author);

            // bookDiv.appendChild(infoDiv);
            booksContainer.appendChild(bookDiv);
        }
    });
