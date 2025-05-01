import json
import dotenv
import psycopg2
import os
dotenv.load_dotenv()

def get_db_con():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host="localhost",
        port=os.getenv('DB_PORT')
    )
    return conn

def insert_article(cur, topic, content):
    cur.execute("""
        INSERT INTO articles (topic, content)
        VALUES (%s, %s)
        RETURNING id;
    """, (topic, content))
    return cur.fetchone()[0]

def insert_question(cur, question_id, article_id, question, answers, is_impossible):
    answers_json = json.dumps(answers) if answers else json.dumps([])
    cur.execute("""
        INSERT INTO questions (id, article_id, question, answers, is_impossible)
        VALUES (%s, %s, %s, %s, %s);
    """, (question_id, article_id, question, answers_json, is_impossible))

def get_all_content(cur):
    cur.execute("SELECT id, content FROM articles;")
    result=cur.fetchall()
    content_ids=[row[0] for row in result]
    content= [row[1] for row in result]
    return content_ids, content
