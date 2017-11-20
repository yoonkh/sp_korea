from .. import db

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('video_tags.id'), primary_key=True),
                db.Column('video_id', db.Integer, db.ForeignKey('videos.id'), primary_key=True)
                )


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    running_time = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    company = db.Column(db.String(32))
    description = db.Column(db.Text())
    link = db.Column(db.String())
    tags = db.relationship('VideoTag', secondary=tags, lazy='subquery',
                           backref=db.backref('videos', lazy=True))


class VideoTag(db.Model):
    __tablename__ = 'video_tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    @staticmethod
    def check_and_add_tags(tag_list):
        """ 각 태그들을 분리하고, db에 있는지 확인 한뒤, 태그들의 아이디 값을 리턴한다."""
        tag_list = list(set(tag_list.split('#')))
        tags_to_add_db = []
        tag_id_list = []
        for tag_str in tag_list:
            tag_str = tag_str.strip()
            if tag_str is '':
                continue
            tag_db = VideoTag.query.filter_by(name=tag_str).first()
            if tag_db is None:
                tag_db = VideoTag(name=tag_str)
                tags_to_add_db.append(tag_db)
            else:
                tag_id_list.append(tag_db)
        db.session.add_all(tags_to_add_db)
        db.session.commit()

        for tag in tags_to_add_db:
            tag_id_list.append(tag)
        return tag_id_list
