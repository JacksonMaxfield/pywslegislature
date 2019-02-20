#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from .biennium import Biennium
from .committee import Committee
from .services import CommitteeService
from .query import WSLRequest

###############################################################################

log = logging.getLogger(__name__)

###############################################################################


class Legislature(object):
    """
    Create a Legislature object to interact and manage all of the primary queries
    for a Washington State Legislature given a biennium.

    :param biennium: A Biennium object for the Legislature to manage queries for.
    """

    def __init__(self, biennium: Biennium = None):
        # Initialize with current biennium
        if biennium is None:
            biennium = Biennium()

        # Make hidded
        self._biennium = biennium

        # Lazy loaded
        self._committees = None

    @property
    def biennium(self):
        return self._biennium

    @property
    def committees(self):
        # Lazy load committees
        if self._committees is None:
            # Construct request using defaults and object biennium
            request = WSLRequest(
                CommitteeService.header,
                CommitteeService.GetCommittees.name,
                {"biennium": str(self.biennium)}
            )

            # Get results from request
            results = request.process().json["ArrayOfCommittee"]["Committee"]

            # Convert to committee objects
            self._committees = [
                Committee(c["Id"], c["Name"], c["LongName"], c["Agency"], c["Acronym"], c["Phone"]) for c in results
            ]
            log.info("Reduced returned results by selecting {}:{}".format("ArrayOfCommittee", "Committee"))

        return self._committees

    def __str__(self):
        return "<Legislature [{}]>".format(self.biennium)

    def __repr__(self):
        return str(self)