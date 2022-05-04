from flask import request, Blueprint, jsonify, make_response

from data.jobs import Job
from data.users import User
from data import db_session


api = Blueprint('api', __name__, url_prefix='/api')


@api.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@api.get('/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'title', 'team_leader_id', 'work_size', 'collaborators', 'is_finished', 'user_created.name'))
                 for item in jobs]
        }
    )


@api.get('/jobs/<int:id>')
def get_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == id).first()
    if job:
        return jsonify(
            {f'job {id}': job.to_dict(only=('title', 'team_leader_id', 'work_size', 'collaborators', 'is_finished', 'user_created.name'))}
        )
    return jsonify({'job': f'Job with id={id} not found'})


@api.post('/jobs')
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['id', 'title', 'team_leader_id', 'work_size', 'collaborators', 'is_finished', 'user_created']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(Job).filter(Job.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    job = Job(
        id=request.json['id'],
        title=request.json['title'],
        team_leader_id=request.json['team_leader_id'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        user_created=request.json['user_created']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@api.delete('/jobs/<int:id>')
def delete_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).get(id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@api.put('/jobs/<int:id>')
def edit_job(id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title', 'team_leader_id', 'work_size', 'collaborators', 'is_finished', 'user_created']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Job).get(id)
    if not job:
        return jsonify({'error': 'Id not exists'})
    job.title = request.json['title']
    job.team_leader_id = request.json['team_leader_id']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']
    job.user_created = request.json['user_created']
    db_sess.commit()
    return jsonify({'success': 'OK'})


@api.get('/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'about', 'email', 'created_date'))
                 for item in users]
        }
    )


@api.get('/users/<int:id>')
def get_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        return jsonify(
            {f'User {id}': user.to_dict(only=('name', 'about', 'email', 'created_date'))}
        )
    return jsonify({'user': f'User with id={id} not found'})


@api.post('/users')
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['id', 'name', 'about', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        name=request.json['name'],
        about=request.json['about'],
        email=request.json['email'],
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@api.put('/users/<int:id>')
def edit_user(id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['name', 'about', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    if not user:
        return jsonify({'error': 'Id not exists'})
    user.name = request.json['name']
    user.about = request.json['about']
    user.email = request.json['email']
    user.set_password(request.json['password'])
    db_sess.commit()
    return jsonify({'success': 'OK'})


@api.delete('/users/<int:id>')
def delete_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})