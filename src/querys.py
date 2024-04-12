#Distribution of shows and movies on streaming platforms
def streamingType():
    query = """
    SELECT s.streaming_name,
       COUNT(CASE WHEN t.title_type = 'SHOW' THEN 1 END) AS series_count,
       COUNT(CASE WHEN t.title_type = 'MOVIE' THEN 1 END) AS movie_count
    FROM titles t
    INNER JOIN titles_streamings ts ON t.title_id = ts.title_id
    INNER JOIN streamings s ON ts.streaming_id = s.streaming_id
    GROUP BY s.streaming_name
    ORDER BY s.streaming_name;
    """
    return query

#Distribution of titles by streaming platform
def distributionStreamings():
    query = """
    SELECT s.streaming_name,
        COUNT(DISTINCT t.title_id) AS title_count,
        COUNT(DISTINCT t.title_id) / (SELECT COUNT(DISTINCT title_id) FROM Titles) AS multi_platform_ratio
    FROM titles t
    INNER JOIN titles_streamings ts ON t.title_id = ts.title_id
    INNER JOIN streamings s ON ts.streaming_id = s.streaming_id
    GROUP BY s.streaming_name;
    """
    return query

#Top 5 countries with the most titles
def countryTitles():
    query = """
    SELECT c.country_name, COUNT(t.title_id) AS title_count
    FROM titles t
    INNER JOIN titles_countries tc ON t.title_id = tc.title_id
    INNER JOIN countries c ON tc.country_id = c.country_id
    GROUP BY c.country_name
    ORDER BY title_count DESC
    LIMIT 5;
    """
    return query

#Number of actors who are also directors
def personActorDirector():
    query = """
    SELECT COUNT(DISTINCT tpr.person_id) AS actor_director_count
    FROM titles t
    INNER JOIN title_person tpr ON t.title_id = tpr.title_id
    INNER JOIN roles r1 ON tpr.role_id = r1.role_id
    INNER JOIN roles r2 ON tpr.role_id = r2.role_id
    INNER JOIN persons p ON tpr.person_id = p.person_id
    WHERE t.title_type = 'MOVIE'
    AND r1.role_name = 'ACTOR'
    AND r2.role_name = 'DIRECTOR'
    GROUP BY p.person_name;
    """
    return query

#Average runtime of movies and shows by streaming platform
def streamingRuntimeMovie():
    query = """
    SELECT s.streaming_name,
        AVG(t.title_runtime) AS total_movie_runtime
    FROM titles t
    INNER JOIN titles_streamings ts ON t.title_id = ts.title_id
    INNER JOIN streamings s ON ts.streaming_id = s.streaming_id
    WHERE t.title_type = 'MOVIE'
    GROUP BY s.streaming_name;
    """
    return query

#Average runtime of movies and shows by streaming platform
def streamingRuntimeShow():
    query = """
    SELECT s.streaming_name,
        AVG(t.title_runtime) AS total_show_runtime
    FROM titles t
    INNER JOIN titles_streamings ts ON t.title_id = ts.title_id
    INNER JOIN streamings s ON ts.streaming_id = s.streaming_id
    WHERE t.title_type = 'SHOW'
    GROUP BY s.streaming_name;
    """
    return query

#Ranking of the most popular streaming service
def streamingMostValue():
    query = """
    SELECT s.streaming_name,
       AVG(COALESCE(t.title_imdb_score, 0)) AS avg_imdb_score,
       AVG(COALESCE(t.title_tmdb_score, 0)) AS avg_tmdb_score
    FROM titles t
    INNER JOIN titles_streamings ts ON t.title_id = ts.title_id
    INNER JOIN streamings s ON ts.streaming_id = s.streaming_id
    GROUP BY s.streaming_name;
    """
    return query

