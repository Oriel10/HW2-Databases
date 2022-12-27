from typing import List, Tuple

import psycopg2
from psycopg2 import sql
from psycopg2 import errors

import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException

from Business.Movie import Movie
from Business.Studio import Studio
from Business.Critic import Critic
from Business.Actor import Actor
'''
notes:
1)in actorPlayedInMovie we cannot use "if" for an empty list
2)line 717 - i'm not sure you can check these things with if 
'''


def resultSetToCritic(resultset_row: list) -> Critic:
    if len(resultset_row) != 2:
        return Critic.badCritic()
    return Critic(resultset_row[0], resultset_row[1])

def resultSetToMovie(resultset_row: list) -> Movie:
    if len(resultset_row) != 3:
        return Movie.badMovie()
    return Movie(resultset_row[0], resultset_row[1], resultset_row[2])

def resultSetToStudio(resultset_row: list) -> Studio:
    if len(resultset_row) != 2:
        return Studio.badStudio()
    return Studio(resultset_row[0], resultset_row[1])

def resultSetToActor(resultset_row: list) -> Actor:
    if len(resultset_row) != 4:
        return Actor.badActor()
    return Actor(resultset_row[0], resultset_row[1], resultset_row[2], resultset_row[3])



# ---------------------------------- CRUD API: ----------------------------------

