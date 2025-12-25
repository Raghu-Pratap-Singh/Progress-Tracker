import sqlite3
from sortedcontainers import SortedDict
import datetime
# fenwick tree class creation
class FenwickTree:

    def __init__(self, n):
        self.fen = [0]*(n+1)
    
    def update(self, idx, val):
        while idx<len(self.fen):
            self.fen[idx]+=val
            idx+=idx & (-idx)
    
    def query(self, idx):
        cnt = 0
        while idx>0:
            cnt+=self.fen[idx]
            idx-=idx & (-idx)
        return cnt

import sqlite3
import datetime
from sortedcontainers import SortedDict

# ... (FenwickTree class remains same)

class tool:
    def __init__(self):
        self.conn = sqlite3.connect("tracker.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                date TEXT, 
                tasks_done INTEGER
            )
        """)  
        self.conn.commit()
        self.Map = SortedDict()

    def to_tuple(self, date_str):
        temp = [int(x) for x in date_str.split("-")]
        return (temp[2], temp[1], temp[0])

    # New validation function
    def check_date(self, date_tuple):
        today = datetime.date.today()
        today_tuple = (today.year, today.month, today.day)
        if date_tuple > today_tuple:
            return False
        return True


    def create_tree(self):
        self.cursor.execute("select * from records order by date")
        response = self.cursor.fetchall()
        arr = []
        for t in response:
            y, m, d = self.to_tuple(t[1])
            arr.append((y, m, d, t[2]))
        
        arr.sort()
        n = len(arr)
        for i in range(n):
            self.Map[(arr[i][0], arr[i][1], arr[i][2])] = [i+1, arr[i][3]]
        
        self.fen = FenwickTree(36600)
        for key in self.Map:
            self.fen.update(self.Map[key][0], self.Map[key][1])
    def great(self,date_str):
        # Convert the input string to a (Y, M, D) tuple for comparison
        new_date_tuple = self.to_tuple(date_str)
        
        # If the Map is empty, this is the first entry, so it's "the greatest" by default
        if not self.Map:
            return True
            
        # Get the latest date currently in the Map
        # self.Map.peekitem(-1) returns a tuple (key, value). We want the key [0].
        last_date_tuple = self.Map.peekitem(-1)[0]
        
        # Return True if the new date is strictly greater than the last stored date
        return new_date_tuple > last_date_tuple
    def update(self, date_str:str, tasks:int):
        search_tuple = self.to_tuple(date_str)
        
        # Run check
        response = self.check_date(search_tuple)
        if response is False:
            return False
        
        target_idx = None
        if search_tuple in self.Map:
            target_idx = self.Map[search_tuple][0]
            self.cursor.execute("UPDATE records SET tasks_done = tasks_done + ? WHERE date = ?", (tasks, date_str))
        else:
            # first check that user if not updating previous date, then he/she should insert the latest date only, that is greater than greatest present
            isGreater = self.great(date_str)
            if not isGreater:
                return False
            target_idx = len(self.Map) + 1
            self.Map[search_tuple] = [target_idx, tasks]
            self.cursor.execute("INSERT INTO records (date, tasks_done) VALUES (?, ?)", (date_str, tasks))

        self.conn.commit()
        self.fen.update(target_idx, tasks)
        return True

    def get_idx_lower_bound(self, date_str:str):
        query_tuple = self.to_tuple(date_str)
        
        # Run check
        self.check_date(query_tuple)
        
        idx = self.Map.bisect_left(query_tuple)
        if idx < len(self.Map):
            return self.Map.peekitem(idx)[1][0]
        return None
    
    def query(self, start_date:str, end_date:str):
        # The checks are now inside get_idx_lower_bound or called here
        i = self.get_idx_lower_bound(start_date)
        
        # Check end date specifically
        end_tuple = self.to_tuple(end_date)
        response = self.check_date(end_tuple)
        if response is False:
            return -1

        j_pos = self.Map.bisect_right(end_tuple) - 1
        j = self.Map.peekitem(j_pos)[1][0] if j_pos >= 0 else None

        if (i is not None) and (j is not None) and (i <= j):
            response = self.fen.query(j) - self.fen.query(i-1)
            return response
        
        return 0
    
