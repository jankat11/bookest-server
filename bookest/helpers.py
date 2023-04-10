def get_book_credentials(data):
    google_id = data["googleId"]
    isbn = data["isbn"]
    title = data["title"]
    no_cover = data["noCover"]
    will_be_read = data["willBeRead"]
    has_been_read = data["hasBeenRead"]
    shelf = "will_be_read" if will_be_read else "has_been_read"
    other_shelf = "will_be_read" if has_been_read else "has_been_read"
    return {
        "id":google_id,
        "isbn":isbn, 
        "title":title, 
        "cover":no_cover, 
        "shelf":shelf, 
        "other_shelf": other_shelf
    }


def get_review_credentials(data):
    google_id = data["googleId"]
    isbn = data["isbn"]
    title = data["title"]
    no_cover = data["noCover"]
    content = data["content"]
    return {
        "id":google_id,
        "isbn":isbn, 
        "title":title, 
        "cover":no_cover, 
        "content": content
    }


def get_book_on_notes(data):
    google_id = data["googleId"]
    isbn = data["isbn"]
    title = data["title"]
    no_cover = data["noCover"]
    return {
        "id":google_id,
        "isbn":isbn, 
        "title":title, 
        "cover":no_cover, 
    }