def createTables():
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("CREATE TABLE Critic(\
            Critic_ID INTEGER PRIMARY KEY,\
            check(Critic_ID > 0),\
            Name Text NOT NULL)")

        conn.execute("CREATE TABLE Movie(\
            Movie_Name TEXT,\
            Year INTEGER,\
            Genre VARCHAR(6) NOT NULL,\
            check(Year >= 1895),\
            check(Genre = 'Drama' OR Genre = 'Action' OR Genre = 'Comedy' OR Genre = 'Horror'),\
            PRIMARY KEY(Movie_Name, Year))")

        conn.execute("CREATE TABLE Actor(\
            Actor_ID INTEGER,\
            Name TEXT NOT NULL,\
            Age INTEGER NOT NULL,\
            Height INTEGER NOT NULL,\
            check(Actor_ID > 0),\
            check(Age > 0),\
            check(Height > 0),\
            PRIMARY KEY(Actor_ID))")

        conn.execute("CREATE TABLE Studio(\
            Studio_ID INTEGER,\
            Name TEXT NOT NULL,\
            check(Studio_ID > 0),\
            PRIMARY KEY(Studio_ID))")

        conn.execute("CREATE TABLE CriticRating(\
                    Movie_Name TEXT,\
                    Year INTEGER,\
                    Critic_ID INTEGER,\
                    Rating INTEGER,\
                    check(1 <= Rating AND Rating <= 5),\
                    FOREIGN KEY(Movie_Name, Year) REFERENCES Movie(Movie_Name, Year) ON DELETE CASCADE,\
                    FOREIGN KEY(Critic_ID) REFERENCES Critic(Critic_ID) ON DELETE CASCADE,\
                    PRIMARY KEY(Movie_Name, Year, Critic_ID))")

        conn.execute("CREATE TABLE ActorInMovie(\
                            Movie_Name TEXT,\
                            Year INTEGER,\
                            Actor_ID INTEGER,\
                            Salary INTEGER,\
                            Num_Roles INTEGER,\
                            check(0 < Salary),\
                            check(0 < Num_Roles),\
                            FOREIGN KEY(Movie_Name, Year) REFERENCES Movie(Movie_Name, Year) ON DELETE CASCADE,\
                            FOREIGN KEY(Actor_ID) REFERENCES Actor(Actor_ID) ON DELETE CASCADE,\
                            PRIMARY KEY(Movie_Name, Year, Actor_ID))")

        conn.execute("CREATE TABLE ActorRoleInMovie(\
                                    Movie_Name TEXT,\
                                    Year INTEGER,\
                                    Actor_ID INTEGER,\
                                    Actor_Role TEXT NOT NULL,\
                                    FOREIGN KEY(Movie_Name, Year, Actor_ID) REFERENCES ActorInMovie(Movie_Name, Year, Actor_ID) ON DELETE CASCADE)")

        conn.execute("CREATE TABLE StudioProducedMovie(\
                        Movie_Name TEXT,\
                        Year INTEGER,\
                        Studio_ID INTEGER,\
                        Budget INTEGER NOT NULL,\
                        Revenue INTEGER NOT NULL,\
                        check(0 <= Budget),\
                        check(0 <= Revenue),\
                        PRIMARY KEY(Movie_Name, Year),\
                        FOREIGN KEY(Movie_Name, Year) REFERENCES Movie(Movie_Name, Year) ON DELETE CASCADE,\
                        FOREIGN KEY(Studio_ID) REFERENCES Studio(Studio_ID) ON DELETE CASCADE)")

        conn.execute("CREATE VIEW MovieAverageCriticRating AS\
                          SELECT Movie_Name, Year, AVG(Rating) as average_rating\
                          FROM CriticRating\
                          GROUP BY (Movie_Name, Year)")

        conn.execute("CREATE VIEW MovieAverageRating AS\
                          SELECT M.Movie_Name, M.Year, COALESCE(MACR.average_rating, 0) as average_rating \
                          FROM Movie AS M LEFT OUTER JOIN MovieAverageCriticRating AS MACR\
                          ON MACR.Movie_Name = M.Movie_Name AND MACR.Year = M.Year")

        conn.execute("CREATE VIEW MovieBudget AS \
                        SELECT M.Movie_Name, M.Year, COALESCE(SPM.Budget, 0) AS Budget\
                        FROM Movie AS M LEFT OUTER JOIN StudioProducedMovie AS SPM\
                        ON M.Movie_Name = SPM.Movie_Name AND M.Year = SPM.Year")

        conn.execute("CREATE VIEW MovieTotalNumRoles AS \
                        SELECT AIM.Movie_Name, AIM.Year, SUM(Num_Roles) as Num_Roles\
                        FROM ActorInMovie AS AIM\
                        GROUP BY AIM.Movie_Name, AIM.Year")

        conn.execute("CREATE VIEW ActorInGenre AS \
                        SELECT DISTINCT AIM.Actor_ID, Name, Age, Height, Genre\
                        FROM Movie M, ActorInMovie AIM, Actor A\
                        WHERE M.Movie_Name = AIM.Movie_Name AND M.Year = AIM.Year AND AIM.Actor_ID = A.Actor_ID")


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
        conn.execute("DROP TABLE IF EXISTS CriticRating CASCADE")
        conn.execute("DROP TABLE IF EXISTS ActorInMovie CASCADE")
        conn.execute("DROP TABLE IF EXISTS ActorRoleInMovie CASCADE")
        conn.execute("DROP TABLE IF EXISTS StudioProducedMovie CASCADE")

        conn.execute("DROP VIEW IF EXISTS MovieAverageCriticRating")
        conn.execute("DROP VIEW IF EXISTS MovieAverageRating")
        conn.execute("DROP VIEW IF EXISTS MovieBudget")
        conn.execute("DROP VIEW IF EXISTS MovieTotalNumRoles")
        conn.execute("DROP VIEW IF EXISTS ActorInGenre")

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
    conn = None
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Critic(Critic_ID, Name) VALUES({id}, {username})").format(
            id=sql.Literal(critic.getCriticID()),
            username=sql.Literal(critic.getName())
        )
        rows_effected, _ = conn.execute(query)
        if rows_effected == 1:
            ret_val = ReturnValue.OK

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        ret_val = ReturnValue.ALREADY_EXISTS
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret_val



def deleteCritic(critic_id: int) -> ReturnValue:
    conn = None
    rows_effected = 0
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Critic WHERE Critic_ID={other_id}").format(
            other_id=sql.Literal(critic_id),
        )
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            ret_val = ReturnValue.NOT_EXISTS
        else:
            ret_val = ReturnValue.OK

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
        conn.close()
        return ret_val


