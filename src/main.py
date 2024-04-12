import connection
import querys
import matplotlib.pyplot as plt

cursor = connection.connection.cursor()

streamingType = querys.streamingType()
distribuitonStreaming = querys.distributionStreamings()
countryTitles = querys.countryTitles()
personActorDirector = querys.personActorDirector()
streamingRuntimeMovie = querys.streamingRuntimeMovie()
streamingRuntimeShow = querys.streamingRuntimeShow()
streamingValues = querys.streamingMostValue()
bestMovieDecade = querys.bestMovieByDecade()
bestDecade = querys.bestDecade()
distributionGenreStreaming = querys.distributionGenreStreaming()
scorePopularity = querys.scorePopularity()
scoreRuntime = querys.scoreRuntime()
scoreYear = querys.scoreYear()
correlacionScores = querys.correlacionScores()
genreScore = querys.genreScore()
genreRestriction = querys.genreRestricted()
countryShows = querys.countryShows()
countryMovies = querys.countryMovies()
streamingCountry = querys.streamingCountry()
genreYear = querys.genreYear()

cursor.execute(distributionGenreStreaming)
results = cursor.fetchall()

for row in results:
    #print(row)
    x = [row[0] for row in results]
    y = [row[1] for row in results]
    z_decimal = [row[2] for row in results]
    z = [float(i) for i in z_decimal]

cursor.execute(genreYear)
results = cursor.fetchall()

for row in results:
    #print(row)
    x = [row[1] for row in results]
    y = [row[2] for row in results]
    z = [row[3] for row in results]

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, z)
ax.set_xlabel('Year')
ax.set_ylabel('Genre')
ax.set_title('Distribution of genres by year')
plt.show()




