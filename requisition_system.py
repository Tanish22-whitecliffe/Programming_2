# requisition_system.py
# Assessment 2 - Requisition System prototype

# Shared data for all requisitions (global, outside __init__)
next_requisition_id = 10001
all_requisitions = []


class Requisition:
    """Holds the details of one staff requisition."""

    def __init__(self, date, staff_id, staff_name):
        global next_requisition_id

        self.date = date
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.requisition_id = next_requisition_id
        next_requisition_id += 1

        self.items = []                    # list of (item_name, cost)
        self.total = 0
        self.status = "Pending"
        self.approval_ref = "Not available"

        all_requisitions.append(self)

    def add_requisition(self, items):
        """Store the items and return the total cost.
        items is a list of (item_name, cost) tuples."""
        self.items = items
        self.total = sum(cost for _, cost in items)
        return self.total


# Simple test - runs only when this file is run directly
if __name__ == "__main__":
    r1 = Requisition("03/04/2024", "FN19", "John Paul")
    total = r1.add_requisition([("Pens", 50), ("Paper", 400)])
    print("Requisition ID:", r1.requisition_id)
    print("Staff Name:", r1.staff_name)
    print("Total: $" + str(total))
    print("Status:", r1.status)

    def approve_requisition(self):
        """Set status automatically based on the total.
        Under $500 is Approved, $500 or more stays Pending."""
        if self.total < 500:
            self.status = "Approved"
            self.approval_ref = "FN" + self.staff_id[2:] + str(self.requisition_id)[-3:]
        else:
            self.status = "Pending"
        return self.status

    def respond_to_requisition(self, decision):
        """Manager sets the status to 'Approved' or 'Not approved'.
        Only works on requisitions that are still Pending."""
        if self.status != "Pending":
            return False
        if decision == "Approved":
            self.status = "Approved"
            self.approval_ref = "FN" + self.staff_id[2:] + str(self.requisition_id)[-3:]
        elif decision == "Not approved":
            self.status = "Not approved"
        else:
            return False
        return True