def getCriticProfile(critic_id: int) -> Critic:
    conn = None
    rows_effected = 0
    res_critic = Critic.badCritic()
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("Select * FROM Critic WHERE Critic_ID={other_id}").format(
            other_id=sql.Literal(critic_id),
        )

        rows_effected, result = conn.execute(query)
        assert (result.size() == 1)
        res_critic = resultSetToCritic(result.rows[0])
        # print('res_critic: ', res_critic)
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
        conn.close()
        return res_critic


def addActor(actor: Actor) -> ReturnValue:
    conn = None
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Actor(Actor_ID, Name, Age, Height) VALUES({id}, {name}, {age}, {height})").format(
            id=sql.Literal(actor.getActorID()),
            name=sql.Literal(actor.getActorName()),
            age=sql.Literal(actor.getAge()),
            height=sql.Literal(actor.getHeight())
        )
        rows_effected, _ = conn.execute(query)
        if rows_effected == 1:
            ret_val = ReturnValue.OK

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        ret_val = ReturnValue.ALREADY_EXISTS
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret_val


def deleteActor(actor_id: int) -> ReturnValue:
    conn = None
    rows_effected = 0
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Actor WHERE Actor_ID={id}").format(
            id=sql.Literal(actor_id),
        )
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            ret_val = ReturnValue.NOT_EXISTS
        else:
            ret_val = ReturnValue.OK

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
        conn.close()
        return ret_val


def getActorProfile(actor_id: int) -> Actor:
    conn = None
    rows_effected = 0
    res_actor = Actor.badActor()
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("Select * FROM Actor WHERE Actor_ID={id}").format(
            id=sql.Literal(actor_id),
        )

        rows_effected, result = conn.execute(query)
        assert (result.size() == 1)
        res_actor = resultSetToActor(result.rows[0])
        # print('res_actor: ', res_actor)
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
        conn.close()
        return res_actor


def addMovie(movie: Movie) -> ReturnValue:
    conn = None
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Movie(Movie_Name, Year, Genre) VALUES({name}, {year}, {genre})").format(
            name=sql.Literal(movie.getMovieName()),
            year=sql.Literal(movie.getYear()),
            genre=sql.Literal(movie.getGenre())
        )
        rows_effected, _ = conn.execute(query)
        if rows_effected == 1:
            ret_val = ReturnValue.OK
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        ret_val = ReturnValue.ALREADY_EXISTS
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret_val


def deleteMovie(movie_name: str, year: int) -> ReturnValue:
    conn = None
    rows_effected = 0
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Movie WHERE Movie_Name={name} AND Year={y}").format(
            name=sql.Literal(movie_name),
            y=sql.Literal(year)
        )
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            ret_val = ReturnValue.NOT_EXISTS
        else:
            ret_val = ReturnValue.OK

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
        conn.close()
        return ret_val


def getMovieProfile(movie_name: str, year: int) -> Movie:
    conn = None
    rows_effected = 0
    res_movie = Movie.badMovie()
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("Select * FROM Movie WHERE Movie_Name={name} AND Year={y}").format(
            name=sql.Literal(movie_name),
            y=sql.Literal(year),
        )

        rows_effected, result = conn.execute(query)
        assert (result.size() == 1)
        res_movie = resultSetToMovie(result.rows[0])
        # print('res_movie: ', res_movie)
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
        conn.close()
        return res_movie


def addStudio(studio: Studio) -> ReturnValue:
    conn = None
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Studio(Studio_ID, Name) VALUES({id}, {name})").format(
            id=sql.Literal(studio.getStudioID()),
            name=sql.Literal(studio.getStudioName())
        )
        rows_effected, _ = conn.execute(query)
        if rows_effected == 1:
            ret_val = ReturnValue.OK

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        ret_val = ReturnValue.ALREADY_EXISTS
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret_val

