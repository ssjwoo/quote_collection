# from sqlalchemy import Column, Integer, ForeignKey
# from app.database import Base

# class QuoteTag(Base):
#     __tablename__ = "quote_tags"

#     quote_id = Column(Integer, ForeignKey("quotes.id", ondelete="CASCADE"), primary_key=True)
#     tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

###아래 내용으로 대체###
# Table 객체를 만들기 위해 sqlalchemy에서 Table을 가져옵니다.
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

# 'QuoteTag' 클래스 대신 'quote_tags'라는 이름의 Table 변수를 직접 선언합니다.
# 이 변수는 순수한 테이블 구조 정보만 담고 있어, 순환 참조를 일으키지 않습니다.
quote_tags = Table(
    'quote_tags', # 데이터베이스에 생성될 실제 테이블의 이름입니다.
    Base.metadata,
    # 'quotes' 테이블의 id를 참조하는 외래키 컬럼
    Column('quote_id', Integer, ForeignKey('quotes.id', ondelete="CASCADE"), primary_key=True),
    # 'tags' 테이블의 id를 참조하는 외래키 컬럼
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)
)