import os

# Password: Bootcamp#2025
# Encoded # as %23
content = [
    'DATABASE_URL=mysql+aiomysql://jinwoo:Bootcamp%232025@34.136.215.22:3306/quote_collection',
    'SYNC_DATABASE_URL=mysql+pymysql://jinwoo:Bootcamp%232025@34.136.215.22:3306/quote_collection',
    'GOOGLE_PROJECT_ID=gen-lang-client-0121173096',
    'GOOGLE_LOCATION=us-central1',
    'GOOGLE_APPLICATION_CREDENTIALS="C:\\quote_collection\\gcloud\\gen-lang-client-0121173096-c6cf40e73952.json"',
    'ALADIN_API_KEY=ttbygomania1045001',
    'SECRET_KEY=temporary-for-dev',
    'ALGORITHM=HS256',
    'ACCESS_TOKEN_EXPIRE_MINUTES=30'
]

with open('c:/quote_collection/.env', 'w', encoding='utf-8') as f:
    f.write('\n'.join(content) + '\n')

print("Successfully updated .env with Bootcamp#2025")