def deleteStudio(studio_id: int) -> ReturnValue:
    conn = None
    rows_effected = 0
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Studio WHERE Studio_ID={id}").format(
            id=sql.Literal(studio_id),
        )
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            ret_val = ReturnValue.NOT_EXISTS
        else:
            ret_val = ReturnValue.OK

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
        conn.close()
        return ret_val


def getStudioProfile(studio_id: int) -> Studio:
    conn = None
    rows_effected = 0
    res_studio = Studio.badStudio()
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("Select * FROM Studio WHERE Studio_ID={id}").format(
            id=sql.Literal(studio_id),
        )

        rows_effected, result = conn.execute(query)
        assert (result.size() == 1)
        res_studio = resultSetToStudio(result.rows[0])
        # print('res_studio: ', res_studio)
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
        conn.close()
        return res_studio


def criticRatedMovie(movieName: str, movieYear: int, criticID: int, rating: int) -> ReturnValue:
    conn = None
    rows_effected = 0
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO CriticRating(Movie_Name, Year, Critic_ID, Rating) VALUES({name}, {year}, {id}, {rating})").format(
            name=sql.Literal(movieName),
            year=sql.Literal(movieYear),
            id=sql.Literal(criticID),
            rating=sql.Literal(rating)
        )
        rows_effected, _ = conn.execute(query)
        if rows_effected == 1:
            ret_val = ReturnValue.OK

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        ret_val = ReturnValue.ALREADY_EXISTS
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        ret_val = ReturnValue.NOT_EXISTS
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret_val


def criticDidntRateMovie(movieName: str, movieYear: int, criticID: int) -> ReturnValue:
    conn = None
    rows_effected = 0
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM CriticRating WHERE Movie_Name={name} AND Year={y} AND Critic_ID={id}").format(
            name=sql.Literal(movieName),
            y=sql.Literal(movieYear),
            id=sql.Literal(criticID)
        )
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            ret_val = ReturnValue.NOT_EXISTS
        else:
            ret_val = ReturnValue.OK

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        ret_val = ReturnValue.NOT_EXISTS
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret_val

def actorPlayedInMovie(movieName: str, movieYear: int, actorID: int, salary: int, roles: List[str]) -> ReturnValue:
    conn = None
    rows_effected = 0
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO ActorInMovie(Movie_Name, Year, Actor_ID, Salary, Num_Roles) VALUES({name}, {year}, {id}, {salary}, {num_roles});").format(
            name=sql.Literal(movieName),
            year=sql.Literal(movieYear),
            id=sql.Literal(actorID),
            salary=sql.Literal(salary),
            num_roles=sql.Literal(len(roles))
        )

        query += sql.SQL("INSERT INTO ActorRoleInMovie(Movie_Name, Year, Actor_ID, Actor_Role) VALUES")
        for idx, role in enumerate(roles):
            query += sql.SQL("({name}, {year}, {id}, {actor_role})").format(
                name=sql.Literal(movieName),
                year=sql.Literal(movieYear),
                id=sql.Literal(actorID),
                actor_role=sql.Literal(role)
            )
            if idx + 1 < len(roles):
                query += sql.SQL(", ")

        rows_effected, _ = conn.execute(query, printSchema=True)
        # print("rows_effected: ", rows_effected)
        if rows_effected == len(roles):
            ret_val = ReturnValue.OK

        # testquery1 = sql.SQL("SELECT * FROM ActorInMovie")
        # rows_effected1, _ = conn.execute(testquery1, printSchema=True)
        # testquery2 = sql.SQL("SELECT * FROM ActorRoleInMovie")
        # rows_effected2, _ = conn.execute(testquery2, printSchema=True)

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        ret_val = ReturnValue.ALREADY_EXISTS
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        ret_val = ReturnValue.NOT_EXISTS
        print(e)
    except psycopg2.errors.SyntaxError as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret_val


