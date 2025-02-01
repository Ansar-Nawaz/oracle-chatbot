import psycopg2

def log_feedback(error_code: str, is_helpful: bool):
    conn = psycopg2.connect(os.getenv("DB_URL"))
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO feedback (error_code, upvotes, downvotes)
        VALUES (%s, %s, %s)
        ON CONFLICT (error_code) DO UPDATE
        SET upvotes = feedback.upvotes + EXCLUDED.upvotes,
            downvotes = feedback.downvotes + EXCLUDED.downvotes
    """, (error_code, 1 if is_helpful else 0, 0 if is_helpful else 1))
    conn.commit()
    cur.close()
