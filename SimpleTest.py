import unittest
import Solution
from Utility.ReturnValue import ReturnValue
from Tests.abstractTest import AbstractTest

from Business.Critic import Critic
from Business.Actor import Actor
from Business.Movie import Movie
from Business.Studio import Studio

'''
    Simple test, create one of your own
    make sure the tests' names start with test
'''
from psycopg2 import sql
import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException



class Test(AbstractTest):

    # def testCritic(self) -> None:
    #     invalid_critic = Critic(critic_id=1, critic_name=None)
    #     self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addCritic(invalid_critic), "invalid name")
    #     invalid_critic = Critic(critic_id=None, critic_name="John")
    #     self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addCritic(invalid_critic), "invalid id")
    #     jhon = Critic(critic_id=1, critic_name="John")
    #     self.assertEqual(ReturnValue.OK, Solution.addCritic(jhon), "valid critic1")
    #     bob = Critic(critic_id=1, critic_name="Bob")
    #     self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addCritic(bob), "existing id")
    #     #
    #     #     #My Added Tests
    #     danny = Critic(critic_id=2, critic_name="Danny")
    #     self.assertEqual(ReturnValue.OK, Solution.addCritic(danny), "valid critic2")
    #     #
    #     #     #deletion
    #     self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteCritic(3), "deleting non existing id")
    #     self.assertEqual(ReturnValue.OK, Solution.deleteCritic(1), "deleting existing id")
    #     #
    #     #     #getCriticProfile
    #     self.assertEqual(Critic.badCritic(), Solution.getCriticProfile(3), "get non existing profile")
    #     self.assertEqual(danny, Solution.getCriticProfile(2), "get existing profile")

    # def testActor(self) -> None:
    #     invalid_actor = Actor(actor_id=None, actor_name=None, age=-500, height=0)
    #     self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addActor(invalid_actor), "invalid parameters")
    #     leonardo = Actor(actor_id=1, actor_name="Leonardo DiCaprio", age=48, height=183)
    #     self.assertEqual(ReturnValue.OK, Solution.addActor(leonardo), "should work")
    #     self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addActor(leonardo), "already exists")
    #     #
    #     #     # My Added Tests
    #     john = Actor(actor_id=122, actor_name="John", age=27, height=189)
    #     self.assertEqual(ReturnValue.OK, Solution.addActor(john), "valid actor2")
    #     #
    #     john = Actor(actor_id=122, actor_name="John", age=27, height=189)
    #     #     # deletion
    #     self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteActor(12312), "deleting non existing id")
    #     self.assertEqual(ReturnValue.OK, Solution.deleteActor(1), "deleting existing id")
    #     #
    #     #     # getActorProfile
    #     self.assertEqual(Actor.badActor(), Solution.getActorProfile(1223), "get non existing profile")
    #     self.assertEqual(john, Solution.getActorProfile(122), "get existing profile")
    # #     # print("solution: ", Solution.getActorProfile(122))
    # #     # print("wolfie: ", john)

    # def testMovie(self) -> None:
    #     invalid_movie = Movie(movie_name="Mission Impossible", year="343", genre="Action")
    #     self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMovie(invalid_movie), "invalid year")
    #     mission_impossible = Movie(movie_name="Mission Impossible", year="1996", genre="Action")  #note that postgreSQL will convert this string to an int
    #     self.assertEqual(ReturnValue.OK, Solution.addMovie(mission_impossible), "should work")
    #     self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addMovie(mission_impossible), "already exists")
    #     #
    #     #     # My Added Tests
    #     invalid_movie1 = Movie(movie_name="Mission Impossible", year="1996", genre="Acton")
    #     self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMovie(invalid_movie1), "invalid genre")
    #     #
    #     invalid_movie2 = Movie(movie_name=None, year="1996", genre="Action")
    #     self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMovie(invalid_movie2), "invalid movie_name")
    #     #
    #     django = Movie(movie_name="Django", year=2009, genre="Drama")
    #     self.assertEqual(ReturnValue.OK, Solution.addMovie(django), "should work")
    #     #
    #     #     # getMovieProfile
    #     self.assertEqual(Movie.badMovie(), Solution.getMovieProfile(movie_name="Django", year="2010"), "get non existing profile")
    #     self.assertEqual(django, Solution.getMovieProfile(movie_name="Django", year=2009), "get existing profile")
    #     # print("solution: ", type(Solution.getMovieProfile("Django", "2009").getYear()))
    #     # print("django: ", type(django.getYear()))
    #     #
    #     #     #deletion
    #     self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteMovie("Wolf of Wallstreet", 1999), "deleting non existing movie")
    #     self.assertEqual(ReturnValue.OK, Solution.deleteMovie("Mission Impossible", "1996"), "deleting existing movie")

    #
    # def testStudio(self) -> None:
    #     invalid_studio = Studio(studio_id=None, studio_name="Warner Bros")
    #     self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addStudio(invalid_studio), "invalid id")
    #     warner_bros = Studio(studio_id=1, studio_name="Warner Bros")
    #     self.assertEqual(ReturnValue.OK, Solution.addStudio(warner_bros), "should work")
    #     paramount = Studio(studio_id=1, studio_name="Paramount")
    #     self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addStudio(paramount), "ID 1 already exists")
    #
    #     #     # My Added Tests
    #     #
    #     haifa_studio = Studio(studio_id=2, studio_name="Haifa Studio")
    #     self.assertEqual(ReturnValue.OK, Solution.addStudio(haifa_studio), "valid studio2")
    #
    #     # deletion
    #     self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteStudio(3), "deleting non existing id")
    #     self.assertEqual(ReturnValue.OK, Solution.deleteStudio(1), "deleting existing id")
    #
    #     # getCriticProfile
    #     self.assertEqual(Studio.badStudio(), Solution.getStudioProfile(3), "get non existing profile")
    #     self.assertEqual(haifa_studio, Solution.getStudioProfile(2), "get existing profile")
    #
    #
    # #my tests
    # def testCriticRatedMovie(self) -> None:
    #
    #     oriel = Critic(critic_id=123, critic_name="Oriel")
    #     self.assertEqual(ReturnValue.OK, Solution.addCritic(oriel), "valid critic3")
    #
    #     tal = Critic(critic_id=124, critic_name="Tal")
    #     self.assertEqual(ReturnValue.OK, Solution.addCritic(tal), "valid critic4")
    #
    #     wolfie = Movie(movie_name="Wolf of Wallstreet", year=2012, genre="Drama")
    #     self.assertEqual(ReturnValue.OK, Solution.addMovie(wolfie), "should work")
    #
    #     self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie('Wolf of Wallstreet', 2012, 123, 5), "legit critic rating")
    #     self.assertEqual(ReturnValue.BAD_PARAMS, Solution.criticRatedMovie('Wolf of Wallstreet', 2012, 124, 6), "bad params cause of rating=6")
    #     self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie('Wolf of Wallstreet', 2012, 124, 4), "legit critic rating")
    #     self.assertEqual(ReturnValue.NOT_EXISTS, Solution.criticRatedMovie('Wolf of Wallstreet', 20121, 113124, 4), "not exist - foreign key problem")
    #
    #
    # def testCriticDidntRateMovie(self) -> None:
    #
    #     oriel = Critic(critic_id=123, critic_name="Oriel")
    #     self.assertEqual(ReturnValue.OK, Solution.addCritic(oriel), "valid critic3")
    #
    #     tal = Critic(critic_id=124, critic_name="Tal")
    #     self.assertEqual(ReturnValue.OK, Solution.addCritic(tal), "valid critic4")
    #
    #     wolfie = Movie(movie_name="Wolf of Wallstreet", year=2012, genre="Drama")
    #     self.assertEqual(ReturnValue.OK, Solution.addMovie(wolfie), "should work")
    #
    #     self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie(movieName='Wolf of Wallstreet', movieYear=2012, criticID=123, rating=5), "legit critic rating")
    #     self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie(movieName='Wolf of Wallstreet', movieYear=2012, criticID=124, rating=3), "legit critic rating")
    #
    #     self.assertEqual(ReturnValue.OK, Solution.criticDidntRateMovie(movieName='Wolf of Wallstreet', movieYear=2012, criticID=124), "legit critic deleting")
    #     self.assertEqual(ReturnValue.NOT_EXISTS, Solution.criticDidntRateMovie(movieName='Wolf of Wallstreet', movieYear=2012, criticID=124), "not exist deleting")
    #
    # def testAverageRating(self) -> None:
        # self.assertEqual(0, Solution.averageRating("Forrest Gump", 1994), "no movie")

        #add movie
        # forrest_gump = Movie(movie_name="Forrest Gump", year=1994, genre="Drama")
        # self.assertEqual(ReturnValue.OK, Solution.addMovie(forrest_gump), "should work")

        # spiderman = Movie(movie_name="Spiderman", year=2006, genre="Action")
        # self.assertEqual(ReturnValue.OK, Solution.addMovie(spiderman), "should work")
        #
        # superman = Movie(movie_name="Superman", year=2007, genre="Action")
        # self.assertEqual(ReturnValue.OK, Solution.addMovie(superman), "should work")
        #
        #
        # self.assertEqual(0, Solution.averageRating("Forrest Gump", 1994), "no ratings")
        #
        # jake = Actor(actor_id=2001, actor_name="Jake", age=48, height=183)
        # self.assertEqual(ReturnValue.OK, Solution.addActor(jake), "should work")
        #
        # self.assertEqual(ReturnValue.OK, Solution.actorPlayedInMovie('Forrest Gump', 1994, 2001, 100000,
        #                                                              ['Forrest', 'Main Role', 'Role3']), "legit acting")
        # self.assertEqual(ReturnValue.OK, Solution.actorPlayedInMovie('Spiderman', 2006, 2001, 100000,
        #                                                              ['Forrest', 'Main Role', 'Role3']), "legit acting")
        # self.assertEqual(ReturnValue.OK, Solution.actorPlayedInMovie('Superman', 2007, 2001, 100000,
        #                                                              ['Forrest', 'Main Role', 'Role3']), "legit acting")

        #create critics
        # critic1000 = Critic(critic_id=1000, critic_name="critic1000")
        # self.assertEqual(ReturnValue.OK, Solution.addCritic(critic1000), "valid critic3")
        # critic1001 = Critic(critic_id=1001, critic_name="critic1001")
        # self.assertEqual(ReturnValue.OK, Solution.addCritic(critic1001), "valid critic3")
        # critic1002 = Critic(critic_id=1002, critic_name="critic1002")
        # self.assertEqual(ReturnValue.OK, Solution.addCritic(critic1002), "valid critic3")
        # critic1003 = Critic(critic_id=1003, critic_name="critic1003")
        # self.assertEqual(ReturnValue.OK, Solution.addCritic(critic1003), "valid critic3")
        # #
        #add ratings
        # self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie('Forrest Gump', 1994, 1000, 5), "legit rating")
        # self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie('Forrest Gump', 1994, 1001, 4), "legit rating")
        # self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie('Forrest Gump', 1994, 1002, 5), "legit rating")
        # self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie('Forrest Gump', 1994, 1003, 5), "legit rating")
        #
        # self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie('Spiderman', 2006, 1000, 3), "legit rating")
        # self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie('Spiderman', 2006, 1001, 5), "legit rating")
        # self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie('Spiderman', 2006, 1002, 3), "legit rating")
        # self.assertEqual(ReturnValue.OK, Solution.criticRatedMovie('Spiderman', 2006, 1003, 3), "legit rating")

        # self.assertEqual(4.75, Solution.averageRating("Forrest Gump", 1994), "rating is (5+4+5+5)/4 = 4.75")
        # conn = Connector.DBConnector()
        # conn.execute("SELECT * FROM MovieAverageCriticRating", printSchema=True)
        # conn.execute("SELECT * FROM MovieAverageRating", printSchema=True)

        # float_res = Solution.bestPerformance(2001)
        # print("float_res: ", float_res)

    def testActorPlayedInMovie(self) -> None:
        top = Actor(actor_id=2000, actor_name="Tom Hanks", age=60, height=183)
        self.assertEqual(ReturnValue.OK, Solution.addActor(top), "should work")

        jake = Actor(actor_id=2001, actor_name="Jake", age=48, height=183)
        self.assertEqual(ReturnValue.OK, Solution.addActor(jake), "should work")

        forrest_gump = Movie(movie_name="Forrest Gump", year=1994, genre="Drama")
        self.assertEqual(ReturnValue.OK, Solution.addMovie(forrest_gump), "should work")

        prisoners = Movie(movie_name="Prisoners", year=2012, genre="Drama")
        self.assertEqual(ReturnValue.OK, Solution.addMovie(prisoners), "should work")

        self.assertEqual(ReturnValue.OK, Solution.actorPlayedInMovie('Forrest Gump', 1994, 2000, 100000, ['Forrest', 'Main Role', 'Role3']), "legit acting")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.actorPlayedInMovie('Forrest Gump', 1994, 2000, 100000, ['Forrest', 'Main Role']), "already exist acting")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.actorPlayedInMovie('Prisoners', 2012, 2001, -10, ["Role1", 'Role2']), "bad params - negative salary")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.actorPlayedInMovie('Prisoners', 2012, 2001, -10, []), "bad params - empty list")
        self.assertEqual(ReturnValue.OK, Solution.actorPlayedInMovie('Prisoners', 2012, 2001, 200000, ["Role1", 'Role2', 'Role3']), "legit acting")

        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.actorPlayedInMovie('Avatar', 2012, 2001, 100000, ["Role1", 'Role2']), "no such movie")


        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.actorDidntPlayInMovie('Avatar', 2012, 2001), "actor didnt play")
        self.assertEqual(ReturnValue.OK, Solution.actorDidntPlayInMovie('Prisoners', 2012, 2001), "delete actor played")

        self.assertEqual(['Role3', 'Main Role', 'Forrest'], Solution.getActorsRoleInMovie(2000, 'Forrest Gump', 1994), "legit roles")



    # def testStudioProducedMovie(self) -> None:
    #     studio1 = Studio(studio_id=3000, studio_name="Studio1")
    #     self.assertEqual(ReturnValue.OK, Solution.addStudio(studio1), "should work")
    #     studio2 = Studio(studio_id=3001, studio_name="studio2")
    #     self.assertEqual(ReturnValue.OK, Solution.addStudio(studio2), "should work")
    #
    #     goodfellas = Movie(movie_name="Good Fellas", year=1994, genre="Drama")
    #     self.assertEqual(ReturnValue.OK, Solution.addMovie(goodfellas), "should work")
    #
    #     moviename = Movie(movie_name="moviename", year=2012, genre="Drama")
    #     self.assertEqual(ReturnValue.OK, Solution.addMovie(moviename), "should work")
    #
    #     self.assertEqual(ReturnValue.BAD_PARAMS, Solution.studioProducedMovie(3000, "Good Fellas", 1994, -100, 150), "negative")
    #     self.assertEqual(ReturnValue.BAD_PARAMS, Solution.studioProducedMovie(3000, "Good Fellas", 1994, 100, -150), "negative")
    #     self.assertEqual(ReturnValue.OK, Solution.studioProducedMovie(3000, "Good Fellas", 1994, 100, 150), "legit")
    #     self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.studioProducedMovie(3000, "Good Fellas", 1994, 100, 150), "already exist")
    #     self.assertEqual(ReturnValue.OK, Solution.studioProducedMovie(3001, "moviename", 2012, 100, 150), "legit")
    #     self.assertEqual(ReturnValue.NOT_EXISTS, Solution.studioProducedMovie(3001, "notexist_moviename", 2012, 100, 150), "not exist")
    #
    #     self.assertEqual(ReturnValue.OK, Solution.studioDidntProduceMovie(3000, "Good Fellas", 1994), "legit deletion")
    #     self.assertEqual(ReturnValue.OK, Solution.studioDidntProduceMovie(3001, "moviename", 2012), "legit deletion")


    # def testMoviesAverageCriticRating(self) -> None:
    #     fight_club = Movie(movie_name="Fight Club", year="1994", genre="Action")
    #     self.assertEqual(ReturnValue.OK, Solution.addMovie(fight_club), "should work")
    #
    #     spiderman = Movie(movie_name="Spiderman", year=2006, genre="Action")
    #     self.assertEqual(ReturnValue.OK, Solution.addMovie(spiderman), "should work")

    # def testStageCrewBudget(self):
    #     spiderman = Movie(movie_name="Spiderman", year=2006, genre="Action")
    #     self.assertEqual(ReturnValue.OK, Solution.addMovie(spiderman), "should work")
    #
    #     superman = Movie(movie_name="Superman", year=2007, genre="Action")
    #     self.assertEqual(ReturnValue.OK, Solution.addMovie(superman), "should work")
    #
    #     studio1 = Studio(studio_id=3000, studio_name="Studio1")
    #     self.assertEqual(ReturnValue.OK, Solution.addStudio(studio1), "should work")
    #     self.assertEqual(ReturnValue.OK, Solution.studioProducedMovie(3000, "Spiderman", 2006, 70000, 150), "legit")
    #     # self.assertEqual(ReturnValue.OK, Solution.studioProducedMovie(3000, "Spiderman", 2006, 100, 150), "legit")
    #
    #     jake1 = Actor(actor_id=2001, actor_name="Jake", age=48, height=183)
    #     self.assertEqual(ReturnValue.OK, Solution.addActor(jake1), "should work")
    #     jake2 = Actor(actor_id=2002, actor_name="Jake", age=48, height=183)
    #     self.assertEqual(ReturnValue.OK, Solution.addActor(jake2), "should work")
    #
    #     self.assertEqual(ReturnValue.OK, Solution.actorPlayedInMovie('Spiderman', 2006, 2001, 20000,
    #                                                                  ['Forrest', 'Main Role', 'Role3']), "legit acting")
    #     self.assertEqual(ReturnValue.OK, Solution.actorPlayedInMovie('Spiderman', 2006, 2002, 30000,
    #                                                                  ['Forrest', 'Main Role', 'Role3']), "legit acting")
    #
    #     res = Solution.stageCrewBudget('Spiderman', 2006)
    #     print('The Result: ', res)

















# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