#Best movie by decade
def bestMovieByDecade():
    query = """
    SELECT t.decade,
           t.title,
           t.avg_total_score
    FROM (
        SELECT title,
               FLOOR(title_release_year / 10) * 10 AS decade,
               AVG(COALESCE(title_imdb_score, 0)) AS avg_imdb_score,
               AVG(COALESCE(title_tmdb_score, 0)) AS avg_tmdb_score,
               AVG(COALESCE(title_imdb_score, 0) + COALESCE(title_tmdb_score, 0)) AS avg_total_score,
               ROW_NUMBER() OVER (PARTITION BY FLOOR(title_release_year / 10) * 10 ORDER BY AVG(COALESCE(title_imdb_score, 0) + COALESCE(title_tmdb_score, 0)) DESC) AS rn
        FROM titles
        WHERE title_type = 'MOVIE'
        GROUP BY title, FLOOR(title_release_year / 10) * 10
    ) t
    WHERE t.rn = 1
    ORDER BY t.decade;
    """
    return query

#Best movie by decade
def bestDecade():
    query = """
    SELECT t.decade,
           AVG(t.avg_total_score) AS avg_total_score
    FROM (
        SELECT FLOOR(title_release_year / 10) * 10 AS decade,
               AVG(COALESCE(title_imdb_score, 0) + COALESCE(title_tmdb_score, 0)) AS avg_total_score
        FROM titles
        WHERE title_type = 'MOVIE'
        GROUP BY FLOOR(title_release_year / 10) * 10
    ) t
    GROUP BY t.decade
    ORDER BY t.decade DESC;
    """
    return query

#Ranking of the most popular genre titles by streaming service
def genreStreaming():
    query = """
    SELECT
        s.streaming_name,
        g.genre_name AS most_used_genre,
        COUNT(*) AS genre_count
    FROM
        titles_streamings ts
    JOIN
        titles t ON ts.title_id = t.title_id
    JOIN
        titles_genres tg ON t.title_id = tg.title_id
    JOIN
        genres g ON tg.genre_id = g.genre_id
    JOIN
        streamings s ON ts.streaming_id = s.streaming_id
    GROUP BY
        s.streaming_name,
        g.genre_name
    HAVING
        COUNT(*) = (
            SELECT MAX(genre_count)
            FROM (
                SELECT
                    s2.streaming_name,
                    g2.genre_name AS most_used_genre,
                    COUNT(*) AS genre_count
                FROM
                    titles_streamings ts2
                JOIN
                    titles t2 ON ts2.title_id = t2.title_id
                JOIN
                    titles_genres tg2 ON t2.title_id = tg2.title_id
                JOIN
                    genres g2 ON tg2.genre_id = g2.genre_id
                JOIN
                    streamings s2 ON ts2.streaming_id = s2.streaming_id
                WHERE
                    s2.streaming_name = s.streaming_name
                GROUP BY
                    s2.streaming_name,
                    g2.genre_name
                ORDER BY
                    COUNT(*) DESC
                LIMIT 1
            ) AS subquery
        );
    """
    return query

#Distribution of genres by streaming service
def distributionGenreStreaming():
    query = """
    SELECT
        s.streaming_name,
        g.genre_name AS most_used_genre,
        COUNT(*) / total_titles.total_titles_count * 100 AS genre_percentage
    FROM
        titles_streamings ts
    JOIN
        titles t ON ts.title_id = t.title_id
    JOIN
        titles_genres tg ON t.title_id = tg.title_id
    JOIN
        genres g ON tg.genre_id = g.genre_id
    JOIN
        streamings s ON ts.streaming_id = s.streaming_id
    JOIN
        (
            SELECT
                ts.streaming_id,
                COUNT(*) AS total_titles_count
            FROM
                titles_streamings ts
            GROUP BY
                ts.streaming_id
        ) AS total_titles ON s.streaming_id = total_titles.streaming_id
    GROUP BY
        s.streaming_name,
        g.genre_name
    ORDER BY s.streaming_name;
    """
    return query

def scorePopularity():
    query = """
    SELECT title, title_tmdb_popularity, title_tmdb_score
    FROM titles;
    """
    return query

