from datetime import datetime
from alembic import op
import sqlalchemy as sa
from passlib.hash import bcrypt
from src.enums.user_role import UserRole

# revision identifiers
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # === Создаём таблицы ===
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum(UserRole, name="userrole"), nullable=False, server_default=UserRole.USER.value),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("balance", sa.Numeric(12, 2), nullable=False, server_default="0.00"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("transaction_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # === Заполняем тестовыми данными ===
    conn = op.get_bind()
    now = datetime.utcnow()

    conn.execute(sa.text("""
        INSERT INTO users (email, hashed_password, full_name, role, created_at, updated_at)
        VALUES (:email, :password, :full_name, :role, :created_at, :updated_at)
    """), {
        "email": "admin@example.com",
        "password": bcrypt.hash("admin123"),
        "full_name": "Test Admin",
        "role": UserRole.ADMIN.value,
        "created_at": now,
        "updated_at": now
    })

    conn.execute(sa.text("""
        INSERT INTO users (email, hashed_password, full_name, role, created_at, updated_at)
        VALUES (:email, :password, :full_name, :role, :created_at, :updated_at)
    """), {
        "email": "user@example.com",
        "password": bcrypt.hash("user123"),
        "full_name": "Test User",
        "role": UserRole.USER.value,
        "created_at": now,
        "updated_at": now
    })

    conn.execute(sa.text("""
        INSERT INTO accounts (user_id, balance, created_at, updated_at)
        VALUES ( (SELECT id FROM users WHERE email = :email), 100.00, :created_at, :updated_at )
    """), {
        "email": "user@example.com",
        "created_at": now,
        "updated_at": now
    })


def downgrade():
    op.drop_table("payments")
    op.drop_table("accounts")
    op.drop_table("users")