def actorDidntPlayInMovie(movieName: str, movieYear: int, actorID: int) -> ReturnValue:
    conn = None
    rows_effected = 0
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM ActorInMovie WHERE Movie_Name={name} AND Year={y} AND Actor_ID={id}").format(
            name=sql.Literal(movieName),
            y=sql.Literal(movieYear),
            id=sql.Literal(actorID)
        )
        rows_effected, result = conn.execute(query)
        if rows_effected > 0:
            ret_val = ReturnValue.OK
        else:
            ret_val = ReturnValue.NOT_EXISTS

        # testquery1 = sql.SQL("SELECT * FROM ActorInMovie")
        # rows_effected1, _ = conn.execute(testquery1, printSchema=True)
        # testquery2 = sql.SQL("SELECT * FROM ActorRoleInMovie")
        # rows_effected2, _ = conn.execute(testquery2, printSchema=True)

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        ret_val = ReturnValue.NOT_EXISTS
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret_val


def studioProducedMovie(studioID: int, movieName: str, movieYear: int, budget: int, revenue: int) -> ReturnValue:
    conn = None
    rows_effected = 0
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO StudioProducedMovie(Movie_Name, Year, Studio_ID, Budget, Revenue) VALUES({name}, {year}, {id}, {budget}, {revenue})").format(
            name=sql.Literal(movieName),
            year=sql.Literal(movieYear),
            id=sql.Literal(studioID),
            budget=sql.Literal(budget),
            revenue=sql.Literal(revenue)
        )
        rows_effected, _ = conn.execute(query)
        if rows_effected == 1:
            ret_val = ReturnValue.OK

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        ret_val = ReturnValue.BAD_PARAMS
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        ret_val = ReturnValue.ALREADY_EXISTS
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        ret_val = ReturnValue.NOT_EXISTS
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret_val


def studioDidntProduceMovie(studioID: int, movieName: str, movieYear: int) -> ReturnValue:
    conn = None
    rows_effected = 0
    ret_val = ReturnValue.ERROR
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM StudioProducedMovie WHERE Movie_Name={name} AND Year={y} AND Studio_ID={id}").format(
            name=sql.Literal(movieName),
            y=sql.Literal(movieYear),
            id=sql.Literal(studioID)
        )
        rows_effected, result = conn.execute(query)
        if rows_effected == 0:
            ret_val = ReturnValue.NOT_EXISTS
        else:
            ret_val = ReturnValue.OK

        # testquery1 = sql.SQL("SELECT * FROM StudioProducedMovie")
        # rows_effected1, _ = conn.execute(testquery1, printSchema=True)

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        ret_val = ReturnValue.NOT_EXISTS
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return ret_val


# ---------------------------------- BASIC API: ----------------------------------
def averageRating(movieName: str, movieYear: int) -> float:
    conn = None
    res_val = 0
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "SELECT average_rating\
             FROM MovieAverageRating\
             WHERE Movie_Name={name} AND Year={y}").format(
            name=sql.Literal(movieName),
            y=sql.Literal(movieYear)
        )

        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
            res_val = result.rows[0][0] #TODO: find out what to return here - result.rows[0] is the tuple (Decimal('num'),)

        print("--result--: ", result)
        # print("res_val: ", (res_val))

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
        conn.close()
        return res_val

def averageActorRating(actorID: int) -> float:
    conn = None
    res_val = 0
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "SELECT AVG(average_rating) as actor_rating\
             FROM MovieAverageRating MAR, ActorInMovie AIM\
             WHERE AIM.Actor_ID={actorID} AND MAR.Movie_Name=AIM.Movie_Name AND MAR.Year=AIM.Year").format(
            actorID=sql.Literal(actorID)
        )
        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
            if result.rows[0][0] is None:
                res_val = 0
            else:
                res_val = result.rows[0][0]
        # print("result: ", result)
        # print("res_val: ", res_val)

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
        conn.close()
        return float(res_val)


