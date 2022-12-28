#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create geo-comments tables."""

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from sqlalchemy.dialects import mysql, postgresql

# revision identifiers, used by Alembic.
revision = "9ee00acd3274"
down_revision = "f79e92a678f0"
branch_labels = ()
depends_on = "9e0ac518b9df"


def upgrade():
    """Upgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "packagecomment_metadata",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column("user", sa.Integer(), nullable=True),
        sa.Column("record", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["record"],
            ["geo_package_records_metadata.id"],
            name=op.f("fk_packagecomment_metadata_record_geo_package_records_metadata"),
        ),
        sa.ForeignKeyConstraint(
            ["user"],
            ["accounts_user.id"],
            name=op.f("fk_packagecomment_metadata_user_accounts_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_packagecomment_metadata")),
    )
    op.create_table(
        "packagefeedback_metadata",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column("user", sa.Integer(), nullable=True),
        sa.Column("record", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["record"],
            ["geo_package_records_metadata.id"],
            name=op.f(
                "fk_packagefeedback_metadata_record_geo_package_records_metadata"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["user"],
            ["accounts_user.id"],
            name=op.f("fk_packagefeedback_metadata_user_accounts_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_packagefeedback_metadata")),
        sa.UniqueConstraint(
            "user", "record", name=op.f("uq_packagefeedback_metadata_user")
        ),
    )
    op.create_table(
        "resourcecomment_metadata",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column("user", sa.Integer(), nullable=True),
        sa.Column("record", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["record"],
            ["rdm_records_metadata.id"],
            name=op.f("fk_resourcecomment_metadata_record_rdm_records_metadata"),
        ),
        sa.ForeignKeyConstraint(
            ["user"],
            ["accounts_user.id"],
            name=op.f("fk_resourcecomment_metadata_user_accounts_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_resourcecomment_metadata")),
    )
    op.create_table(
        "resourcefeedback_metadata",
        sa.Column(
            "created",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column("user", sa.Integer(), nullable=True),
        sa.Column("record", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["record"],
            ["rdm_records_metadata.id"],
            name=op.f("fk_resourcefeedback_metadata_record_rdm_records_metadata"),
        ),
        sa.ForeignKeyConstraint(
            ["user"],
            ["accounts_user.id"],
            name=op.f("fk_resourcefeedback_metadata_user_accounts_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_resourcefeedback_metadata")),
        sa.UniqueConstraint(
            "user", "record", name=op.f("uq_resourcefeedback_metadata_user")
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("resourcefeedback_metadata")
    op.drop_table("resourcecomment_metadata")
    op.drop_table("packagefeedback_metadata")
    op.drop_table("packagecomment_metadata")
    # ### end Alembic commands ###
