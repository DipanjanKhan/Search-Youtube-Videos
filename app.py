from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import videoSearch

load_dotenv('.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class RecentSearch(db.Model):
    slno = db.Column(db.Integer, primary_key = True)
    searchName = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

@app.route('/')
def youtubeVideoFinder():
    allRecentSearch = list(reversed(RecentSearch.query.all()))
    return render_template('index.html', allRecentSearch = allRecentSearch)

@app.route('/', methods = ['GET', 'POST'])
def searchVideos():
    if request.method == 'POST' and request.form['search'] != '':
        searchName = request.form['search']
        recentSearch = RecentSearch(searchName = searchName)
        db.session.add(recentSearch)
        db.session.commit()
        channelId = videoSearch.findChannelId(searchName)

        if channelId == 'Not found':
            return render_template('/notfound.html')
        
        videoDetails = videoSearch.findLatestVideos(channelId)

    return render_template('show.html', videoDetails = videoDetails)

@app.route('/delete/<slno>')
def delete(slno):
    details = RecentSearch.query.get(slno)
    db.session.delete(details)
    db.session.commit()
    return redirect('/')

@app.route('/search/<searchName>')
def search(searchName):
    recentSearch = RecentSearch(searchName = searchName)
    db.session.add(recentSearch)
    db.session.commit()
    channelId = videoSearch.findChannelId(searchName)

    if channelId == 'Not found':
        return render_template('/notfound.html')
    
    videoDetails = videoSearch.findLatestVideos(channelId)
    return render_template('show.html', videoDetails = videoDetails)

if __name__ == '__main__':

    app.run()