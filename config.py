from datetime import datetime

current_data = datetime.today().strftime('%Y-%m-%d')

REVIEW_DATABASE_NAME = "review.db"
REVIEW_DATABASE_BACKUP_NAME = 'review_' + current_data + '.db'
