#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

from autopkglib import Processor, ProcessorError, URLGetter


__all__ = ["TechSmithURLProvider"]

TS_BASE_URL = "https://www.techsmith.com/api/v/1/products/getallversions/%s"
TS_VER_URL = "https://www.techsmith.com/api/v/1/products/getversioninfo/%s"
TS_DL_URL = "http://download.techsmith.com%s%s"

TS_PROD_CODES = {
    "camtasia": 9,
    "snagit": 100,
}


class TechSmithURLProvider(URLGetter):
    """Provides URL to the latest Techsmith product release."""

    description = __doc__
    input_variables = {
        "product_name": {
            "required": True,
            "description": "Product to fetch URL for. One of 'camtasia' or 'snagit'.",
        },
        "base_url": {
            "required": False,
            "description": "Default is '%s." % TS_BASE_URL,
        },
    }
    output_variables = {
        "url": {"description": "URL to the latest Techsmith product release.",},
    }

    def main(self):
        """Provide a Techsmith download URL"""

        # Use provided product name to determine the product code
        product_name = self.env["product_name"]
        if product_name not in TS_PROD_CODES.keys():
            raise ProcessorError("Unknown product name: %s" % product_name)
        prodcode = TS_PROD_CODES[product_name]

        # Retrieve JSON file that contains version information
        base_url = self.env.get("base_url", TS_BASE_URL)
        url = base_url % (prodcode)
        data = json.loads(self.download(url))

        # Get version information for the item with the greatest VersionID
        data = sorted(data, key=lambda x: int(x["VersionID"]), reverse=True)
        vers = "%s.%s.%s" % (data[0]["Major"], data[0]["Minor"], data[0]["Maintenance"])
        versionid = data[0]["VersionID"]

        # With the latest version information, obtain the download URL
        vurl = TS_VER_URL % (versionid)
        vdata = json.loads(self.download(vurl))
        dlurl = TS_DL_URL % (
            vdata["PrimaryDownloadInformation"]["RelativePath"],
            vdata["PrimaryDownloadInformation"]["Name"],
        )
        self.env["url"] = dlurl
        self.env["version"] = vers
        self.output("Found URL %s" % self.env["url"])
        self.output("Found Version %s" % self.env["version"])


if __name__ == "__main__":
    PROCESSOR = TechSmithURLProvider()
    PROCESSOR.execute_shell()