def scoreRuntime():
    query = """
    SELECT 
        title, 
        title_runtime, 
        AVG((title_imdb_score + title_tmdb_score) / 2) AS avg_score
    FROM 
        titles
    GROUP BY 
        title, 
        title_runtime;
    """
    return query

def scoreYear():
    query = """
    SELECT 
        title, 
        title_release_year, 
        AVG((title_imdb_score + title_tmdb_score) / 2) AS avg_score
    FROM 
        titles
    GROUP BY 
        title, 
        title_release_year;
    """
    return query

def correlacionScores():
    query = """
    SELECT 
        title_imdb_score, 
        title_tmdb_score
    FROM 
        titles;
    """
    return query

def genreScore():
    query = """
    SELECT
        g.genre_name,
        AVG((t.title_imdb_score + t.title_tmdb_score) / 2.0) AS avg_rating
    FROM
        titles t
    JOIN
        titles_genres tg ON t.title_id = tg.title_id
    JOIN
        genres g ON tg.genre_id = g.genre_id
    GROUP BY
        g.genre_name
    ORDER BY
        avg_rating DESC
    LIMIT 5;
    """
    return query

def genreRestricted():
    query = """
    SELECT g.genre_name, COUNT(t.title_id) AS restricted_titles_count
    FROM titles t
    JOIN titles_genres tg ON t.title_id = tg.title_id
    JOIN genres g ON tg.genre_id = g.genre_id
    JOIN titles_ages ta ON t.title_id = ta.title_id
    JOIN ages a ON ta.age_id = a.age_id
    WHERE a.age_name IN ('NC-17', 'TV-MA')
    GROUP BY g.genre_name
    ORDER BY restricted_titles_count DESC
    LIMIT 5;
    """
    return query

def countryShows():
    query = """
    SELECT 
        c.country_name,
        COUNT(CASE WHEN t.title_type = 'SHOW' THEN 1 END) AS series_count,
        COUNT(CASE WHEN t.title_type = 'MOVIE' THEN 1 END) AS movie_count
    FROM 
        titles t
    JOIN 
        titles_countries tc ON t.title_id = tc.title_id
    JOIN 
        countries c ON tc.country_id = c.country_id
    GROUP BY 
        c.country_name
    HAVING 
        series_count > movie_count
    ORDER BY 
        series_count - movie_count DESC
    LIMIT 5;
    """
    return query

def countryMovies():
    query = """
    SELECT 
        c.country_name,
        COUNT(CASE WHEN t.title_type = 'MOVIE' THEN 1 END) AS movie_count,
        COUNT(CASE WHEN t.title_type = 'SHOW' THEN 1 END) AS series_count
    FROM 
        titles t
    JOIN 
        titles_countries tc ON t.title_id = tc.title_id
    JOIN 
        countries c ON tc.country_id = c.country_id
    GROUP BY 
        c.country_name
    HAVING 
        movie_count > series_count
    ORDER BY 
        movie_count - series_count DESC
    LIMIT 5;
    """
    return query

def streamingCountry():
    query = """
    SELECT 
        s.streaming_name,
        COUNT(DISTINCT c.country_id) AS country_count
    FROM 
        streamings s
    JOIN 
        titles_streamings ts ON s.streaming_id = ts.streaming_id
    JOIN 
        titles_countries tc ON ts.title_id = tc.title_id
    JOIN 
        countries c ON tc.country_id = c.country_id
    GROUP BY 
        s.streaming_name
    ORDER BY 
        s.streaming_name;
    """
    return query

def genreYear():
    query = """
    SELECT 
        tg.genre_id,
        g.genre_name,
        t.title_release_year,
        COUNT(*) AS title_count
    FROM 
        titles t
    JOIN 
        titles_genres tg ON t.title_id = tg.title_id
    JOIN 
        genres g ON tg.genre_id = g.genre_id
    GROUP BY 
        tg.genre_id, g.genre_name, t.title_release_year
    ORDER BY 
        tg.genre_id, t.title_release_year;
    """
    return query