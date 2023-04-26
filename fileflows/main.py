#!/usr/bin/python3

import sys
from fileflows import apps


if __name__ == '__main__':
    file_path: str = sys.argv[1]
    
    try:
        app = apps.Sonarr(item_path=file_path)
        body: str = f"{app.series_name} - S{app.season_number:02d}E{app.episode_number:02d}"
    except TypeError as e:
        app = apps.Radarr(item_path=file_path)
        body = f"{app.movie_name} ({app.movie_year})"
        
    app.notify(
        title="FileFlows - Standardize Audio",
        body=f"{body}",
        image=app.poster_image
    )
    
