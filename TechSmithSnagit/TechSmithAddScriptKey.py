#!/usr/bin/env python
#
# Copyright 2015 Brandon Kerns
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, print_function

import os

from autopkglib import Processor, ProcessorError, get_pref

__all__ = ["TechSmithAddScriptKey"]


class TechSmithAddScriptKey(Processor):
    description = "Allows AutoPkg to add a supplied regTechSmithAddScriptKeyistration key to \
                   the postinstall script that will be included in the pkg."
    input_variables = {
        "REG_KEY": {
            "description": "TechSmith Registration Key.",
            "required": True
        }
    }
    output_variables = {
    }

    def main(self):
        # Open the postinstall script, substitute the registration info, write changes.
        
        key = self.env['REG_KEY']
        
        # print(key)
        
        path = os.path.join(os.path.dirname(__file__), 'Scripts/postinstall')
        
        # print(path)
        
        if key is not None:
            
            filetext = None
            
            with open(path, 'r') as file :
               filetext = file.read()
            
            if 'regkey=""' in filetext:
                
                filetext = filetext.replace('regkey=\"\"', "regkey=\"%s\"" % (key))
                
                with open(path, 'w') as file:
                    file.write(filetext)

if __name__ == "__main__":
    processor = TechSmithAddScriptKey()
    processor.execute_shell()
