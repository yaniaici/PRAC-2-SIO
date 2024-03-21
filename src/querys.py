#Ranking of the most popular Action titles by streaming service
def streamingAction():
    query = """
    SELECT streaming_name, COUNT(*) AS action_count
    FROM titles t
    INNER JOIN titles_genres tg ON t.title_id = tg.title_id
    INNER JOIN genres g ON tg.genre_id = g.genre_id
    INNER JOIN titles_streamings ts ON t.title_id = ts.title_id
    INNER JOIN streamings s ON ts.streaming_id = s.streaming_id
    WHERE g.genre_name = "action"
    GROUP BY streaming_name
    ORDER BY action_count DESC;
    """
    return query

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

def topActors():
    query = """
    SELECT p.person_name, COUNT(t.title_id) AS title_count
    FROM persons p
    INNER JOIN title_person tpr ON p.person_id = tpr.person_id
    INNER JOIN titles t ON tpr.title_id = t.title_id
    GROUP BY p.person_id, p.person_name
    ORDER BY title_count DESC
    LIMIT 10;
    """
    return query