# Case No. 1 from https://github.com/Pogchamp-company/alembic-postgresql-enum/issues/26
import enum
from typing import TYPE_CHECKING

from alembic_postgresql_enum.get_enum_data import (
    TableReference,
    get_defined_enums,
    get_declared_enums,
)
from tests.base.run_migration_test_abc import CompareAndRunTestCase
from tests.schemas import ANOTHER_SCHEMA_NAME, DEFAULT_SCHEMA

if TYPE_CHECKING:
    from sqlalchemy import Connection
from sqlalchemy import MetaData, Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import ENUM

my_metadata = MetaData(schema=ANOTHER_SCHEMA_NAME)


Base = declarative_base(metadata=my_metadata)


# Definition of my enum
class _TestStatus(enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


# Definition of my model class
class TableWithExplicitEnumSchema(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)

    status = Column(
        ENUM(_TestStatus, name="test_status", inherit_schema=True),
        nullable=False,
    )


def test_get_defined_enums(connection: "Connection"):
    database_schema = my_metadata
    database_schema.create_all(connection)

    function_result = get_defined_enums(connection, ANOTHER_SCHEMA_NAME)

    assert function_result == {"test_status": tuple(map(lambda item: item.value, _TestStatus))}


def test_get_declared_enums(connection: "Connection"):
    declared_schema = my_metadata

    function_result = get_declared_enums(declared_schema, ANOTHER_SCHEMA_NAME, DEFAULT_SCHEMA, connection)

    assert function_result.enum_values == {"test_status": tuple(map(lambda item: item.value, _TestStatus))}
    assert function_result.enum_table_references == {
        "test_status": frozenset(
            [
                TableReference(
                    table_schema=ANOTHER_SCHEMA_NAME,
                    table_name=TableWithExplicitEnumSchema.__tablename__,
                    column_name="status",
                )
            ]
        )
    }


class TestCompareAndRun(CompareAndRunTestCase):
    def get_database_schema(self) -> MetaData:
        return my_metadata

    def get_target_schema(self) -> MetaData:
        return my_metadata

    def get_expected_upgrade(self) -> str:
        return f"""
        # ### commands auto generated by Alembic - please adjust! ###
        pass
        # ### end Alembic commands ###
        """

    def get_expected_downgrade(self) -> str:
        return f"""
        # ### commands auto generated by Alembic - please adjust! ###
        pass
        # ### end Alembic commands ###
        """
