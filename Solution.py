from typing import List, Tuple
from psycopg2 import sql

import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException

from Business.Movie import Movie
from Business.Studio import Studio
from Business.Critic import Critic
from Business.Actor import Actor


# ---------------------------------- CRUD API: ----------------------------------

def createTables():
    # TODO: implement
    conn = None
    try:
        conn = Connector.DBConnector()
        # conn.execute("CREATE TABLE Users(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        conn.execute("CREATE TABLE Critic(\
            Critic_ID INTEGER PRIMARY KEY,\
             Name Text NOT NULL)")

        conn.execute("CREATE TABLE Movie(\
            Movie_Name VARCHAR(255) NOT NULL,\
            Year Integer NOT NULL,\
            Genre VARCHAR(6) NOT NULL,\
            check(Year >= 1895),\
            UNIQUE(Movie_Name, Year))")

        conn.execute("CREATE TABLE Actor(\
            Actor_ID Integer NOT NULL,\
            Name TEXT NOT NULL,\
            Age Integer NOT NULL,\
            Height Integer NOT NULL,\
            check(Actor_ID > 0),\
            check(Age > 0),\
            check(Height > 0),\
            UNIQUE(Actor_ID))")

        conn.execute("CREATE TABLE Studio(\
            Studio_ID INTEGER NOT NULL,\
            Name TEXT NOT NULL,\
            UNIQUE(Studio_ID))")

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        # will happen any way after try termination or exception handling
        conn.close()


def clearTables():
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("DELETE FROM Critic")
        conn.execute("DELETE FROM Movie")
        conn.execute("DELETE FROM Actor")
        conn.execute("DELETE FROM Studio")

    except DatabaseException.ConnectionInvalid as e:
        # do stuff
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        # do stuff
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        # do stuff
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        # do stuff
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        # do stuff
        print(e)
    except Exception as e:
        print(e)
    finally:
        # will happen any way after code try termination or exception handling
        conn.close()


def dropTables():
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("DROP TABLE IF EXISTS Critic CASCADE")
        conn.execute("DROP TABLE IF EXISTS Movie CASCADE")
        conn.execute("DROP TABLE IF EXISTS Actor CASCADE")
        conn.execute("DROP TABLE IF EXISTS Studio CASCADE")

    except DatabaseException.ConnectionInvalid as e:
        # do stuff
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        # do stuff
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        # do stuff
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        # do stuff
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        # do stuff
        print(e)
    except Exception as e:
        print(e)
    finally:
        # will happen any way after code try termination or exception handling
        conn.close()


def addCritic(critic: Critic) -> ReturnValue:
    # TODO: implement
    pass


def deleteCritic(critic_id: int) -> ReturnValue:
    # TODO: implement
    pass


def getCriticProfile(critic_id: int) -> Critic:
    # TODO: implement
    pass


def addActor(actor: Actor) -> ReturnValue:
    # TODO: implement
    pass


def deleteActor(actor_id: int) -> ReturnValue:
    # TODO: implement
    pass


def getActorProfile(actor_id: int) -> Actor:
    # TODO: implement
    pass


def addMovie(movie: Movie) -> ReturnValue:
    # TODO: implement
    pass


def deleteMovie(movie_name: str, year: int) -> ReturnValue:
    # TODO: implement
    pass


def getMovieProfile(movie_name: str, year: int) -> Movie:
    # TODO: implement
    pass


def addStudio(studio: Studio) -> ReturnValue:
    # TODO: implement
    pass


def deleteStudio(studio_id: int) -> ReturnValue:
    # TODO: implement
    pass


def getStudioProfile(studio_id: int) -> Studio:
    # TODO: implement
    pass


def criticRatedMovie(movieName: str, movieYear: int, criticID: int, rating: int) -> ReturnValue:
    # TODO: implement
    pass


def criticDidntRateMovie(movieName: str, movieYear: int, criticID: int) -> ReturnValue:
    # TODO: implement
    pass


def actorPlayedInMovie(movieName: str, movieYear: int, actorID: int, salary: int, roles: List[str]) -> ReturnValue:
    # TODO: implement
    pass


def actorDidntPlayeInMovie(movieName: str, movieYear: int, actorID: int) -> ReturnValue:
    # TODO: implement
    pass


def studioProducedMovie(studioID: int, movieName: str, movieYear: int, budget: int, revenue: int) -> ReturnValue:
    # TODO: implement
    pass


def studioDidntProduceMovie(studioID: int, movieName: str, movieYear: int) -> ReturnValue:
    # TODO: implement
    pass


# ---------------------------------- BASIC API: ----------------------------------
def averageRating(movieName: str, movieYear: int) -> float:
    # TODO: implement
    pass


def averageActorRating(actorID: int) -> float:
    # TODO: implement
    pass


def bestPerformance(actor_id: int) -> Movie:
    # TODO: implement
    pass


def stageCrewBudget(movieName: str, movieYear: int) -> int:
    # TODO: implement
    pass


def overlyInvestedInMovie(movie_name: str, movie_year: int, actor_id: int) -> bool:
    # TODO: implement
    pass


# ---------------------------------- ADVANCED API: ----------------------------------


def franchiseRevenue() -> List[Tuple[str, int]]:
    # TODO: implement
    pass


def studioRevenueByYear() -> List[Tuple[str, int]]:
    # TODO: implement
    pass


def getFanCritics() -> List[Tuple[int, int]]:
    # TODO: implement
    pass


def averageAgeByGenre() -> List[Tuple[str, float]]:
    # TODO: implement
    pass


def getExclusiveActors() -> List[Tuple[int, int]]:
    # TODO: implement
    pass

# GOOD LUCK!
