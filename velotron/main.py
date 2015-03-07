'''
Created on Mar 5, 2015

@author: dan
'''

import velotron

def main():
    f1 = 'c:\users\dan\downloads\DAN-QVT 40 MILES FLAT STRAIGHT-2015-03-04-10-36-50.3DP.txt'
    f2 = 'c:\users\dan\downloads\DAN-QVT 40 MILES FLAT STRAIGHT-2015-03-04-11-11-58.3DP.txt'
    of1 = r'c:\users\dan\downloads\DAN-QVT 40 MILES FLAT STRAIGHT-2015-03-04-11-12-34.3DP.txt'
    v1 = velotron.Velotron3DWorkout(f1)
    v2 = velotron.Velotron3DWorkout(f2)
    v1.append(v2)
    v1.write(of1)

if __name__ == '__main__':
    main()