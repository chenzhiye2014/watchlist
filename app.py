import os
import click

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)    # 初始化扩展，传入程序实例 app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()
def forge():
    db.create_all()

    name = 'Chen Zhetao'
    movies = [
        {'title': '龙猫', 'year': '1988'},
        {'title': '死亡诗社', 'year': '1989'},
        {'title': '美丽新世界', 'year': '1993'},
        {'title': '这个杀手不太冷', 'year': '1994'},
        {'title': '麻将', 'year': '1996'},
        {'title': '燕尾蝶', 'year': '1996'},
        {'title': '喜剧之王', 'year': '1999'},
        {'title': '鬼子来了', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': '麦兜', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done')


@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)
