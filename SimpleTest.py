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

class Test(AbstractTest):

    def testCritic(self) -> None:
        invalid_critic = Critic(critic_id=1, critic_name=None)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addCritic(invalid_critic), "invalid name")
        invalid_critic = Critic(critic_id=None, critic_name="John")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addCritic(invalid_critic), "invalid id")
        jhon = Critic(critic_id=1, critic_name="John")
        self.assertEqual(ReturnValue.OK, Solution.addCritic(jhon), "valid critic1")
        bob = Critic(critic_id=1, critic_name="Bob")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addCritic(bob), "existing id")

        #My Added Tests
        danny = Critic(critic_id=2, critic_name="Danny")
        self.assertEqual(ReturnValue.OK, Solution.addCritic(danny), "valid critic2")

        #deletion
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteCritic(3), "deleting non existing id")
        self.assertEqual(ReturnValue.OK, Solution.deleteCritic(1), "deleting existing id")

        #getCriticProfile
        self.assertEqual(Critic.badCritic(), Solution.getCriticProfile(3), "get non existing profile")
        self.assertEqual(danny, Solution.getCriticProfile(2), "get existing profile")

    def testActor(self) -> None:
        invalid_actor = Actor(actor_id=None, actor_name=None, age=-500, height=0)
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addActor(invalid_actor), "invalid parameters")
        leonardo = Actor(actor_id=1, actor_name="Leonardo DiCaprio", age=48, height=183)
        self.assertEqual(ReturnValue.OK, Solution.addActor(leonardo), "should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addActor(leonardo), "already exists")

        # My Added Tests
        john = Actor(actor_id=122, actor_name="John", age=27, height=189)
        self.assertEqual(ReturnValue.OK, Solution.addActor(john), "valid actor2")

        # john = Actor(actor_id=122, actor_name="John", age=27, height=189)
        # deletion
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteActor(12312), "deleting non existing id")
        self.assertEqual(ReturnValue.OK, Solution.deleteActor(1), "deleting existing id")

        # getActorProfile
        self.assertEqual(Actor.badActor(), Solution.getActorProfile(1223), "get non existing profile")
        self.assertEqual(john, Solution.getActorProfile(122), "get existing profile")
        # print("solution: ", Solution.getActorProfile(122))
        # print("wolfie: ", john)

    def testMovie(self) -> None:
        invalid_movie = Movie(movie_name="Mission Impossible", year="343", genre="Action")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMovie(invalid_movie), "invalid year")
        mission_impossible = Movie(movie_name="Mission Impossible", year="1996", genre="Action")  #note that postgreSQL will convert this string to an int
        self.assertEqual(ReturnValue.OK, Solution.addMovie(mission_impossible), "should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addMovie(mission_impossible), "already exists")

        # My Added Tests
        invalid_movie1 = Movie(movie_name="Mission Impossible", year="1996", genre="Acton")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMovie(invalid_movie1), "invalid genre")

        invalid_movie2 = Movie(movie_name=None, year="1996", genre="Action")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addMovie(invalid_movie2), "invalid movie_name")

        wolfie = Movie(movie_name="Wolf of Wallstreet", year=2012, genre="Drama")
        self.assertEqual(ReturnValue.OK, Solution.addMovie(wolfie), "should work")

        # getMovieProfile
        self.assertEqual(Movie.badMovie(), Solution.getMovieProfile("Wolf of Wallstreet", "2021"), "get non existing profile")
        self.assertEqual(wolfie, Solution.getMovieProfile("Wolf of Wallstreet", 2012), "get existing profile")
        # print("solution: ", type(Solution.getMovieProfile("Wolf of Wallstreet", "2012").getYear()))
        # print("wolfie: ", type(wolfie.getYear()))

        #deletion
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteMovie("Wolf of Wallstreet", 1999), "deleting non existing movie")
        self.assertEqual(ReturnValue.OK, Solution.deleteMovie("Mission Impossible", "1996"), "deleting existing movie")


    def testStudio(self) -> None:
        invalid_studio = Studio(studio_id=None, studio_name="Warner Bros")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addStudio(invalid_studio), "invalid id")
        warner_bros = Studio(studio_id=1, studio_name="Warner Bros")
        self.assertEqual(ReturnValue.OK, Solution.addStudio(warner_bros), "should work")
        paramount = Studio(studio_id=1, studio_name="Paramount")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addStudio(paramount), "ID 1 already exists")

        # My Added Tests

        haifa_studio = Studio(studio_id=2, studio_name="Haifa Studio")
        self.assertEqual(ReturnValue.OK, Solution.addStudio(haifa_studio), "valid studio2")

        # deletion
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteStudio(3), "deleting non existing id")
        self.assertEqual(ReturnValue.OK, Solution.deleteStudio(1), "deleting existing id")

        # getCriticProfile
        self.assertEqual(Studio.badStudio(), Solution.getStudioProfile(3), "get non existing profile")
        self.assertEqual(haifa_studio, Solution.getStudioProfile(2), "get existing profile")


# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
