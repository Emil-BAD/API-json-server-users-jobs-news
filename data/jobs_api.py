import flask
from flask import request, jsonify

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {'jobs': [item.to_dict(
            only=('id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished', 'team_leader'))
            for item in jobs]})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify({'jobs': job.to_dict(
        only=('id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished', 'team_leader'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    id_jobs = list([i.id for i in jobs])
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'work_size', 'collaborators', 'is_finished', 'team_leader']):
        return jsonify({'error': 'Bad request'})
    for i in id_jobs:
        if int(i) == int(request.json['id']):
            return jsonify({'error': 'Id already exists'})

    jobs = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        team_leader=request.json['team_leader']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_news(jobs_id):
    db_sess = db_session.create_session()
    id_jobs = db_sess.query(Jobs).get(jobs_id)
    if not id_jobs:
        return jsonify({'error': 'Not found'})
    elif not all(key in request.json for key in
                 ['job', 'work_size', 'collaborators', 'is_finished', 'team_leader']):
        return jsonify({'error': 'Bad request'})
    for job_ed in db_sess.query(Jobs).filter(Jobs.id == jobs_id):
        job_ed.job = request.json['job']
        job_ed.work_size = request.json['work_size']
        job_ed.collaborators = request.json['collaborators']
        job_ed.is_finished = request.json['is_finished']
        job_ed.team_leader = request.json['team_leader']
    db_sess.commit()
    return jsonify({'success': 'OK'})
