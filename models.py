from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Intonation(db.Model):
    __tablename__ = 'intonations'

    id = Column(Integer, primary_key=True)
    intonation = Column(String)


class Semantics(db.Model):
    __tablename__ = 'semantics'

    id = Column(Integer, primary_key=True)
    semantics = Column(String)


class SpeechAct(db.Model):
    __tablename__ = 'speech_acts'

    id = Column(Integer, primary_key=True)
    speech_act = Column(String)


class DF(db.Model):
    __tablename__ = 'dfs'

    id = Column(Integer, primary_key=True)
    df = Column(String)
    language = Column(String)
    glosses = Column(String)
    syntax = Column(String)
    primary_semantics_id = Column(Integer, ForeignKey('semantics.id'))
    primary_semantics = relationship("Semantics", foreign_keys=[primary_semantics_id])
    additional_semantics_id = Column(Integer, ForeignKey('semantics.id'))
    additional_semantics = relationship("Semantics", foreign_keys=[additional_semantics_id])
    speech_act_1_id = Column(Integer, ForeignKey("speech_acts.id"))
    speech_act_1 = relationship("SpeechAct", foreign_keys=[speech_act_1_id])
    speech_act_id = Column(Integer, ForeignKey("speech_acts.id"))
    speech_act = relationship("SpeechAct", foreign_keys=[speech_act_id])
    structure = Column(String)
    intonation_id = Column(Integer, ForeignKey("intonations.id"))
    intonation = relationship("Intonation", foreign_keys=[intonation_id])
    source_construction = Column(String)
    source_construction_syntax = Column(String)
    source_construction_intonation_id = Column(Integer, ForeignKey("intonations.id"))
    source_construction_intonation = relationship("Intonation", foreign_keys=[source_construction_intonation_id])
    examples = Column(String)
    comments = Column(String)

    def __eq__(self, other: "DF"):
        # print([self.df, other.df],
        #       [self.language, other.language],
        #       [self.glosses, other.glosses],
        #       [self.syntax, other.syntax],
        #       [self.primary_semantics_id, other.primary_semantics_id],
        #       [self.additional_semantics_id, other.additional_semantics_id],
        #       [self.speech_act_id, other.speech_act_id],
        #       [self.speech_act_1_id, other.speech_act_1_id],
        #       [self.structure, other.structure],
        #       [self.intonation_id, other.intonation_id],
        #       [self.source_construction, other.source_construction],
        #       [self.source_construction_syntax, other.source_construction_syntax],
        #       [self.source_construction_intonation_id, other.source_construction_intonation_id],
        #       [self.examples, other.examples],
        #       [self.comments, other.comments])

        return str(self.df) == str(other.df) and str(self.language) == str(other.language) \
               and str(self.glosses) == str(other.glosses) and str(self.syntax) == str(other.syntax) \
               and str(self.primary_semantics_id) == str(other.primary_semantics_id) \
               and str(self.additional_semantics_id) == str(other.additional_semantics_id) \
               and str(self.speech_act_id) == str(other.speech_act_id) and str(self.speech_act_1_id) == str(
            other.speech_act_1_id) \
               and str(self.structure) == str(other.structure) and str(self.intonation_id) == str(other.intonation_id) \
               and str(self.source_construction) == str(other.source_construction) \
               and str(self.source_construction_syntax) == str(other.source_construction_syntax) \
               and str(self.source_construction_intonation_id) == str(other.source_construction_intonation_id) \
               and str(self.examples) == str(other.examples) and str(self.comments) == str(other.comments)
