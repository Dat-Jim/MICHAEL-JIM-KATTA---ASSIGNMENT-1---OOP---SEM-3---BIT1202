"""
Vaccination Tracker - PROG 211 Objected-Oriented Programming
Domain: Health
Follows Digital Public Goods (DPG) principles:
    - Open-Source (hosted on GitHub)
    - Privacy-respecting: only anonymous IDs are stored, no personal
    - Modular and reusable: small classes and functions
"""
from datetime import date


class Vaccine: 
    """A vaccine and how many doses it needs."""
    total_vaccines = 0 # class attribute shared by all Vaccine objects

    def __init__(self, name, doses_required):
        self.name = name
        self.doses_required = doses_required
        Vaccine.total_vaccines += 1

    def display_info(self): # instance method
        print(f"Vaccine: {self.name} | Doses required: {self.doses_required}")

    @classmethod
    def get_total_vaccines(cls): # class method
        return cls.total_vaccines

class Recipient: 
    """An anonymous vaccine recipient (ID and age group only)."""

    AGE_GROUPS = ("child", "adult", "elderly") # tuple: fixed, never changes

    def __init__(self, recipient_id, age_group):
        if not Recipient.is_valid_age_group(age_group):
            raise ValueError(f"Age group must be one of {Recipient. AGE_GROUPS}")
        self.recipient_id = recipient_id
        self.age_group = age_group
        self.doses = [] # each dose is a tuple: (vaccine_name, date_given)

    @staticmethod
    def is_valid_age_group(age_group): # static method
        return age_group in Recipient.AGE_GROUPS

    def doses_received(self, vaccine):
        return sum(1 for name, _ in self.doses if name == vaccine.name)

    def record_dose(self, vaccine, dose_date=None): # interacts with a vaccine objects
        received = self.doses_received(vaccine)
        if received >= vaccine.doses_required:
            print(f"{self.recipient_id}: all {vaccine.doses_required} dose(s) "
                  f"of {vaccine.name} already recorded.")
            return False
        if dose_date is None: 
            dose_date = date.today().isoformat()
        self.doses.append((vaccine.name, dose_date))
        print(f"{self.recipient_id}: {vaccine.name} dose {received + 1} of"
              f"{vaccine.doses_required} recorded ({dose_date})")
        return True

    def vaccination_status(self, vaccine):
        received = self.doses_received(vaccine)
        if received == 0:
            return "Not started"
        if received >= vaccine.doses_required:
            return f"Fully vaccinated ({received}/{vaccine.doses_required})"
        return f"Partially vaccinated ({received}/{vaccine.doses_required})"

    def update_record(self, new_age_group):
        if Recipient.is_valid_age_group(new_age_group):
            self.age_group = new_age_group
            return True
        print("iNVALID AGE GROUP - RECORD NOT UPDATED.")
        return False

    def display_info(self):
        print(f"Recipient ID: {self.recipient_id} | Age group: {self.age_group}")
        for vaccine_name, dose_date in self.doses: # tuple unpacking
            print(f"    - {vaccine_name}on {dose_date}")

# --- Functions that work on the dictionary ---

def add_recipient(registry, recipient):
    """Add a Recipient to the dictionary, using its ID as the key."""
    if recipient.recipient_id in registry: 
        print(f"Record {recipient.recipient_id} already exists - not added.")
        return False 
    registry[recipient.recipient_id] = recipient
    print(f"Added recoord {recipient.recipient_id}")
    return True


def display_all(registry):
    """Loop through the dictionary and display every record."""
    print("\n--- Vaccination Records ---")
    for recipient in registry.values():
        recipient.display_info

def main():
    covid = Vaccine("COVID-19", 2)
    polio = Vaccine("Polio", 3)


    registry = {} # the one ddata structure: dictionaty {ID: Recipient}
    add_recipient(registry, Recipient("R001", "adult"))
    add_recipient(registry, Recipient("R002", "child"))
    add_recipient(registry, Recipient("R001", "elderly")) # duplicate ID test
    
    registry["R001"].record_dose(covid, "2026-09-10")
    registry["R001"].record_dose(covid, "2026-10-01")
    registry["R001"].record_dose(covid, "2026-10-20") # exceeds required
    registry["R002"].record_dose(polio, "2026-09-15")

    display_all(registry)

    print("\n--- Status ---")
    print("R001 -> COVID-19:", registry["R001"].vaccination_status(covid))
    print("R002 -> POLIO:", registry["R002"].vaccination_status(polio))

    print("n\n--- Summary ---")
    covid.display_info()
    print("Tootal vaccines defined:", Vaccine.get_total_vaccines())
    print("Total records:", len(registry))


if __name__ == "__main__":
    main()