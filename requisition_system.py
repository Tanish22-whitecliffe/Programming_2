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

    def make_approval_ref(self):
        """Build a reference like FN19001 from staff ID and requisition ID."""
        return "FN" + self.staff_id[2:] + str(self.requisition_id)[-3:]

    def approve_requisition(self):
        """Set status automatically based on the total.
        Under $500 is Approved, $500 or more stays Pending."""
        if self.total < 500:
            self.status = "Approved"
            self.approval_ref = self.make_approval_ref()
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
            self.approval_ref = self.make_approval_ref()
        elif decision == "Not approved":
            self.status = "Not approved"
        else:
            return False
        return True

    @staticmethod
    def display_requisitions():
        """Print the details of every requisition."""
        for r in all_requisitions:
            print("Date:", r.date)
            print("Requisition ID:", r.requisition_id)
            print("Staff ID:", r.staff_id)
            print("Staff Name:", r.staff_name)
            print("Total: $" + str(r.total))
            print("Status:", r.status)
            print("Approval Reference Number:", r.approval_ref)
            print()

    @staticmethod
    def requisition_statistics():
        """Count requisitions by status, print them and return them."""
        stats = {
            "submitted": len(all_requisitions),
            "approved": sum(1 for r in all_requisitions if r.status == "Approved"),
            "pending": sum(1 for r in all_requisitions if r.status == "Pending"),
            "not_approved": sum(1 for r in all_requisitions if r.status == "Not approved"),
        }
        print("Total submitted:", stats["submitted"])
        print("Total approved:", stats["approved"])
        print("Total pending:", stats["pending"])
        print("Total not approved:", stats["not_approved"])
        return stats


# Test scenarios - runs only when this file is run directly
if __name__ == "__main__":
    # 1. Under $500, approved automatically
    r1 = Requisition("03/04/2024", "FN19", "John Paul")
    r1.add_requisition([("Pens", 50), ("Paper", 400)])
    r1.approve_requisition()

    # 2. $500 or more, left pending
    r2 = Requisition("05/04/2024", "FN20", "Tracy Brown")
    r2.add_requisition([("Laptop", 1000)])
    r2.approve_requisition()

    # 3. $500 or more, manager says Not approved
    r3 = Requisition("07/05/2024", "FN15", "Emma Wellington")
    r3.add_requisition([("Desk", 3500)])
    r3.approve_requisition()
    r3.respond_to_requisition("Not approved")

    # 4. Under $500, approved automatically
    r4 = Requisition("03/05/2024", "FN02", "Catlin White")
    r4.add_requisition([("Printer ink", 490)])
    r4.approve_requisition()

    # 5. Exactly $500 (boundary case), left pending
    r5 = Requisition("09/05/2024", "FN30", "Ali Khan")
    r5.add_requisition([("Chair", 500)])
    r5.approve_requisition()

    print("=== Before manager response to r5 ===")
    Requisition.display_requisitions()
    Requisition.requisition_statistics()

    # Manager approves r5
    r5.respond_to_requisition("Approved")

    print("\n=== After manager response to r5 ===")
    Requisition.display_requisitions()
    Requisition.requisition_statistics()