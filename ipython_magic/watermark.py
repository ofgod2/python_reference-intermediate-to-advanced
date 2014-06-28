""" 
Sebastian Raschka 2014

watermark.py
version 1.0.0


IPython magic function to print date/time stamps and various system information.

Installation: 

    %install_ext https://raw.githubusercontent.com/rasbt/python_reference/master/ipython_magic/watermark.py
    
Usage:

    %load_ext watermark
    
    %watermark
    
    optional arguments:
      -d, --date            prints current date
      -n, --datename        prints date with abbrv. day and month names
      -t, --time            prints current time
      -z, --timezone        appends the local time zone
      -u, --updated         appends a string "Last updated: "
      -c CUSTOM_TIME, --custom_time CUSTOM_TIME
                        prints a valid strftime() string
      -v, --python          prints Python and IPython version
      -p PACKAGES, --packages PACKAGES
                        prints versions of specified Python modules and
                        packages
      -m, --machine         prints system and machine info
    
Examples:

    %watermark -d -t
    
"""
import platform
from time import strftime
from pkg_resources import get_distribution
from multiprocessing import cpu_count

import IPython
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

@magics_class
class WaterMark(Magics):
    """ 
    IPython magic function to print date/time stamps 
    and various system information.
    
    """
    @magic_arguments()
    @argument('-d', '--date', action='store_true', help='prints current date')
    @argument('-n', '--datename', action='store_true', help='prints date with abbrv. day and month names')
    @argument('-t', '--time', action='store_true', help='prints current time')
    @argument('-z', '--timezone', action='store_true', help='appends the local time zone')
    @argument('-u', '--updated', action='store_true', help='appends a string "Last updated: "')    
    @argument('-c', '--custom_time', type=str, help='prints a valid strftime() string')
    @argument('-v', '--python', action='store_true', help='prints Python and IPython version')
    @argument('-p', '--packages', type=str, help='prints versions of specified Python modules and packages')
    @argument('-m', '--machine', action='store_true', help='prints system and machine info')
    @line_magic
    def watermark(self, line):
        """ 
        IPython magic function to print date/time stamps 
        and various system information.
    
        """
        self.out = ''
        args = parse_argstring(self.watermark, line)

        if not any(vars(args).values()):
            self.out += strftime('%d/%m/%Y %H:%M:%S')
            self._get_pyversions()
            self._get_sysinfo()  
            
        else:
            if args.updated:
                self.out += 'Last updated: '
            if args.custom_time:
                self.out += '%s ' %strfime(args.custom_time)
            if args.date:
                self.out += '%s ' %strftime('%d/%m/%Y')
            elif args.datename:
                self.out += '%s ' %strftime('%a %b %M %Y')
            if args.time:
                self.out += '%s ' %strftime('%H:%M:%S')
            if args.timezone:
                self.out += strftime('%Z')
            if args.python:
                self._get_pyversions()
            if args.packages:
                self._get_packages(args.packages)
            if args.machine:
                self._get_sysinfo()
                
        print(self.out)

  
    def _get_packages(self, pkgs):
        if self.out:
            self.out += '\n'
        packages = pkgs.split(',') 
        for p in packages:
            self.out += '\n%s %s' %(p, get_distribution(p).version)
            
            
    def _get_pyversions(self):
        if self.out:
            self.out += '\n\n'
        self.out += 'Python %s\nIPython %s' %(
                platform.python_version(), 
                IPython.__version__
                )

        
    def _get_sysinfo(self):
        if self.out:
            self.out += '\n\n'
        self.out += 'compiler   : %s\nsystem     : %s\n'\
        'release    : %s\nmachine    : %s\n'\
        'processor  : %s\nCPU cores  : %s\ninterpreter: %s'%(
        platform.python_compiler(),
        platform.system(),
        platform.release(),
        platform.machine(),
        platform.processor(),
        cpu_count(),
        platform.architecture()[0]
        )


def load_ipython_extension(ipython):
    ipython.register_magics(WaterMark)