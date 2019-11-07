import datetime
import json
import re

from monolith.database import db, Story, Like, Dislike, retrieve_themes, retrieve_dice_set, is_date, Follow, get_suggested_stories
from monolith.background import async_like, async_dislike, async_remove_like, async_remove_dislike
from monolith.auth import admin_required, current_user
from monolith.classes.DiceSet import _throw_to_faces

from flask import Blueprint, redirect, render_template, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.sql.expression import func

stories = Blueprint('stories', __name__)

@stories.route('/', methods=['GET'])
def _myhome(message=''):
    if current_user.is_anonymous:
        return redirect("/login", code=302)
    followingStories= (db.session.query(Story).join(Follow, Story.author_id == Follow.user_id)
                                             .filter(Follow.followed_by_id == current_user.id)
                                             .filter(Story.published==1)
                                             .order_by(Story.date.desc())
                                             .all())
    suggestedStories=get_suggested_stories(current_user.id)
    return render_template("home.html", message=message, followingstories=followingStories, suggestedstories=suggestedStories)

@stories.route('/explore', methods=['GET', 'POST'])
def _stories(message=''):
    if current_user.is_anonymous:
        return redirect("/login", code=302)

    allstories = db.session.query(Story).filter_by(published=1).order_by(Story.date.desc())
    if request.method == 'POST':
        beginDate = request.form["beginDate"]
        if beginDate == "" or not is_date(beginDate):
            beginDate = str(datetime.date.min)

        endDate = request.form["endDate"]
        if endDate == "" or not is_date(endDate):
            endDate = str(datetime.date.max)

        filteredStories = allstories.filter(Story.date.between(beginDate, endDate))
        return render_template("explore.html", message="Filtered stories", stories=filteredStories, url="/story/")
    else:
        return render_template("explore.html", message=message, stories=allstories)

@stories.route('/story/<int:story_id>')
@login_required
def _story(story_id, message=''):
    story = Story.query.filter_by(id=story_id).filter_by(published=1).first()
    if story is None:
        message = 'Ooops.. Story not found!'
        return render_template("message.html", message=message)

    rolls_outcome = json.loads(story.rolls_outcome)
    return render_template("story.html", message=message, story=story,
                           url="/story/", current_user=current_user, rolls_outcome=rolls_outcome)

@stories.route('/story/<story_id>/delete')
@login_required
def _delete_story(story_id):
    story = Story.query.filter_by(id=story_id).filter_by(published=1)
    if story.first() is None:
        abort(404)

    if story.first().author_id != current_user.id:
        abort(401)
    else:
        story.delete()
        db.session.commit()
        message = 'Story sucessfully deleted'
    return render_template("message.html", message=message)

@stories.route('/random_story')
@login_required
def _random_story(message=''):
    story = Story.query.filter(Story.author_id != current_user.id).filter_by(published=1).order_by(func.random()).first()
    if story is None:
        message = 'Ooops.. No random story for you!'
        rolls_outcome = []
    else:
        rolls_outcome = json.loads(story.rolls_outcome)
    return render_template("story.html", message=message, story=story,
                           url="/story/", current_user=current_user, rolls_outcome=rolls_outcome)

@stories.route('/story/<int:story_id>/like')
@login_required
def _like(story_id):
    story = Story.query.filter_by(id=story_id).filter_by(published=1).first()
    if story is None:
        abort(404)
    
    q = Like.query.filter_by(liker_id=current_user.id, story_id=story_id)
    if q.first() is None:
        new_like = Like()
        new_like.liker_id = current_user.id
        new_like.story_id = story_id
        # remove dislike, if present
        d = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id).first()
        if d is not None: 
            db.session.delete(d)
            async_like.delay(story_id, True)
        else:
            async_like.delay(story_id)
        db.session.add(new_like)
        db.session.commit()
        message = 'Like added!'
    else:
        message = 'You\'ve already liked this story!'
    return _story(story_id, message)

