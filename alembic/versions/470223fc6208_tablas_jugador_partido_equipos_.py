"""Tablas jugador, partido, equipos, estadisticas partidos

Revision ID: 470223fc6208
Revises:
Create Date: 2026-03-08 15:51:54.215870

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "470223fc6208"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Tabla jugadores
    op.create_table(
        "jugadores",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
        sa.Column("apodo", sa.Text, nullable=True),  # Cambiado a True
        sa.Column("imagen", sa.Text, nullable=True),
    )

    # Tabla equipos
    op.create_table(
        "equipos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nombre", sa.Text, nullable=False),
    )

    # Tabla partidos
    op.create_table(
        "partidos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fecha", sa.Date(), nullable=False),
        sa.Column(
            "equipo_local_id", sa.Integer, sa.ForeignKey("equipos.id"), nullable=False
        ),
        sa.Column(
            "equipo_visitante_id",
            sa.Integer,
            sa.ForeignKey("equipos.id"),
            nullable=False,
        ),
        sa.Column("goles_local", sa.Integer, server_default="0"),
        sa.Column("goles_visitante", sa.Integer, server_default="0"),
    )

    # Tabla estadisticas
    op.create_table(
        "estadisticas_partidos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "partido_id", sa.Integer, sa.ForeignKey("partidos.id"), nullable=False
        ),
        sa.Column(
            "jugador_id", sa.Integer, sa.ForeignKey("jugadores.id"), nullable=False
        ),
        sa.Column("equipo_id", sa.Integer, sa.ForeignKey("equipos.id"), nullable=False),
        sa.Column("goles", sa.Integer, server_default="0"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # El orden de borrado debe ser inverso a la creación
    op.drop_table("estadisticas_partidos")
    op.drop_table("partidos")
    op.drop_table("equipos")
    op.drop_table("jugadores")
