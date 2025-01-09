class Package:
    def __init__(self, new_object):
        # Check if the note is empty or None
        self.note = new_object[7] if new_object[7] is not None and new_object[7] != '' else "no notes provided"
        self.id = new_object[0]
        self.address = new_object[1]
        self.city = new_object[2]
        self.state = new_object[3]
        self.zip = new_object[4]
        self.deadline = new_object[5]
        self.weight = new_object[6]
        self.status = 'in HUB'
        self.time_delivered = None

    # get parameters

    def get_id(self):
        return self.id
        
    def get_address(self):
        return self.address

    def get_city(self):
        return self.city
    
    def get_state(self):
        return self.state
    
    def get_zip(self):
        return self.zip
    
    def get_deadline(self):
        return self.deadline
    
    def get_weight(self):
        return self.weight
    
    def get_address_zip(self):
        return str(self.address) + ',' + str(self.zip)
    
    def get_status(self):
        return self.status
    
    def get_note(self):
        return self.note
    
    def get_time_delivered(self):
        return self.time_delivered
    
    # set parameters

    def set_status(self, string):
        self.status = string

    def set_time_delivered(self, time):
        self.time_delivered = time

    def set_address(self, string):
        self.address = string

    def set_city(self, string):
        self.city = string

    def set_state(self, string):
        self.state = string

    def set_zip(self, string):
        self.zip = string