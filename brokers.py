class BaseBroker():

    def get_local(self, arg, theclass):

        return theclass(*arg)