def bestPerformance(actor_id: int) -> Movie:
    conn = None
    rows_effected = 0
    res_movie = Movie.badMovie()
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("Select M.Movie_Name, M.Year, M.Genre \
                        FROM Movie M, MovieAverageRating MAR, ActorInMovie AIM\
                        WHERE M.Movie_Name=MAR.Movie_Name AND M.Movie_Name=AIM.Movie_Name\
                        AND M.Year=MAR.Year AND M.Year=AIM.Year AND AIM.Actor_ID ={actorID}\
                        ORDER BY MAR.average_rating DESC, M.Year ASC, M.Movie_Name Desc\
                        LIMIT 1").format(
            actorID=sql.Literal(actor_id)
        )

        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
            res_movie = resultSetToMovie(result.rows[0])
        print('res_movie: ', res_movie)

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
        conn.close()
        return res_movie


def stageCrewBudget(movieName: str, movieYear: int) -> int:
    conn = None
    res_val = -1
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "SELECT COALESCE(IDK.Budget,0) - COALESCE(SUM(IK.Salary),0) as SCB\
             FROM (SELECT MB.Movie_Name, MB.Year, MB.Budget\
                   FROM MovieBudget AS MB\
                   WHERE MB.Movie_Name={movieName} AND MB.Year={movieYear}) AS IDK\
             LEFT OUTER JOIN \
                  (SELECT AIM.Movie_Name, AIM.Year, AIM.Salary\
                   FROM ActorInMovie AS AIM\
                   WHERE AIM.Movie_Name={movieName} AND AIM.Year={movieYear}) AS IK\
             ON IDK.Movie_Name=IK.Movie_Name AND IDK.Year=IK.Year\
             GROUP BY IDK.Movie_Name, IDK.Year, IDK.Budget").format(
            movieName=sql.Literal(movieName),
            movieYear=sql.Literal(movieYear)
        )

        rows_effected, result = conn.execute(query)
        if rows_effected == 1:
                res_val = result.rows[0][0]

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
        conn.close()
        return res_val


def overlyInvestedInMovie(movie_name: str, movie_year: int, actor_id: int) -> bool:
    conn = None
    res_val = False
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT AIM.Actor_ID\
                         FROM ActorInMovie AS AIM\
                         WHERE AIM.Movie_Name={movie_name} AND AIM.Year={movie_year} AND AIM.Actor_ID={actor_id} AND\
                         2*AIM.Num_Roles >= (SELECT MTNR.Num_Roles FROM MovieTotalNumRoles AS MTNR\
                         WHERE MTNR.Movie_Name={movie_name} AND MTNR.Year={movie_year})").format(

            movie_name=sql.Literal(movie_name),
            movie_year=sql.Literal(movie_year),
            actor_id=sql.Literal(actor_id)
        )

        rows_effected, result = conn.execute(query)
        res_val = 1 == rows_effected

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
        conn.close()
        return res_val


# ---------------------------------- ADVANCED API: ----------------------------------


def franchiseRevenue() -> List[Tuple[str, int]]:
    conn = None
    res_list = []
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "SELECT Mov.Movie_Name, COALESCE(SUM(PMOV.Revenue),0) as total_revenue\
             FROM\
                (SELECT M.Movie_Name\
                 FROM MOVIE M\
                 GROUP BY M.Movie_Name) AS Mov\
            LEFT OUTER JOIN\
                (SELECT SPM.Movie_Name, SPM.Revenue\
                 FROM StudioProducedMovie SPM) AS PMOV\
            ON Mov.Movie_Name = PMov.Movie_Name\
            GROUP BY Mov.Movie_Name\
            ORDER BY Movie_Name DESC")

        rows_effected, result = conn.execute(query)

        res_list = [(result[i]['Movie_Name'], result[i]['total_revenue']) for i in range(result.size())]

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
        conn.close()
        return res_list

