import os
import sys
from flask_frozen import Freezer
from app import app, recommender, get_dummy_recommendations, get_trending_songs, get_new_releases, get_sample_artists

# Configure app for freezing
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

# Create the freezer
freezer = Freezer(app)

# Register dynamic routes
@freezer.register_generator
def song_detail():
    if recommender:
        for song_key in list(recommender.song_index_mapping.keys())[:100]:  # Limit to 100 songs
            yield {'song_key': song_key}
    else:
        # If no recommender, provide some sample song keys
        dummy_recs = get_dummy_recommendations(8)
        for song in dummy_recs:
            yield {'song_key': song['song_key']}
    
@freezer.register_generator
def artist_page():
    if recommender:
        for artist in recommender.song_data['artist'].unique()[:30]:  # Limit to 30 artists
            yield {'artist_name': artist}
    else:
        # If no recommender, provide some sample artists
        artists = ['The Beatles', 'Queen', 'Michael Jackson', 'Led Zeppelin', 'Pink Floyd']
        for artist in artists:
            yield {'artist_name': artist}
            
@freezer.register_generator
def api_recommendations():
    for user_id in range(1, 6):  # Generate for 5 dummy users
        yield {'user_id': user_id}

@freezer.register_generator
def switch_user():
    for user_id in range(1, 6):  # Generate for 5 dummy users
        yield {'user_id': user_id}

if __name__ == '__main__':
    # Create static folder if it doesn't exist
    if not os.path.exists('build'):
        os.makedirs('build')
        
    # Create build path for static assets
    if not os.path.exists('build/static'):
        os.makedirs('build/static/css')
        os.makedirs('build/static/js')
        os.makedirs('build/static/img')
        
    # Copy static files (if they exist)
    if os.path.exists('static'):
        os.system('cp -r static/* build/static/')
    
    # Freeze the app
    print("Freezing Flask app...")
    freezer.freeze()
    print("Flask app frozen successfully!")
    
    # Create a simple index.html if it doesn't exist
    if not os.path.exists('build/index.html'):
        print("Creating fallback index.html...")
        with open('build/index.html', 'w') as f:
            f.write("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Spotify Music Recommender</title>
                <meta http-equiv="refresh" content="0;url=/" />
            </head>
            <body>
                <p>Redirecting to the home page...</p>
            </body>
            </html>
            """)
    
    print("Build completed successfully!") 