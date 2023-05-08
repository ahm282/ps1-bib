fetch("api_books.json")
    .then((response) => response.json())
    .then((booksData) => {
        fetch("availability.json")
            .then((response) => response.json())
            .then((availabilityData) => {
                const booksContainer = document.querySelector("#books-container");
                for (const book of booksData.books) {
                    const bookDiv = document.createElement("div");
                    bookDiv.classList.add("book-div");

                    const cover = document.createElement("img");
                    cover.classList.add("book-cover");

                    cover.src = book.cover_image;
                    cover.alt = book.title;
                    bookDiv.appendChild(cover);

                    const infoAvailabilityDiv = document.createElement("div");
                    infoAvailabilityDiv.classList.add("book-info-availability");

                    const infoDiv = document.createElement("div");
                    infoDiv.classList.add("book-info");

                    // Title
                    const title = document.createElement("h2");
                    title.classList.add("book-title");
                    title.textContent = book.title + " (" + book.publication_date + ")";
                    infoDiv.appendChild(title);

                    // Author
                    const author = document.createElement("h4");
                    author.classList.add("book-author");
                    author.textContent = book.author;
                    infoDiv.appendChild(author);

                    // Genre
                    if (book.genre !== null) {
                        const genre = document.createElement("p");
                        genre.classList.add("book-genre");
                        genre.textContent = "Genre: " + book.genre;
                        infoDiv.appendChild(genre);
                    }

                    // Language
                    const language = document.createElement("p");
                    language.classList.add("book-language");
                    language.textContent = "Taal: " + book.language;
                    infoDiv.appendChild(language);

                    // Series
                    if (book.series !== null) {
                        const series = document.createElement("p");
                        series.classList.add("book-language");
                        series.textContent = "Series: " + book.series;
                        infoDiv.appendChild(series);
                    }

                    // Summary
                    if (book.summary !== null) {
                        const summary = document.createElement("p");
                        summary.classList.add("book-summary");
                        summary.textContent = book.summary;
                        infoDiv.appendChild(summary);
                    }

                    // Availability
                    const availabilityDiv = document.createElement("div");
                    availabilityDiv.classList.add("book-availability");

                    if (availabilityData[book.title]) {
                        // get library object
                        const firstLocation = availabilityData[book.title].locations[0];
                        const locationName = Object.keys(firstLocation)[0]; // get the name of the library location
                        const locationData = firstLocation[locationName]; // get the object containing the location data

                        // get status
                        const status = document.createElement("p");
                        status.classList.add("book-status");
                        status.textContent = "Status: " + locationData.status;
                        availabilityDiv.appendChild(status);

                        // if status is !== "Aanwezig", get the due date
                        if (
                            locationData.status !== "Aanwezig" &&
                            locationData.status !== "Niet beschikbaar"
                        ) {
                            // get due date
                            const dueDate = document.createElement("p");
                            dueDate.classList.add("book-due-date");
                            dueDate.textContent = "Due date: " + locationData.due_date;
                            availabilityDiv.appendChild(dueDate);
                        }

                        // get sublocation
                        const sublocation = document.createElement("p");
                        sublocation.classList.add("book-sublocation");
                        sublocation.textContent = "Sublocation: " + locationData.sublocation;
                        availabilityDiv.appendChild(sublocation);

                        if (locationData.shelfmark !== null) {
                            // get shelfmark
                            const shelfmark = document.createElement("p");
                            shelfmark.classList.add("book-shelfmark");
                            shelfmark.textContent = "Shelfmark: " + locationData.shelfmark;
                            availabilityDiv.appendChild(shelfmark);
                        }
                    } else {
                        const notAvailable = document.createElement("p");
                        notAvailable.classList.add("book-not-available");
                        notAvailable.textContent = "Niet beschikbaar";
                        availabilityDiv.appendChild(notAvailable);
                    }

                    // create div for info and availability
                    const positioningDiv = document.createElement("div");
                    positioningDiv.classList.add("positioning-div");

                    positioningDiv.appendChild(infoDiv);
                    positioningDiv.appendChild(availabilityDiv);

                    infoAvailabilityDiv.appendChild(positioningDiv);
                    bookDiv.appendChild(infoAvailabilityDiv);
                    booksContainer.appendChild(bookDiv);
                }
            });
    });
