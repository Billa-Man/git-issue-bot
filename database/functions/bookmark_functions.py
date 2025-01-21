from database.functions.connect_database import get_db_connection

#---------- RETRIEVE, ADD & DELETE REPOS ----------
def add_bookmark_to_db(type, website):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            if type == "issue":
                query = "INSERT INTO bookmarkedissues (website) VALUES (%s) ON CONFLICT (website) DO NOTHING"
            elif type == "repository":
                query = "INSERT INTO bookmarkedrepositories (website) VALUES (%s) ON CONFLICT (website) DO NOTHING"
            cursor.execute(query, (website,))
        conn.commit()


def get_bookmarks_from_db(type):
    conn = get_db_connection()

    with conn.cursor() as cursor:
        if type == "issue":
            query = "SELECT website FROM bookmarkedissues ORDER BY timestamp DESC"
        elif type == "repository":
            query =  "SELECT website FROM bookmarkedrepositories ORDER BY timestamp DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
    return [row[0] for row in rows]


def delete_bookmark_from_db(type, website):
    conn = get_db_connection()

    with conn.cursor() as cursor:
        if type == "issue":
            query = "DELETE FROM bookmarkedissues WHERE website = %s"
        elif type == "repository":
            query = "DELETE FROM bookmarkedrepositories WHERE website = %s"
        cursor.execute(query, (website,))
    conn.commit()