@stories.route('/story/<int:story_id>/dislike')
@login_required
def _dislike(story_id):
    story = Story.query.filter_by(id=story_id).filter_by(published=1).first()
    if story is None:
        abort(404)

    q = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id)
    if q.first() is None:
        new_dislike = Dislike()
        new_dislike.disliker_id = current_user.id
        new_dislike.story_id = story_id
        # remove like, if present
        l = Like.query.filter_by(liker_id=current_user.id, story_id=story_id).first()
        if l is not None:
            db.session.delete(l)
            async_dislike.delay(story_id, True)
        else:
            async_dislike.delay(story_id)
        db.session.add(new_dislike)
        db.session.commit()
        message = 'Dislike added!'
    else:
        message = 'You\'ve already disliked this story!'
    return _story(story_id, message)

@stories.route('/story/<int:story_id>/remove_like')
@login_required
def _remove_like(story_id):
    story = Story.query.filter_by(id=story_id).first()
    if story is None:
        abort(404)
    
    l = Like.query.filter_by(liker_id=current_user.id, story_id=story_id).first()
    if l is None:
        message = 'You have to like it first!'
    else:
        async_remove_like.delay(story_id)
        db.session.delete(l)
        db.session.commit()
        message = 'You removed your like'
    return _story(story_id, message)
    
    
@stories.route('/story/<int:story_id>/remove_dislike')
@login_required
def _remove_dislike(story_id):
    story = Story.query.filter_by(id=story_id).first()
    if story is None:
        abort(404)
    
    d = Dislike.query.filter_by(disliker_id=current_user.id, story_id=story_id).first()
    if d is None:
        message = 'You didn\'t dislike it yet..'
    else:
        async_remove_dislike.delay(story_id)
        db.session.delete(d)
        db.session.commit()
        message = 'You removed your dislike!'
    return _story(story_id, message)

# Function to be called during story publishing.
# If it return False, stop publishing and return an error message.
def is_story_valid(story_text, dice_roll):
    split_story_text = re.findall(r"[\w']+|[.,!?;]", story_text.lower())
    for word in dice_roll:
        if word.lower() not in split_story_text:
            return False
    return True

@stories.route('/stories/new_story', methods=['GET', 'POST'])
@login_required
def new_stories():
    if request.method == 'GET':
        dice_themes = retrieve_themes()
        return render_template("new_story.html", themes=dice_themes)
    else:
        stry = Story.query.filter(Story.author_id == current_user.id).filter(
            Story.published == 0).filter(Story.theme == request.form["theme"]).first()
        if stry != None:
            return redirect("../write_story/"+str(stry.id), code=302)

        dice_set = retrieve_dice_set(request.form["theme"])
        face_set = dice_set.throw()[:int(request.form["dice_number"])]
        new_story = Story()
        new_story.author_id = current_user.id
        new_story.theme = request.form["theme"]
        new_story.rolls_outcome = json.dumps(face_set)
        db.session.add(new_story)
        db.session.flush()
        db.session.commit()
        db.session.refresh(new_story)
        return redirect('/write_story/'+str(new_story.id), code=302)

@stories.route('/write_story/<story_id>', methods=['POST', 'GET'])
@login_required
def write_story(story_id):
    story = Story.query.filter_by(id=story_id).filter_by(published=0).first()
    if story is None:
        abort(404)

    if current_user.id != story.author_id:
        abort(401)

    rolls_outcome = json.loads(story.rolls_outcome)
    faces = _throw_to_faces(rolls_outcome)

    if request.method == 'POST':
        story.text = request.form["text"]
        story.title = request.form["title"]
        story.published = 1 if request.form["store_story"] == "1" else 0

        if story.published and story.title == "":
            db.session.rollback()
            message = "You must complete the title in order to publish the story"
            return render_template("/write_story.html", theme=story.theme, outcome=story.rolls_outcome,
                                   title=story.title, text=story.text, message=message)

        if story.published and not is_story_valid(story.text, faces):
            db.session.rollback()
            message = "You must use all the words of the outcome!"
            return render_template("/write_story.html", theme=story.theme, outcome=rolls_outcome, title=story.title, text=story.text, message=message)
        
        if story.published == 0 and (story.title == "None" or len(story.title.replace(" ", ""))==0):
            story.title="Draft("+str(story.theme)+")" 
        db.session.commit()

        if story.published == 1:
            return redirect("../story/"+str(story.id), code=302)
        elif story.published == 0:
            return redirect("../", code=302)

    return render_template("/write_story.html", theme=story.theme, outcome=rolls_outcome, title=story.title, text=story.text, message="")
