'''
Created on Mar 6, 2015

@author: dan
'''

class Velotron3DWorkout(object):
    '''
    classdocs
    '''

    def append(self, v):
        if self.workout_cols != v.workout_cols:
            raise Exception('attempt to append workout with different workout_cols')
        
        time_col = self.workout_cols_dict['ms']
        miles_col = self.workout_cols_dict['miles']
        
        time_offset = 1 + int(self.workout[-1][time_col].strip('"'))
        miles_offset = float(self.workout[-1][miles_col].strip('"'))
        
        for l in v.workout:
            l[time_col] = '"%10d"' % (time_offset + int(l[time_col].strip('"')))
            l[miles_col] = '"%8.4f"' % (miles_offset + float(l[miles_col].strip('"')))
            self.workout.append(l)
            
        
    def write(self, file_name):
        f = open(file_name, 'w')
        f.write('[USER DATA]\n')
        f.write('%s\n' % self.user_data['user'])
        for item in self.user_data_items:
            f.write('%s=%s\n' % (item, self.user_data[item]))
        f.write('[END USER DATA]\n')
        
        f.write('\n[COURSE HEADER]\n')
        for item in self.course_header_items:
            f.write('%s = %s\n' % (item, self.course_header[item]))
        f.write('[END COURSE HEADER]\n')
        
        f.write('\n[COURSE DATA]\n')
        for line in self.course_data:
            f.write(line)
        f.write('[END COURSE DATA]\n')
        
        f.write('\nnumber of records = %d\n\n' % self.num_records)
        f.write('%s\n\n' % ' '.join(self.workout_cols))
        
        for l in self.workout:
            f.write('%s\n' % ','.join(l))
        
        f.write('\n')
        f.close()
        
    def __init__(self, file_name):
        '''
        Constructor
        '''
        f = open(file_name, 'r')
        d = dict()
        
        ##
        ## Digest USER DATA section
        ##
        ln = 0
        line, ln = f.readline(), ln+1
        lookfor = '[USER DATA]'
        
        if line.strip() != lookfor:
            raise Exception('line %d: expecting %s' % (ln, lookfor))
        
        line, ln = f.readline(), ln+1
        d['user'] = line.strip()
        l = []
        
        while True:
            line, ln = f.readline(), ln+1
            if line.strip() == '[END USER DATA]':
                break
            tokens=line.strip().split('=')
            if len(tokens) != 2:
                raise Exception('line %d: expecting form <attr>=<value> but got "%s" instead' % (ln, line))
            d[tokens[0]] = tokens[1]
            l.append(tokens[0])
 
        self.user_data = d
        self.user_data_items = l
                    
        ##
        ## Digest COURSE HEADER section
        ##
        while True:
            line, ln = f.readline(), ln+1
            if len(line)==0 or line != '\n':
                break
        
        lookfor = '[COURSE HEADER]\n'
        if line != lookfor:
            raise Exception('line %d: expecting %s' % (ln, lookfor))

        d, l = {}, []
        
        while True:
            line, ln = f.readline(), ln+1
            if line == '[END COURSE HEADER]\n':
                break
            tokens=line.strip().split('=')
            if len(tokens) != 2:
                raise Exception('line %d: expecting form <attr>=<value> but got "%s" instead' % (ln, line))
            d[tokens[0].strip()] = tokens[1].strip()
            l.append(tokens[0].strip())
            
        self.course_header = d
        self.course_header_items = l
        
        ##
        ## Digest COURSE DATA section
        ##
        while True:
            line, ln = f.readline(), ln+1
            if len(line)==0 or line != '\n':
                break
        
        lookfor = '[COURSE DATA]\n'
        if line != lookfor:
            raise Exception('line %d: expecting %s' % (ln, lookfor))

        l = []
                
        while True:
            line, ln = f.readline(), ln+1
            if line == '[END COURSE DATA]\n':
                break
            l.append(line)

        self.course_data = l
        
        ##
        ## Digest COURSE DATA section
        ##
        while True:
            line, ln = f.readline(), ln+1
            if len(line)==0 or line != '\n':
                break
        
        lookfor = 'number of records = '
        if line.find(lookfor) != 0:
            raise Exception('line %d: expecting %s' % (ln, lookfor))
        tokens=line.split('=')
        if len(tokens) != 2:
            raise Exception('line %d: expecting form <attr>=<value> but got "%s" instead' % (ln, line))
        self.num_records = int(tokens[1])
        
        while True:
            line, ln = f.readline(), ln+1
            if len(line.strip()) != 0:
                break

        self.workout_cols = line.strip().split(' ')
        self.workout_cols_dict = {}    
        for i in range(len(self.workout_cols)):
            self.workout_cols_dict[self.workout_cols[i]] = i
        

        while True:
            line, ln = f.readline(), ln+1
            if len(line)==0 or line != '\n':
                break

        self.workout = []
        while True:
            tokens=line.strip().split(',')
            if len(tokens) != len(self.workout_cols):
                raise Exception('line %d: expecting row with %d comma-separated tokens enclosed in double-quotes' % (ln, len(self.workout_cols)))
            self.workout.append(tokens)
            while True:
                line, ln = f.readline(), ln+1
                if len(line)==0 or line != '\n':
                    break
                
            if len(line)==0:
                break
        
        f.close()