import sys
import unittest
import xml.etree.ElementTree as ET
import logging

from tests.logger import log


def compare_versions(version1, version2):
    v1_parts = [int(part) for part in version1.split(".")]
    v2_parts = [int(part) for part in version2.split(".")]

    for v1, v2 in zip(v1_parts, v2_parts):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
    return 0


def incremental_changeset_ids(tree):
    root = tree.getroot()

    last_version = "0.0.0"  # Start with a very low version
    for changeset in root.findall(
        ".//{http://www.liquibase.org/xml/ns/dbchangelog}changeSet"
    ):
        version_str = changeset.get("id").split("_")[1]
        if compare_versions(version_str, last_version) > 0:
            last_version = version_str
        else:
            log.info(f"Incorrect version --> {version_str}")
            return False
    return True


class TestChangeLog(unittest.TestCase):

    def setUp(self):
        self.changeset = ET.parse("liquibase-postgres-db/changelog/change_log_main.xml")

    def test_incremental_changeset_ids(self):
        print(self.changeset)
        self.assertTrue(
            incremental_changeset_ids(self.changeset),
            "ChangeSet IDs are not incremental.",
        )


if __name__ == "__main__":
    unittest.main()