import datetime

import pytz

import main


class servertime():
    id : int
    serverid : str
    servertitle : str
    serverbeforetext : str
    serveraftertext : str
    serverfooter : str
    servertz : str
    servercolor : int
    twelvehourclock : bool

    def __init__(self, serverid,id = None, servertitle = "Default", serverbeforetext = "Default", serveraftertext = "", serverfooter = "Default Footer", servertz = "Europe/Istanbul", servercolor = main.rebeccapink, twelvehourclock = False):
        self.id = id
        self.serverid = serverid
        self.servertitle = servertitle
        self.serverbeforetext = serverbeforetext
        self.serveraftertext = serveraftertext
        self.serverfooter = serverfooter
        self.servertz = servertz
        self.servercolor = servercolor
        self.twelvehourclock = twelvehourclock
    def create(self):
        main.dbDictCursor.execute("INSERT INTO servertime (serverid, servertitle, serverbeforetext, serveraftertext, serverfooter, servertz, servercolor,twelvehourclock) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)", (self.serverid, self.servertitle, self.serverbeforetext, self.serveraftertext, self.serverfooter, self.servertz, self.servercolor,self.twelvehourclock))
        self.id = main.dbDictCursor.lastrowid
        print("Created new server time with id: " + str(self.id))
        return self
    def update(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if not self.checktzvalid(self.servertz) or self.servercolor < 0 or self.servercolor > 16777215:
            print("Invalid value")
            return False
        main.dbDictCursor.execute("UPDATE servertime SET twelvehourclock = %s ,servertitle = %s, serverbeforetext = %s, serveraftertext = %s, serverfooter = %s, servertz = %s, servercolor = %s WHERE id = %s", (self.twelvehourclock, self.servertitle, self.serverbeforetext, self.serveraftertext, self.serverfooter, self.servertz, self.servercolor, self.id))
        print("Updated server time with id: " + str(self.id))
        return self
    def delete(self):
        if self.id:
            main.dbDictCursor.execute("DELETE FROM servertime WHERE id = %s", (self.id,))
            print("Deleted server time with id: " + str(self.id))
            return True
        else:
            print("Server time not found")
            return False
    def time(self):
        if self.servertz:
            tz = pytz.timezone(self.servertz)
            print("Timezone: " + self.servertz)
        else:
            print("Timezone not found")
            tz = pytz.timezone("Europe/Istanbul")
        if self.twelvehourclock:
            return datetime.datetime.now(tz).strftime("%I:%M %p")
        else:
            return datetime.datetime.now(tz).strftime("%H:%M")
    @staticmethod
    def get(id):
        main.dbDictCursor.execute("SELECT * FROM servertime WHERE id = %s", (id,))
        print("Got server time with id: " + str(id))
        return servertime(**main.dbDictCursor.fetchone())
    @staticmethod
    def getall():
        main.dbDictCursor.execute("SELECT * FROM servertime")
        print("Got all server times")
        return [servertime(**x) for x in main.dbDictCursor.fetchall()]
    @staticmethod
    def findifexists(serverid):
        main.dbDictCursor.execute("SELECT * FROM servertime WHERE serverid = %s", (serverid,))
        result = main.dbDictCursor.fetchone()
        if result is not None:
            print("Found server time with serverid: " + str(serverid))
            return servertime(**result)
        else:
            return None
    @staticmethod
    def checktzvalid(tz):
        if tz in pytz.all_timezones:
            print("Timezone is valid")
            return True
        else:
            print("Timezone is not valid")
            return False
class usertime():
    id : int
    userid : str
    usertitle : str
    userbeforetext : str
    useraftertext : str
    userfooter : str
    usertz : str
    usercolor : int
    twelvehourclock : bool

    def __init__(self,userid, id = None,usertitle = "Default", userbeforetext = "Default", useraftertext = "", userfooter = "Default Footer", usertz = "Europe/Istanbul", usercolor = main.rebeccapink, twelvehourclock = False):
        self.userid = userid
        self.id = id
        self.usertitle = usertitle
        self.userbeforetext = userbeforetext
        self.useraftertext = useraftertext
        self.userfooter = userfooter
        self.usertz = usertz
        self.usercolor = usercolor
        self.twelvehourclock = twelvehourclock

    def create(self):
        main.dbDictCursor.execute("INSERT INTO usertime (twelvehourclock,userid, usertitle, userbeforetext, useraftertext, userfooter, usertz, usercolor) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)", (self.twelvehourclock, self.userid, self.usertitle, self.userbeforetext, self.useraftertext, self.userfooter, self.usertz, self.usercolor))
        self.id = main.dbDictCursor.lastrowid
        print("Created new user time with id: " + str(self.id))
        return self
    def update(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        print(f"This is my object = {self}")
        if not self.checktzvalid(self.usertz) or self.usertz == "None" or self.usercolor < 0 or self.usercolor > 0xFFFFFF:
            print("Invalid value")
            return False
        main.dbDictCursor.execute("UPDATE usertime SET twelvehourclock = %s ,userid = %s, usertitle = %s, userbeforetext = %s, useraftertext = %s, userfooter = %s, usertz = %s, usercolor = %s WHERE id = %s", (self.twelvehourclock, self.userid, self.usertitle, self.userbeforetext, self.useraftertext, self.userfooter, self.usertz, self.usercolor, self.id))
        print("Updated user time with id: " + str(self.id))
        return self
    def delete(self):
        if self.id:
            main.dbDictCursor.execute("DELETE FROM usertime WHERE id = %s", (self.id,))
            print("Deleted user time with id: " + str(self.id))
            return True
        else:
            print("User time not found")
            return False
    def time(self):
        if self.usertz == "None":
            print("User has no timezone")
            return datetime.datetime.now(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
        else:
            print("Got user time")
            if self.twelvehourclock:
                return datetime.datetime.now(pytz.timezone(self.usertz)).strftime("%I:%M %p")
            else:
                return datetime.datetime.now(pytz.timezone(self.usertz)).strftime("%H:%M")
    @staticmethod
    def get(id):
        main.dbDictCursor.execute("SELECT * FROM usertime WHERE id = %s", (id,))
        print("Got user time with id: " + str(id))
        return usertime(**main.dbDictCursor.fetchone())
    @staticmethod
    def getall():
        main.dbDictCursor.execute("SELECT * FROM usertime")
        print("Got all user times")
        return [usertime(**x) for x in main.dbDictCursor.fetchall()]
    @staticmethod
    def findifexists(userid):
        main.dbDictCursor.execute("SELECT * FROM usertime WHERE userid = %s", (userid,))
        result = main.dbDictCursor.fetchone()
        if result is not None:
            print("Found user time with userid: " + str(userid))
            return usertime(**result)
        else:
            print("User time not found")
            return None
    @staticmethod
    def checktzvalid(usertz):
        if usertz in pytz.all_timezones:
            print("Timezone is valid")
            return True
        else:
            print("Timezone is not valid")
            return False
class MemberTime():
    id : int
    userid : str
    serverid : str
    userservertitle : str
    userserverbeforetext : str
    userserveraftertext : str
    userserverfooter : str
    userservertz : str
    userservercolor : int
    twelvehourclock : bool
    def __init__(self,serverid,userid ,id = None, userservertitle = "Default", userserverbeforetext = "Default", userserveraftertext = "", userserverfooter = "Default Footer", userservertz = "Europe/Istanbul", userservercolor = main.rebeccapink,twelvehourclock = False):
        self.id = id
        self.userid = userid
        self.serverid = serverid
        self.userservertitle = userservertitle
        self.userserverbeforetext = userserverbeforetext
        self.userserveraftertext = userserveraftertext
        self.userserverfooter = userserverfooter
        self.userservertz = userservertz
        self.userservercolor = userservercolor
        self.twelvehourclock = twelvehourclock
    def create(self):
        main.dbDictCursor.execute("INSERT INTO membertime (twelvehourclock,userid, serverid, userservertitle, userserverbeforetext, userserveraftertext, userserverfooter, userservertz, userservercolor) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)", (self.twelvehourclock, self.userid, self.serverid, self.userservertitle, self.userserverbeforetext, self.userserveraftertext, self.userserverfooter, self.userservertz, self.userservercolor))
        self.id = main.dbDictCursor.lastrowid
        print("Created new user server time with id: " + str(self.id))
        return self
    def update(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if not self.checktzvalid(self.userservertz) or self.userservertz == "None" or self.userservercolor < 0 or self.userservercolor > 16777215:
            print("Invalid value")
            return False
        print(**kwargs)
        main.dbDictCursor.execute("UPDATE membertime SET twelvehourclock = %s , userid = %s, serverid = %s, userservertitle = %s, userserverbeforetext = %s, userserveraftertext = %s, userserverfooter = %s, userservertz = %s, userservercolor = %s WHERE id = %s", (self.twelvehourclock, self.userid, self.serverid, self.userservertitle, self.userserverbeforetext, self.userserveraftertext, self.userserverfooter, self.userservertz, self.userservercolor, self.id))
        print("Updated user server time with id: " + str(self.id))
        return self
    def delete(self):
        if self.id:
            main.dbDictCursor.execute("DELETE FROM membertime WHERE id = %s", (self.id,))
            print("Deleted user server time with id: " + str(self.id))
            return True
        else:
            print("User server time not found")
            return False
    def time(self):
        if self.userservertz == "None":
            print("User Server has no timezone")
            if self.twelvehourclock:
                return datetime.datetime.now(pytz.timezone("Europe/Istanbul")).strftime("%I:%M %p")
            return datetime.datetime.now(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
        else:
            print("Got user server time")
            if self.twelvehourclock:
                return datetime.datetime.now(pytz.timezone(self.userservertz)).strftime("%I:%M %p")
            else:
                return datetime.datetime.now(pytz.timezone(self.userservertz)).strftime("%H:%M")
    @staticmethod
    def get(id):
        main.dbDictCursor.execute("SELECT * FROM membertime WHERE id = %s", (id,))
        result = main.dbDictCursor.fetchone()
        print("Got user server time with id: " + str(id))
        return MemberTime(**result)
    @staticmethod
    def getall():
        main.dbDictCursor.execute("SELECT * FROM membertime")
        print("Got all user server times")
        result = main.dbDictCursor.fetchall()
        return [MemberTime(**x) for x in result]
    @staticmethod
    def findifexists(userid, serverid):
        main.dbDictCursor.execute("SELECT * FROM membertime WHERE userid = %s AND serverid = %s", (userid, serverid))
        result = main.dbDictCursor.fetchone()
        if result is not None:
            print("Found user server time with userid: " + str(userid) + " and serverid: " + str(serverid))
            return MemberTime(**result)
        else:
            print("User server time not found")
            return None
    @staticmethod
    def checktzvalid(userservertz):
        if userservertz in pytz.all_timezones:
            print("The timezone is valid")
            return True
        else:
            print("The timezone is not valid")
            return False
class Serversettings():
    id : int
    serverid : str
    allowusertime : bool
    allowmembertime : bool
    allowservertime : bool

    def __init__(self,serverid,id = None, allowusertime = True, allowmembertime = True, allowservertime = True):
        self.serverid = serverid
        self.id = id
        self.allowusertime = allowusertime
        self.allowmembertime = allowmembertime
        self.allowservertime = allowservertime
    def create(self):
        main.dbDictCursor.execute("INSERT INTO serversettings (serverid, allowusertime, allowmembertime, allowservertime) VALUES (%s, %s, %s, %s)", (self.serverid, self.allowusertime, self.allowmembertime, self.allowservertime))
        self.id = main.dbDictCursor.lastrowid
        print("Server Settings Added to Database")
        return self
    def update(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        main.dbDictCursor.execute("UPDATE serversettings SET allowusertime = %s, allowmembertime = %s, allowservertime = %s WHERE id = %s", (self.allowusertime, self.allowmembertime, self.allowservertime, self.id))
        print("Server Settings Updated")
        return self
    def delete(self):
        if self.id:
            main.dbDictCursor.execute("DELETE FROM serversettings WHERE id = %s", (self.id,))
            print("Server Settings Deleted")
            return True
        else:
            print("Server Settings Not Deleted")
            return False

    @staticmethod
    def get(id):
        main.dbDictCursor.execute("SELECT * FROM serversettings WHERE id = %s", (id,))
        print("Server Settings Fetched")
        return Serversettings(**main.dbDictCursor.fetchone())
    @staticmethod
    def getall():
        main.dbDictCursor.execute("SELECT * FROM serversettings")
        print("All Server Settings Fetched")
        return [Serversettings(**x) for x in main.dbDictCursor.fetchall()]
    @staticmethod
    def findifexists(serverid):
        main.dbDictCursor.execute("SELECT * FROM serversettings WHERE serverid = %s", (serverid,))
        result = main.dbDictCursor.fetchone()
        if result is not None:
            print("Server Settings Fetched")
            print(result)
            return Serversettings(**result)
        else:
            print("Server Settings Not Found")

            return Serversettings(allowusertime=True, allowmembertime=True, allowservertime=True, serverid=serverid).create()

