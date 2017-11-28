from sqlalchemy import func

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
    tags = db.relationship('VideoTag', secondary=tags, lazy='dynamic',
                           backref=db.backref('videos', lazy='joined'))

    def set_tags(self, tags_list):
        """기존의 태그와 비교하여 기존 테그에 추가 및 삭제"""
        origin_tags = set(self.tags)
        new_tags = set(extract_tags(tags_list))
        for tag in (new_tags-origin_tags):
            self.tags.append(tag)
        for tag in (origin_tags - new_tags):
            self.tags.delete(tag)
        db.session.add(self)
        db.session.commit()


class VideoTag(db.Model):
    __tablename__ = 'video_tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    def __repr__(self):
        return '#%s' % self.name


def get_random_video():
    """ Return 5 random videos """
    return Video.query.order_by(func.random()).limit(5).all()


def extract_tags(tags_list):
    """ 각 태그들을 분리하고, db에 있는지 확인한 뒤, 태그들을 리턴한다."""
    result = []
    tags_list = split_tags(tags_list)
    for tag_str in tags_list:
        tag_obj = VideoTag.query.filter_by(name=tag_str).first()
        if tag_obj is None:
            tag_obj = VideoTag(name=tag_str)
        result.append(tag_obj)
    return result


def split_tags(tags_list):
    """ string 태그값을 #을 기준으로 분리하여 리스트를 리턴"""
    tags_list = tags_list.replace(' ', '').replace(',', '').replace('[', '').replace(']', '')
    tags_list = [tag.lower() for tag in tags_list.split('#')]
    tags_list = set(tags_list)
    if '' in tags_list:
        tags_list.remove('')
    return tags_list
