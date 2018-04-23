from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Team, Base, Player

engine = create_engine('sqlite:///mlb_cards.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create user Catalog
User1 = User(name="Catalog", email="catalog@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')  # noqa
session.add(User1)
session.commit()


# Players for Boston Red Sox
team1 = Team(user_id=1,
             name="Boston Red Sox")

session.add(team1)
session.commit()


player1 = Player(user_id=1,
                 name="Mookie Betts",
                 price="$50.00",
                 image="mookie.png",
                 team=team1)
session.add(player1)
session.commit()

player2 = Player(user_id=1,
                 name="Andrew Benintendi",
                 price="$15.00",
                 image="benintendi.png",
                 team=team1)

session.add(player2)
session.commit()

player3 = Player(user_id=1,
                 name="David Price",
                 price="$20.00",
                 image="price.png",
                 team=team1)

session.add(player3)
session.commit()

player4 = Player(user_id=1,
                 name="Dustin Pedroia",
                 price="$15.00",
                 image="pedroia.png",
                 team=team1)

session.add(player4)
session.commit()

player5 = Player(user_id=1,
                 name="Jackie Bradley Jr.",
                 price="$10.00",
                 image="jbj.png",
                 team=team1)

session.add(player5)
session.commit()

player6 = Player(user_id=1,
                 name="Xander Bogaerts",
                 price="$20.00",
                 image="Bogaerts.png",
                 team=team1)

session.add(player6)
session.commit()

# Players for New York Yankees
team2 = Team(user_id=1,
             name="New York Yankees")

session.add(team2)
session.commit()

player1 = Player(user_id=1,
                 name="Aaron Judge",
                 price="$1.50",
                 image="judge.png",
                 team=team2)

session.add(player1)
session.commit()

player2 = Player(user_id=1,
                 name="Luis Severino",
                 price="$3.00",
                 image="severino.png",
                 team=team2)

session.add(player2)
session.commit()

player3 = Player(user_id=1,
                 name="Aroldis Chapman",
                 price="$1.00",
                 image="chapman.png",
                 team=team2)

session.add(player3)
session.commit()

player4 = Player(user_id=1,
                 name="Gary Sanchez",
                 price="$2.00",
                 image="sanchez.png",
                 team=team2)

session.add(player4)
session.commit()

player5 = Player(user_id=1,
                 name="Didi Gregorious",
                 price="$10.00",
                 image="didi.png",
                 team=team2)

session.add(player5)
session.commit()


# Players for Toronto Blue Jays
team3 = Team(user_id=1,
             name="Toronto Blue Jays")

session.add(team3)
session.commit()

player1 = Player(user_id=1,
                 name="Marcus Stroman",
                 price="$5.00",
                 image="stroman.png",
                 team=team3)

session.add(player1)
session.commit()

player2 = Player(user_id=1,
                 name="Josh Donaldson",
                 price="$3.00",
                 image="donaldson.png",
                 team=team3)

session.add(player2)
session.commit()

player3 = Player(user_id=1,
                 name="Kevin Pillar",
                 price="$2.00",
                 image="pillar.png",
                 team=team3)

session.add(player3)
session.commit()

player4 = Player(user_id=1,
                 name="Jose Bautista",
                 price="$10.00",
                 image="bautista.png",
                 team=team3)

session.add(player4)
session.commit()

player5 = Player(user_id=1,
                 name="Kendrys Morales",
                 price="$10.00",
                 image="morales.png",
                 team=team3)

session.add(player5)
session.commit()


# Players for Baltimore Orioles
team4 = Team(user_id=1,
             name="Baltimore Orioles")

session.add(team4)
session.commit()

player1 = Player(user_id=1,
                 name="Manny Machado",
                 price="$25.00",
                 image="machado.png",
                 team=team4)

session.add(player1)
session.commit()

player2 = Player(user_id=1,
                 name="Dylan Bundy",
                 price="$3.00",
                 image="bundy.png",
                 team=team4)

session.add(player2)
session.commit()

player3 = Player(user_id=1,
                 name="Jonathan Schoop",
                 price="$2.00",
                 image="schoop.png",
                 team=team4)

session.add(player3)
session.commit()

player4 = Player(user_id=1,
                 name="Chris Davis",
                 price="$10.00",
                 image="davis.png",
                 team=team4)

session.add(player4)
session.commit()

player5 = Player(user_id=1,
                 name="Adam Jones",
                 price="$10.00",
                 image="jones.png",
                 team=team4)

session.add(player5)
session.commit()


# Players for Tampa Bay Rays
team5 = Team(user_id=1,
             name="Tampa Bay Rays")

session.add(team5)
session.commit()

player1 = Player(user_id=1,
                 name="Chris Archer",
                 price="$25.00",
                 image="archer.png",
                 team=team5)

session.add(player1)
session.commit()

player2 = Player(user_id=1,
                 name="Evan Longoria",
                 price="$23.00",
                 image="longoria.png",
                 team=team5)

session.add(player2)
session.commit()

player3 = Player(user_id=1,
                 name="Kevin Kiermaier",
                 price="$2.00",
                 image="kiermaier.png",
                 team=team5)

session.add(player3)
session.commit()

player4 = Player(user_id=1,
                 name="Logan Morrison",
                 price="$10.00",
                 image="morrison.png",
                 team=team5)

session.add(player4)
session.commit()

print "added players!"
