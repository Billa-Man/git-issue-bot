import psycopg2
from psycopg2 import OperationalError
import requests
import streamlit as st
from settings import settings

#---------- CONNECT DATABASE ----------
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password=settings.POSTGRES_PASSWORD,
            host="db",
            port=5432
        )
        return conn
    except OperationalError as e:
        print(f"Error: Unable to connect to the database. Details: {e}")
        return None

#---------- TOP REPOS ----------
def get_top_repositories(language_filter="All"):
    github_api_url = "https://api.github.com/search/repositories"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": settings.GITHUB_API_TOKEN
    }

    params = {
        "q": "stars:>1",
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
    }

    if language_filter != "All":
        params["q"] += f" language:{language_filter}"

    all_repositories = []
    
    for page in range(1, 11):
        params["page"] = page
        response = requests.get(github_api_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            repositories = data.get("items", [])
            all_repositories.extend(repositories)

            if len(repositories) < 100:
                break
        else:
            st.error(f"Failed to fetch data: {response.status_code} {response.text}")
            break

    return all_repositories

#---------- RETRIEVE, ADD & DELETE REPOS ----------
def add_bookmark_to_db(repo_name, user_id=None):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO bookmarkedrepositories (repo_name, user_id) VALUES (%s, %s)",
            (repo_name, user_id)
        )
    conn.commit()


def get_bookmarked_repos_from_db(user_id=None):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        if user_id:
            cursor.execute("SELECT repo_name FROM bookmarkedrepositories WHERE user_id = %s ORDER BY timestamp DESC", (user_id,))
        else:
            cursor.execute("SELECT repo_name FROM bookmarkedrepositories ORDER BY timestamp DESC")
        rows = cursor.fetchall()
    return [row[0] for row in rows]


def delete_bookmark_from_db(repo_name, user_id=None):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM bookmarkedrepositories WHERE repo_name = %s AND user_id = %s", (repo_name, user_id))
    conn.commit()