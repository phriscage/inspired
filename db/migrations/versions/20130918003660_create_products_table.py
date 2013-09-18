from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ref_product_types = Table('ref_product_types', post_meta,
    Column('ref_product_type_id', Integer(4, unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=60), unique=True, nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)
ref_product_styles = Table('ref_product_styles', post_meta,
    Column('ref_product_style_id', Integer(4, unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=60), unique=True, nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)


products = Table('products', post_meta,
    Column('product_id', Integer(unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=120), unique=True, index=True, nullable=False),
    Column('upc', String(length=120), index=True, nullable=False),
    Column('image_url', String(length=255)),
    Column('ref_product_type_id', Integer(4, unsigned=True), 
        ForeignKey('ref_product_types.ref_product_type_id',
        name='fk_scenes_ref_product_type_id', ondelete="CASCADE"), 
        nullable=False),
    Column('ref_product_style_id', Integer(4, unsigned=True), 
        ForeignKey('ref_product_styles.ref_product_style_id',
        name='fk_scenes_ref_product_style_id', ondelete="CASCADE"), 
        nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['products'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['products'].drop()
