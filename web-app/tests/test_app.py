from flask import Flask, render_template
import pytest
import pytest_flask
import pymongo
import mongomock
import os

class TestApp:

    def test_sanity(self):
        assert True, "Sanity check failed."