#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create marketplace comments/feedback tables."""

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from sqlalchemy.dialects import mysql, postgresql

# revision identifiers, used by Alembic.
revision = "21e0095448da"
down_revision = "9ee00acd3274"
branch_labels = ()
depends_on = ("081eb89a9035",)  # GEO RDM Records - Marketplace tables


def upgrade():
    """Upgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "marketplacecomment_metadata",
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
            ["geo_marketplace_items_metadata.id"],
            name=op.f(
                "fk_marketplacecomment_metadata_record_geo_marketplace_items_metadata"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["user"],
            ["accounts_user.id"],
            name=op.f("fk_marketplacecomment_metadata_user_accounts_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_marketplacecomment_metadata")),
    )
    op.create_table(
        "marketplacefeedback_metadata",
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
            ["geo_marketplace_items_metadata.id"],
            name=op.f(
                "fk_marketplacefeedback_metadata_record_geo_marketplace_items_metadata"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["user"],
            ["accounts_user.id"],
            name=op.f("fk_marketplacefeedback_metadata_user_accounts_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_marketplacefeedback_metadata")),
        sa.UniqueConstraint(
            "user", "record", name=op.f("uq_marketplacefeedback_metadata_user")
        ),
    )
    op.alter_column(
        "files_objecttags",
        "key",
        existing_type=sa.TEXT(),
        type_=sa.String(length=255),
        existing_nullable=False,
    )
    op.alter_column(
        "records_metadata_version",
        "json",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        type_=sa.JSON()
        .with_variant(sqlalchemy_utils.types.json.JSONType(), "mysql")
        .with_variant(
            postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
        )
        .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
        existing_nullable=True,
        autoincrement=False,
    )
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("marketplacefeedback_metadata")
    op.drop_table("marketplacecomment_metadata")
    # ### end Alembic commands ###
