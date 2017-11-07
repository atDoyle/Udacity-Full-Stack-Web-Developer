class Movie():
    """This class creates a movie object that contains the title, storyline, poster and trailer for each object."""
    
    def __init__(self, title, storyline, poster, trailer):
        """Initiates the Movie class with the variables title, storyline, poster url and youtube url."""
        self.title = title
        self.movie_storyline = storyline
        self.poster_image_url = poster
        self.trailer_youtube_url = trailer

        