from mongoengine import *
import datetime

class Checkpoint(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
        distance: MongoEngine float field, required, (checkpoint distance in kilometers),
		location: MongoEngine string field, optional, (checkpoint location name),
		open_time: MongoEngine datetime field, required, (checkpoint opening time),
		close_time: MongoEngine datetime field, required, (checkpoint closing time).
    """
    distance = FloatField(default = 0, required=True)
    location = StringField(max_length = 100)
    open_time = DateTimeField(default=datetime.datetime.utcnow, required=True)
    close_time = DateTimeField(default=datetime.datetime.utcnow, required=True)


class Brevet(Document):
    """
    A MongoEngine document containing:
		length: MongoEngine float field, required
		start_time: MongoEngine datetime field, required
		checkpoints: MongoEngine list field of Checkpoints, required
    """
    length = FloatField(default = 0, required=True)
    start_time = DateTimeField(default=datetime.datetime.utcnow, required=True)
    checkpoints = EmbeddedDocumentListField(Checkpoint, required=True)
