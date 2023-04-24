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

            const infoDiv = document.createElement("div");
            infoDiv.classList.add("book-info");

            const title = document.createElement("h3");
            bookDiv.classList.add("book-div");
            title.classList.add("book-title");

            title.textContent = book.title + " (" + book.publication_date + ")";
            infoDiv.appendChild(title);

            const author = document.createElement("p");
            author.classList.add("book-author");

            author.textContent = book.author;
            infoDiv.appendChild(author);

            const genre = document.createElement("h3");
            bookDiv.classList.add("book-div");
            genre.classList.add("book-genre");

            genre.textContent = book.genre;
            infoDiv.appendChild(genre);

            const language = document.createElement("h3");
            bookDiv.classList.add("book-div");
            language.classList.add("book-language");

            language.textContent = book.language;
            infoDiv.appendChild(language);

            const summary = document.createElement("h3");
            bookDiv.classList.add("book-div");
            summary.classList.add("book-summary");

            summary.textContent = book.summary;
            infoDiv.appendChild(summary);

            bookDiv.appendChild(infoDiv);
            booksContainer.appendChild(bookDiv);

        }
    });