def studioRevenueByYear() -> List[Tuple[str, int]]:
    conn = None
    res_list = []
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT SPM.Studio_ID, SPM.Year, SUM(SPM.Revenue) as total_revenue\
                         FROM StudioProducedMovie as SPM\
                         GROUP BY SPM.Studio_ID, SPM.Year\
                         ORDER BY SPM.Studio_ID DESC, SPM.Year DESC")
        rows_effected, result = conn.execute(query)

        res_list = [(result[i]['Studio_ID'], result[i]['Year'], result[i]['total_revenue']) for i in range(result.size())]

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
        conn.close()
        return res_list


def getFanCritics() -> List[Tuple[int, int]]:
    conn = None
    res_list = []
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT C.Critic_ID, S.Studio_ID\
                        FROM Critic C, Studio S\
                        WHERE NOT EXISTS\
                            (SELECT *\
                             FROM StudioProducedMovie SPM1\
                             WHERE Studio_ID = S.Studio_ID AND (SPM1.Movie_Name, SPM1.Year) NOT IN\
                                (SELECT CR.Movie_Name, CR.Year FROM CriticRating CR\
                                    WHERE CR.Critic_ID = C.Critic_ID)) AND\
                        EXISTS (SELECT * FROM StudioProducedMovie SPM2 WHERE SPM2.Studio_ID = S.Studio_ID)\
                        ORDER BY Critic_ID DESC ,Studio_ID DESC")

        rows_effected, result = conn.execute(query)

        res_list = [(result[i]['Critic_ID'], result[i]['Studio_ID']) for i in range(result.size())]

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
        conn.close()
        return res_list


def averageAgeByGenre() -> List[Tuple[str, float]]:
    conn = None
    res_list = []
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT AIG.Genre, AVG(AIG.Age) as average_age\
                         FROM ActorInGenre AIG\
                         GROUP BY AIG.Genre\
                         ORDER BY AIG.Genre")

        rows_effected, result = conn.execute(query)

        res_list = [(result[i]['Genre'], float(result[i]['average_age'])) for i in range(result.size())]

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
        conn.close()
        return res_list


def getExclusiveActors(print = False) -> List[Tuple[int, int]]:
    conn = None
    res_list = []
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT DISTINCT AIM1.Actor_ID, SPM1.Studio_ID\
                         FROM ActorInMovie AIM1, StudioProducedMovie SPM1\
                         WHERE AIM1.Movie_Name=SPM1.Movie_Name AND AIM1.Year=SPM1.Year AND\
                            NOT EXISTS(SELECT *\
                                       FROM ActorInMovie AIM2, StudioProducedMovie SPM2\
                                       WHERE AIM2.Movie_Name=SPM2.Movie_Name AND AIM2.Year=SPM2.Year\
                                           AND AIM1.Actor_ID=AIM2.Actor_ID AND SPM1.Studio_ID<>SPM2.Studio_ID)\
                         ORDER BY AIM1.Actor_ID DESC")

        rows_effected, result = conn.execute(query, printSchema=print)

        res_list = [(result[i]['Actor_ID'], result[i]['Studio_ID']) for i in range(result.size())]

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
        conn.close()
        return res_list

def getActorsRoleInMovie(actor_id : int, movie_name : str, movieYear :int) -> List[str]:
    conn = None
    res_list = []
    try:
        #ActorRoleInMovie
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT Actor_Role\
                         FROM ActorRoleInMovie\
                         WHERE Movie_Name={movie_name} AND Year={movieYear} AND Actor_ID={actor_id}\
                         ORDER BY Actor_Role DESC").format(
            movie_name=sql.Literal(movie_name),
            movieYear=sql.Literal(movieYear),
            actor_id=sql.Literal(actor_id)
        )

        rows_effected, result = conn.execute(query, printSchema=print)

        if rows_effected != 0:
            res_list = [result[i]['Actor_Role'] for i in range(rows_effected)]

        print("res_list: ", res_list)

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
        conn.close()
        return res_list
