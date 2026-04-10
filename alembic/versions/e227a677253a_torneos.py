"""torneos

Revision ID: e227a677253a
Revises: 470223fc6208
Create Date: 2026-04-09 23:54:19.930852

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e227a677253a"
down_revision: Union[str, Sequence[str], None] = "470223fc6208"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Tabla torneo
    op.create_table(
        "torneos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
        sa.Column("fecha_creacion", sa.DateTime, nullable=False),
        sa.Column("estado", sa.Text, nullable=False),
    )

    # Tabla equipo torneos
    op.create_table(
        "equipos_torneo",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("torneo_id", sa.Integer, sa.ForeignKey("torneos.id"), nullable=False),
        sa.Column("nombre", sa.Text, nullable=False),
    )

    # Tabla jugadores torneo
    op.create_table(
        "jugadores_torneo",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("equipo_torneo_id", sa.Integer, sa.ForeignKey("equipos_torneo.id")),
        sa.Column("usuario_id", sa.Integer, sa.ForeignKey("jugadores.id")),
    )

    # Tabla partidos_toreno
    op.create_table(
        "partidos_torneo",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("torneo_id", sa.Integer, sa.ForeignKey("torneos.id")),
        sa.Column("local_id", sa.Integer, sa.ForeignKey("equipos_torneo.id")),
        sa.Column("visitante_id", sa.Integer, sa.ForeignKey("equipos_torneo.id")),
        sa.Column("goles_local", sa.Integer, nullable=True),
        sa.Column("goles_visitante", sa.Integer, nullable=True),
        sa.Column("fase", sa.Text, nullable=False),
        sa.Column("jugado", sa.Boolean, default=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("torneos")
    op.drop_table("equipos_torneo")
    op.drop_table("jugadores_torneo")
    op.drop_table("partidos_torneo")
