# ==========================================================
#   File: main.py
#   Author: Arkadiusz Wadowski
#   Email: wadowski.arkadiusz@gmail.com
#   Created: 20.03.2018
# ==========================================================

'''
*  Copyright (c) 2018, Arkadiusz Wadowski
*  All rights reserved.
*
*  Redistribution and use in source and binary forms, with or without
*  modification, are permitted provided that the following conditions are met:
*  1. Redistributions of source code must retain the above copyright
*     notice, this list of conditions and the following disclaimer.
*  2. Redistributions in binary form must reproduce the above copyright
*     notice, this list of conditions and the following disclaimer in the
*     documentation and/or other materials provided with the distribution.
*  3. Neither the name of the copyright holder nor the
*     names of its contributors may be used to endorse or promote products
*     derived from this software without specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
*  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
*  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
*  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
*  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
*  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
*  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
*  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
*  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
*  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
*  POSSIBILITY OF SUCH DAMAGE.
'''

from Async_TCP_Server.Async_TCP_Server import *
import logging
import commands

def main():
    try:
        logging.basicConfig(level=logging.DEBUG, format='%(name)s:[%(levelname)s]: %(message)s')
        # here we are forced to use wlan0 interface as it is out internal network interface
        #ip = commands.getstatusoutput('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')[1]
	    ip = '127.0.0.1'
        # just example port number
        port = 1234
	    print port
	    print ip
        server = Async_TCP_Server(('192.168.1.10', port), '192.168.1.10')
        asyncore.loop()
    except KeyboardInterrupt:
        print ("see you!")

if __name__ == '__main__':
    main()
