import unittest

from Solution import *

GENRES = ['Drama', 'Action', 'Comedy', 'Horror']


class MovieStatsTest(unittest.TestCase):
    def setUp(self) -> None:
        dropTables()
        createTables()
        self._fillN(n=9)

    def _fillN(self, n: int) -> None:
        for j in range(1, n + 1):
            self.assertEqual(second=addMovie(Movie(f'm{j}', 1990 + j, GENRES[j % 4])), first=ReturnValue.OK)
            self.assertEqual(second=addActor(Actor(j, f'a{j}', 20 + 3 * j, j * 10)), first=ReturnValue.OK)
            self.assertEqual(second=addStudio(Studio(j, f's{j}')), first=ReturnValue.OK)
            self.assertEqual(second=addCritic(Critic(j, f'c{j}')), first=ReturnValue.OK)
            self.assertEqual(second=criticRatedMovie(f'm{j}', 1990 + j, j, j % 5 + 1), first=ReturnValue.OK)
            self.assertEqual(second=actorPlayedInMovie(f'm{j}', 1990 + j, j, j * 1000, [f'r{j}']), first=ReturnValue.OK)
            self.assertEqual(second=studioProducedMovie(j, f'm{j}', 1990 + j, j * 100, j * 700), first=ReturnValue.OK)

    def test_clearTables(self):
        clearTables()
        self._fillN(n=2)

    def test_addCritic(self):
        self.assertEqual(second=addCritic(Critic(1, 'c1')), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=addCritic(Critic(0, 'c')), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=addCritic(Critic(-5, 'c')), first=ReturnValue.BAD_PARAMS)

    def test_getCriticProfile(self):
        self.assertEqual(second=getCriticProfile(1), first=Critic(1, 'c1'))
        self.assertEqual(second=getCriticProfile(20), first=Critic.badCritic())
        self.assertEqual(second=getCriticProfile(0), first=Critic.badCritic())
        self.assertEqual(second=getCriticProfile(-5), first=Critic.badCritic())

    def test_deleteCritic(self):
        self.assertEqual(second=deleteCritic(1), first=ReturnValue.OK)
        self.assertEqual(second=deleteCritic(0), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=deleteCritic(20), first=ReturnValue.NOT_EXISTS)

    def test_addMovie(self):
        self.assertEqual(second=addMovie(Movie('m1', 1991, GENRES[0])), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=addMovie(Movie('m1', 1991, GENRES[1])), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=addMovie(Movie('m1', 1992, GENRES[0])), first=ReturnValue.OK)
        self.assertEqual(second=addMovie(Movie('m', 1894, GENRES[1])), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=addMovie(Movie('m', 2000, 'Spooky')), first=ReturnValue.BAD_PARAMS)

    def test_getMovieProfile(self):
        self.assertEqual(second=getMovieProfile('m1', 1991), first=Movie('m1', 1991, GENRES[1]))
        self.assertEqual(second=getMovieProfile('m1', 1990), first=Movie.badMovie())
        self.assertEqual(second=getMovieProfile('m1', 1), first=Movie.badMovie())
        self.assertEqual(second=getMovieProfile('m', 2000), first=Movie.badMovie())

    def test_deleteMovie(self):
        self.assertEqual(second=deleteMovie('m1', 1991), first=ReturnValue.OK)
        self.assertEqual(second=deleteMovie('m', 0), first=ReturnValue.NOT_EXISTS)

    def test_addActor(self):
        self.assertEqual(second=addActor(Actor(1, 'a1', 23, 10)), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=addActor(Actor(20, 'a1', 23, 10)), first=ReturnValue.OK)
        self.assertEqual(second=addActor(Actor(21, 'a1', 23, 0)), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=addActor(Actor(21, 'a1', 0, 10)), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=addActor(Actor(0, 'a1', 23, 10)), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=addActor(Actor(21, 'a1', 23, -5)), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=addActor(Actor(21, 'a1', -5, 10)), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=addActor(Actor(-5, 'a1', 23, 10)), first=ReturnValue.BAD_PARAMS)

    def test_getActorProfile(self):
        self.assertEqual(second=getActorProfile(1), first=Actor(1, 'a1', 23, 10))
        self.assertEqual(second=getActorProfile(0), first=Actor.badActor())
        self.assertEqual(second=getActorProfile(20), first=Actor.badActor())
        self.assertEqual(second=getActorProfile(-5), first=Actor.badActor())

    def test_deleteActor(self):
        self.assertEqual(second=deleteActor(1), first=ReturnValue.OK)
        self.assertEqual(second=deleteActor(0), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=deleteActor(-5), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=deleteActor(20), first=ReturnValue.NOT_EXISTS)

    def test_addStudio(self):
        self.assertEqual(second=addStudio(Studio(1, 's1')), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=addStudio(Studio(20, 's1')), first=ReturnValue.OK)
        self.assertEqual(second=addStudio(Studio(0, 's')), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=addStudio(Studio(-5, 's')), first=ReturnValue.BAD_PARAMS)

    def test_getStudioProfile(self):
        self.assertEqual(second=getStudioProfile(1), first=Studio(1, 's1'))
        self.assertEqual(second=getStudioProfile(20), first=Studio.badStudio())
        self.assertEqual(second=getStudioProfile(0), first=Studio.badStudio())
        self.assertEqual(second=getStudioProfile(-5), first=Studio.badStudio())

    def test_deleteStudio(self):
        self.assertEqual(second=deleteStudio(1), first=ReturnValue.OK)
        self.assertEqual(second=deleteStudio(0), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=deleteStudio(20), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=deleteStudio(-5), first=ReturnValue.NOT_EXISTS)

    def test_crticRatedMovie(self):
        self.assertEqual(second=criticRatedMovie('m1', 1991, 1, 2), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=criticRatedMovie('m1', 1990, 1, 2), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=criticRatedMovie('m1', 1991, 20, 2), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=criticRatedMovie('m1', 1991, 2, 2), first=ReturnValue.OK)
        self.assertEqual(second=criticRatedMovie('m1', 1991, 3, 6), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=criticRatedMovie('m1', 1991, 3, 0), first=ReturnValue.BAD_PARAMS)

    def test_CriticDidntRateMovie(self):
        self.assertEqual(second=criticDidntRateMovie('m1', 1991, 1), first=ReturnValue.OK)
        self.assertEqual(second=criticRatedMovie('m1', 1991, 1, 2), first=ReturnValue.OK)
        self.assertEqual(second=criticDidntRateMovie('m1', 1991, 2), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=criticDidntRateMovie('m2', 2000, 2), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=criticDidntRateMovie('m2', 1992, 20), first=ReturnValue.NOT_EXISTS)

    def test_actorPlayedInMovie(self):
        self.assertEqual(second=actorPlayedInMovie('m1', 1991, 1, 1000, ['r1']), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=actorPlayedInMovie('m1', 1991, 1, 10, ['r1']), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=actorPlayedInMovie('m1', 1991, 1, 1000, ['r2']), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=actorPlayedInMovie('m2', 1991, 1, 1000, ['r2']), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=actorPlayedInMovie('m1', 1991, 20, 1000, ['r2']), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=actorPlayedInMovie('m1', 1991, 2, 0, ['r2']), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=actorPlayedInMovie('m1', 1991, 2, -5, ['r2']), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=actorPlayedInMovie('m1', 1991, 2, 1000, []), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=actorPlayedInMovie('m1', 1991, 2, 1000, ['r', None, 'r2']),
                         first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=actorPlayedInMovie('m1', 1991, 2, 1000, [None]), first=ReturnValue.BAD_PARAMS)

    def test_actorDidntPlatInMovie(self):
        self.assertEqual(second=actorDidntPlayInMovie('m1', 1991, 1), first=ReturnValue.OK)
        self.assertEqual(second=actorPlayedInMovie('m1', 1991, 1, 1000, ['r1']), first=ReturnValue.OK)
        self.assertEqual(second=actorDidntPlayInMovie('m2', 1991, 1), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=actorDidntPlayInMovie('m2', 1992, 1), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=actorDidntPlayInMovie('m2', 1992, 20), first=ReturnValue.NOT_EXISTS)

    def test_getActorsRoleInMovie(self):
        self.assertEqual(second=getActorsRoleInMovie(1, 'm1', 1991), first=['r1'])
        self.assertEqual(second=getActorsRoleInMovie(2, 'm1', 1991), first=[])
        self.assertEqual(second=getActorsRoleInMovie(20, 'm1', 1991), first=[])
        self.assertEqual(second=getActorsRoleInMovie(2, 'm', 1991), first=[])
        self.assertEqual(second=getActorsRoleInMovie(2, 'm1', 1), first=[])
        actorPlayedInMovie('m1', 1991, 2, 100, ['Aba', 'Baba', 'Caba'])
        self.assertEqual(second=getActorsRoleInMovie(2, 'm1', 1991), first=['Caba', 'Baba', 'Aba'])

    def test_studioProducedMovie(self):
        self.assertEqual(second=studioProducedMovie(1, 'm1', 1991, 1100, 700), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=studioProducedMovie(1, 'm1', 1991, 1100, 500), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=studioProducedMovie(1, 'm1', 1991, 10, 700), first=ReturnValue.ALREADY_EXISTS)
        self.assertEqual(second=studioProducedMovie(2, 'm1', 1991, 1100, 700), first=ReturnValue.ALREADY_EXISTS)
        addMovie(Movie('m20', 2000, GENRES[0]))
        self.assertEqual(second=studioProducedMovie(20, 'm20', 2000, 100, 700), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=studioProducedMovie(2, 'm20', 2010, 100, 700), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=studioProducedMovie(2, 'm20', 2000, -1, 700), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=studioProducedMovie(2, 'm20', 2000, 1000, -700), first=ReturnValue.BAD_PARAMS)
        self.assertEqual(second=studioProducedMovie(2, 'm20', 2000, 0, 0), first=ReturnValue.OK)

    def test_studioDidntProducedMovie(self):
        self.assertEqual(second=studioDidntProduceMovie(1, 'm1', 1991), first=ReturnValue.OK)
        self.assertEqual(second=studioProducedMovie(1, 'm1', 1991, 1100, 700), first=ReturnValue.OK)
        self.assertEqual(second=studioDidntProduceMovie(2, 'm1', 1991), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=studioDidntProduceMovie(20, 'm1', 1991), first=ReturnValue.NOT_EXISTS)
        self.assertEqual(second=studioDidntProduceMovie(2, 'm', 1991), first=ReturnValue.NOT_EXISTS)

    def test_averageRating(self):
        self.assertEqual(second=averageRating('m20', 2000), first=0)
        addMovie(Movie('m20', 2000, GENRES[0]))
        self.assertEqual(second=averageRating('m20', 2000), first=0)
        criticRatedMovie('m20', 2000, 1, 1)
        self.assertEqual(second=averageRating('m20', 2000), first=1)
        criticRatedMovie('m20', 2000, 2, 2)
        self.assertEqual(second=averageRating('m20', 2000), first=1.5)
        criticRatedMovie('m20', 2000, 3, 3)
        self.assertEqual(second=averageRating('m20', 2000), first=2)

    def test_averageActorRating(self):
        self.assertEqual(second=averageActorRating(20), first=0)
        addActor(Actor(20, 'a20', 20, 200))
        self.assertEqual(second=averageActorRating(20), first=0)
        for j in range(1, 5):
            addMovie(Movie(f'm2{j}', 2000 + j, GENRES[0]))
            actorPlayedInMovie(f'm2{j}', 2000 + j, 20, 100, ['r'])
        self.assertEqual(second=averageActorRating(20), first=0)
        criticRatedMovie('m21', 2001, 1, 4)
        self.assertEqual(second=averageActorRating(20), first=1)
        criticRatedMovie('m21', 2001, 2, 4)
        self.assertEqual(second=averageActorRating(20), first=1)
        criticRatedMovie('m22', 2002, 1, 4)
        self.assertEqual(second=averageActorRating(20), first=2)
        criticRatedMovie('m21', 2001, 3, 5)
        self.assertEqual(
            second=round((averageActorRating(20)), 6), first=round(float((((4 * 2 + 5) / 3) + 4) / 4), 6))

    def test_bestPerformance(self):
        self.assertEqual(second=bestPerformance(20), first=Movie.badMovie())
        addActor(Actor(20, 'a20', 20, 200))
        self.assertEqual(second=bestPerformance(20), first=Movie.badMovie())
        for j in range(1, 4):
            addMovie(Movie(f'm2{j}', 2000 + j, GENRES[0]))
            actorPlayedInMovie(f'm2{j}', 2000 + j, 20, 100, ['r'])
        criticRatedMovie('m21', 2001, 1, 1)
        self.assertEqual(second=bestPerformance(20), first=Movie('m21', 2001, GENRES[0]))
        criticRatedMovie('m22', 2002, 1, 1)
        self.assertEqual(second=bestPerformance(20), first=Movie('m21', 2001, GENRES[0]))
        criticRatedMovie('m22', 2002, 2, 3)
        self.assertEqual(second=bestPerformance(20), first=Movie('m22', 2002, GENRES[0]))
        addMovie(Movie('z', 2002, GENRES[0]))
        actorPlayedInMovie('z', 2002, 20, 10, ['r'])
        criticRatedMovie('z', 2002, 1, 2)
        self.assertEqual(second=bestPerformance(20), first=Movie('z', 2002, GENRES[0]))
        actorDidntPlayInMovie('z', 2002, 20)
        self.assertEqual(second=bestPerformance(20), first=Movie('m22', 2002, GENRES[0]))

    def test_stageCrewBudget(self):
        self.assertEqual(second=stageCrewBudget('m20', 2000), first=-1)
        addMovie(Movie('m20', 2000, GENRES[0]))
        self.assertEqual(second=stageCrewBudget('m20', 2000), first=0)
        for j in range(1, 4):
            actorPlayedInMovie('m20', 2000, j, j * 10, ['r'])
        self.assertEqual(second=stageCrewBudget('m20', 2000), first=0 - (10 + 20 + 30))
        studioProducedMovie(1, 'm20', 2000, 100, 100)
        self.assertEqual(second=stageCrewBudget('m20', 2000), first=100 - (10 + 20 + 30))
        actorDidntPlayInMovie('m20', 2000, 1)
        self.assertEqual(second=stageCrewBudget('m20', 2000), first=100 - (20 + 30))

    def test_overlyInvestedInMovie(self):
        self.assertEqual(second=overlyInvestedInMovie('m20', 2000, 1), first=False)
        self.assertEqual(second=overlyInvestedInMovie('m1', 1991, 20), first=False)
        addMovie(Movie('m20', 2000, GENRES[0]))
        actorPlayedInMovie('m20', 2000, 1, 10, ['r1'])
        self.assertEqual(second=overlyInvestedInMovie('m20', 2000, 1), first=True)
        actorPlayedInMovie('m20', 2000, 2, 10, ['r2'])
        self.assertEqual(second=overlyInvestedInMovie('m20', 2000, 1), first=True)
        self.assertEqual(second=overlyInvestedInMovie('m20', 2000, 2), first=True)
        actorPlayedInMovie('m20', 2000, 3, 10, ['r3', 'r4', 'r5'])
        self.assertEqual(second=overlyInvestedInMovie('m20', 2000, 1), first=False)
        self.assertEqual(second=overlyInvestedInMovie('m20', 2000, 2), first=False)
        self.assertEqual(second=overlyInvestedInMovie('m20', 2000, 3), first=True)
        self.assertEqual(second=overlyInvestedInMovie('m20', 2000, 4), first=False)

    def test_frenchiseRevenue(self):
        result = [(f'm{i}', i * 700) for i in range(9, 0, -1)]
        self.assertEqual(second=franchiseRevenue(), first=result)
        addMovie(Movie('m1', 2000, GENRES[0]))
        studioProducedMovie(3, 'm1', 2000, 10, 3000)
        result[-1] = (result[-1][0], result[-1][1] + 3000)
        self.assertEqual(second=franchiseRevenue(), first=result)
        addMovie(Movie('m', 2000, GENRES[0]))
        result.append(('m', 0))
        self.assertEqual(second=franchiseRevenue(), first=result)

    def test_getFanCritics(self):
        result = [(i, i) for i in range(9, 0, -1)]
        self.assertEqual(second=getFanCritics(), first=result)
        criticRatedMovie('m2', 1992, 1, 1)
        result = result[:-1] + [(1, 2), (1, 1)]
        self.assertEqual(second=getFanCritics(), first=result)
        addMovie(Movie('m20', 2000, GENRES[0]))
        studioProducedMovie(1, 'm20', 2000, 10, 10)
        result = result[:-1]
        self.assertEqual(second=getFanCritics(), first=result)

    def test_averageAgeByGenre(self):
        result = [('Action', (sum([20 + 3 * i for i in [1, 5, 9]])) / 3),
                  ('Comedy', (sum([20 + 3 * i for i in [2, 6]])) / 2),
                  ('Drama', (sum([20 + 3 * i for i in [4, 8]])) / 2),
                  ('Horror', (sum([20 + 3 * i for i in [3, 7]])) / 2)]
        self.assertEqual(second=averageAgeByGenre(), first=result)
        # ['Drama', 'Action', 'Comedy', 'Horror']
        for i, genre in zip(range(1, 8), GENRES * 2):
            addMovie(Movie(f'movie{i}', 1900 + i, genre))
        for i in range(10, 16):
            addActor(Actor(i, f'actor{i}', i, 1))
        actorPlayedInMovie('movie1', 1901, 10, 1, ['r'])  # Drama, 10
        result[2] = ('Drama', round(float(((result[2][1] * 2) + 10) / 3), 6))
        self.assertEqual(second=[(g, round(a, 6)) for (g, a) in averageAgeByGenre()], first=result)
        actorPlayedInMovie('movie5', 1905, 10, 1, ['r'])  # should have no effect
        self.assertEqual(second=[(g, round(a, 6)) for (g, a) in averageAgeByGenre()], first=result)

    def test_getExclusiveActors(self):
        result = [(i, i) for i in range(9, 0, -1)]
        self.assertEqual(second=getExclusiveActors(), first=result)
        actorPlayedInMovie('m2', 1992, 1, 1, ['r'])
        result = result[:-1]
        self.assertEqual(second=getExclusiveActors(), first=result)
        addMovie(Movie('m20', 2000, GENRES[0]))
        studioProducedMovie(2, 'm20', 2000, 1, 1)
        self.assertEqual(second=getExclusiveActors(), first=result)
        actorPlayedInMovie('m20', 2000, 2, 1, ['r'])
        self.assertEqual(second=getExclusiveActors(), first=result)
        actorDidntPlayInMovie('m20', 2000, 2)
        actorDidntPlayInMovie('m2', 1992, 2)
        result = result[:-1]
        self.assertEqual(second=getExclusiveActors(), first=result)

    def tearDown(self) -> None:
        dropTables()


if __name__ == '__main__':
    unittest.main()
