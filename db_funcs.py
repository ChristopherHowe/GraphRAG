import json


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
    cur.execute("SELECT content FROM articles;")
    return [row[0] for row in cur.fetchall()]
