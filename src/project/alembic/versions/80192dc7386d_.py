"""baby proof db

Revision ID: 80192dc7386d
Revises: 41e68099b606
Create Date: 2024-09-19 21:03:56.478432

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "80192dc7386d"
down_revision: Union[str, None] = "41e68099b606"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("languages_repository_id_fkey", "languages", type_="foreignkey")
    op.create_foreign_key(None, "languages", "repositories", ["repository_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "languages", type_="foreignkey")
    op.create_foreign_key(
        "languages_repository_id_fkey",
        "languages",
        "repositories",
        ["repository_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###
