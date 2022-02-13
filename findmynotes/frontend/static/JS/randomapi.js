let random_quote_num = 2,quote="Genius is one percent inspiration and ninety-nine percent perspiration",quote_author="-Thomas Edison";
fetch('https://type.fit/api/quotes')
        .then(res=>res.json())
        .then(async data => {
            let random_quote_num = Math.floor(Math.random() * data.length);

            quote = await data[random_quote_num].text; 
            quote_author = "-"+data[random_quote_num].author;

            console.log(`Quote: `+quote);
            document.querySelector(".quote-text").innerHTML = "<i class='fa fa-quote-left'></i> "+ quote +" <i class='fa fa-quote-right'></i>";
            document.querySelector(".quote-author").textContent = quote_author;
        })
        .catch(err=>{ 
            // alert("err: "+err) 
            document.querySelector(".quote-text").textContent = quote_array[0].text
            document.querySelector(".quote-author").textContent = quote_array[0].author;
        });
        random_num_for_quoteArray = Math.floor(Math.random() * quote_array.length);