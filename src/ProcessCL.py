
# command line parser
import argparse
import os
  
def Init():
    parser = argparse.ArgumentParser(description ='Process one-liner into Google Calendar CSV')
    
    parser.add_argument(dest = "infile", metavar ='infile', nargs = 1, help = 'input filename (pdf)')
    #parser.add_argument('-p', '--pat', metavar ='pattern', 
    #                    required = True, dest ='patterns', 
    #                    action ='append', 
    #                    help ='text pattern to search for')
    
    parser.add_argument('-d', dest ='dumppdf',
                        action ='store_true', help ='print pdf contents and exit')
    parser.add_argument('-v', dest ='verbose',
                        action ='store_true', help ='verbose mode')
    parser.add_argument('-db', dest ='debug',
                        action ='store_true', help ='debug prints mode')
    parser.add_argument('-o', dest ='outfile', 
                        action ='store', help ='output file')
    parser.add_argument('-f', '--format', dest ='format', 
                        action ='store', choices = {'FAM1', 'FAM2'},
                        default ='FAM1', help ='Oneliner format specifier')
    args = parser.parse_args()

    if (args.verbose):
        print("command line args:")
        print(" infile  :", args.infile[0])
        print(" verbose :", args.verbose)
        print(" debug :", args.debug)
        print(" outfile :", args.outfile)
        print(" dumppdf :", args.dumppdf)
        print(" format  :", args.format)
        print(" filename:", os.path.basename(args.infile[0]))

    return args
