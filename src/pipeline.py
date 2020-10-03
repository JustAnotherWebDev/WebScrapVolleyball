from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


metadata = MetaData()

class BeachvolleyballCupsPipeline(object):
  def __init__(self):
    engine = create_engine('sqlite:///:memory:', echo=True)
    
