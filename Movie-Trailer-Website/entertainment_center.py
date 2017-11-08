import media
import fresh_tomatoes

shaun_of_the_dead = media.Movie(
    "Shaun of the Dead",
    """A man decides to turn his moribund life around by winning back his
    ex-girlfriend, reconciling his relationship with his mother, and
    dealing with an entire community
     that has returned from the dead to eat the living.""",
    "https://i.imgur.com/Y8mgOWQ.jpg",
    "https://www.youtube.com/watch?v=mqQ8Y9Sjp7o")
hot_fuzz = media.Movie(
    "Hot Fuzz",
    """A skilled London police officer is transferred to a small town
     that's harbouring a dark secret.""",
    "https://i.imgur.com/ELy33VZ.jpg",
    "https://www.youtube.com/watch?v=fuEG_PSb_Ts")
the_worlds_end = media.Movie(
    "The World's End",
    """Five friends who reunite in an attempt to top their
     epic pub crawl from twenty years earlier unwittingly
      become humanity's only hope for survival.""",
    "https://i.imgur.com/9BsRA4S.jpg",
    "https://www.youtube.com/watch?v=tYs7uguB_JQ")

movies = [
    shaun_of_the_dead,
    hot_fuzz,
    the_worlds_end
    ]

fresh_tomatoes.open_movies_page(movies)
