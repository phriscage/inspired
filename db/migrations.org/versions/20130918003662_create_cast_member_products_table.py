from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
cast_members = Table('cast_members', post_meta,
    Column('cast_member_id', Integer(unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=120), unique=True, index=True, nullable=False),
    Column('first_name', String(length=120)),
    Column('last_name', String(length=120)),
    Column('actor_first_name', String(length=120)),
    Column('actor_last_name', String(length=120)),
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
    Column('ref_product_style_id', Integer, nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

cast_member_products = Table('cast_member_products', post_meta,
    Column('cast_member_id', Integer(unsigned=True),
        ForeignKey('cast_members.cast_member_id',
        name='fk_cast_member_products_cast_member_id', ondelete="CASCADE"),
        index=True, nullable=False),
    Column('product_id', Integer(unsigned=True),
        ForeignKey('products.product_id',
        name='fk_cast_member_products_product_id', ondelete="CASCADE"),
        index=True, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cast_member_products'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cast_member_products'].drop()
